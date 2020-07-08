import os
import hashlib
from typing import List
from tbcs_client import ItemNotFoundError
from tbcs_client import APIConnector

import ast
import astpretty
from robot.api import get_model

class Visitor(ast.NodeVisitor):

    #__tbcs_api_connector: APIConnector
    #testSteps: List[str] = []
    #testCaseName: str
    #external_id = 5


    def __init__(self, tbcs_api_connector: APIConnector):
        self.__tbcs_api_connector = tbcs_api_connector
        self.testSteps: List[str] = []
        self.fileSource: str = ''
        self.testCaseName: str = ''
        self.external_id: str = ''


    def visit_File(self, node):
        #print(f"File '{node.source}' has following tests:")
        # Must call `generic_visit` to visit also child nodes.
        self.fileSource = f'{node.source}'
        self.generic_visit(node)

    def visit_TestCase(self, node):
        self.testSteps = []
        self.testCaseName = ''
        #print(self.testSteps, self.testCaseName)
        self.generic_visit(node)
        #print(self.testCaseName, type(self.testCaseName),self.testSteps)
        #print(self.fileSource)
        #self.external_id = hashlib.sha256((self.testCaseName+self.fileSource).encode('utf-8')).hexdigest() ##quick-fix ID, eher schlechte Idee, da der Listener damit arbeitet
        path_elements: List[str] = self.fileSource.split('\\') if os.name == 'nt' else self.fileSource.split('/')
        file_name: str = path_elements[len(path_elements) - 1]
        #print(file_name)
        self.external_id = hashlib.sha256((self.testCaseName+file_name).encode('utf-8')).hexdigest()
        try:
            test: dict = self.__tbcs_api_connector.get_test_case_by_external_id(self.external_id)
            self.update_test_steps(str(test['id']), self.testSteps, test['testSequence']['testStepBlocks'][2]['steps'])
        except ItemNotFoundError:
            self.__tbcs_api_connector.create_test_case(self.testCaseName, APIConnector.test_case_type_structured, self.external_id, self.testSteps)

    def visit_TestCaseName(self, node):
        self.testCaseName = node.name
        #print(self.testCaseName)
        #print(testCaseName)
        #self.generic_visit(node)

    def visit_KeywordCall(self, node):
        # print(f"{node.type}")
        # teststeps . add (node.bla)
        token = node.get_token('KEYWORD')
        self.testSteps.append(token.value)
        #print(self.testSteps)
    
    #def visit_Token(self, node):
        #print("{node.type}"+"{node.value}")

    """ Method to update test steps for an existing test case if necessary """
    def update_test_steps(self, test_case_id: str, steps_new: List[str], steps_old: List[dict]):
        # TODO: Performance could be increased by implementing a smarter algorithm
        if len(steps_new) < len(steps_old):
            for index, old_step in enumerate(steps_old):
                if index >= len(steps_new):
                    self.__tbcs_api_connector.remove_test_step(test_case_id, str(old_step['id']))

        change_index: int = -1
        for index, old_step in enumerate(steps_old):
            if index >= len(steps_new):
                break
            if not old_step['description'] == steps_new[index]:
                change_index = index
                break

        if change_index == -1:
            if len(steps_new) > len(steps_old):
                for index, old_step in enumerate(steps_old, len(steps_old)):
                    self.__tbcs_api_connector.add_test_step(test_case_id, steps_new[index])
            return
        else:
            for index, old_step in enumerate(steps_old):
                if index >= change_index:
                    self.__tbcs_api_connector.remove_test_step(test_case_id, str(old_step['id']))
            for index, new_step in enumerate(steps_new):
                if index >= change_index:
                    self.__tbcs_api_connector.add_test_step(test_case_id, new_step)


class RobotParser:
    __tbcs_api_connector: APIConnector
    __visitor: Visitor

    def __init__(self, tbcs_api_connector: APIConnector):
        self.__tbcs_api_connector = tbcs_api_connector
        self.__visitor = Visitor(tbcs_api_connector)

    """ Method to import tests from robot files into TestBench CS  
    
    All robot tests from a given directory and all subdirectories are imported into the TestBench CS instance
    provided in your tbcs.config.json. 
    """
    def import_tests_from_directory(self, test_root_path: str):
        for dirName, subdirList, fileList in os.walk(test_root_path):
            for fileName in fileList:
                if fileName.lower().endswith('.robot'):
                    self.import_tests_from_file(os.path.join(dirName, fileName))

    def import_tests_from_file(self, file_path: str):
        file_path = os.path.normpath(file_path)

        #path_elements wird erstmal nicht genutzt → mal schauen, ob es Win/Linux-Probleme gibt; dann \\↔/ tauschen
        path_elements: List[str] = file_path.split('\\') if os.name == 'nt' else file_path.split('/')
        file_name: str = path_elements[len(path_elements) - 1]

        if not file_name.lower().endswith('.robot'):
            return

        test_case = get_model(file_path)
        #astpretty.pprint(test_case)
        
        self.__visitor.visit(test_case)