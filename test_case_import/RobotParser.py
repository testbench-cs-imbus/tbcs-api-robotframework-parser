import os
import hashlib
from typing import List
from robot.parsing.model import TestCaseFile
from tbcs_client import ItemNotFoundError
from tbcs_client import APIConnector


class RobotParser:
    __tbcs_api_connector: APIConnector

    def __init__(self, tbcs_api_connector: APIConnector):
        self.__tbcs_api_connector = tbcs_api_connector

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
        path_elements: List[str] = file_path.split('\\') if os.name == 'nt' else file_path.split('/')
        file_name: str = path_elements[len(path_elements) - 1]
        if not file_name.lower().endswith('.robot'):
            return

        test_cases = TestCaseFile(parent=None, source=file_path).populate()
        for test_case in test_cases.testcase_table.tests:
            external_id: str = hashlib.sha256((test_case.name + file_name).encode('utf-8')).hexdigest()
            steps: List[str] = []
            for step in test_case.steps:
                steps.append(f'{step.name}')
            try:
                test: dict = self.__tbcs_api_connector.get_test_case_by_external_id(external_id)
                self.update_test_steps(str(test['id']), steps, test['testSequence']['testStepBlocks'][2]['steps'])
            except ItemNotFoundError:
                self.__tbcs_api_connector.create_test_case(test_case.name, APIConnector.test_case_type_structured, external_id, steps)

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
