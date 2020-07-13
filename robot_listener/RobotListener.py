import hashlib
import os
from typing import List
from tbcs_client import APIConnector
from test_case_import import RobotParser


class RobotListener:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = '0.1'
    ROBOT_LISTENER_API_VERSION = 2

    __current_file: str = ''
    __current_test_case_id: str = ''
    __current_execution: dict = ''
    __current_execution_counter: int = 0
    __current_execution_id: str = ''
    __connector: APIConnector
    __parser: RobotParser

    def __init__(self, config_file_path: str):
        self.ROBOT_LIBRARY_LISTENER = self
        self.__connector = APIConnector(config_file_path)
        self.__parser = RobotParser(self.__connector)

    def set_connector(self, connector: APIConnector):
        self.__connector = connector
        self.__parser = RobotParser(self.__connector)

    def start_suite(self, name: str, attributes: dict):
        file_path = os.path.normpath(attributes['source'])
        path_elements: List[str] = file_path.split('\\') if os.name == 'nt' else file_path.split('/')
        self.__current_file: str = path_elements[len(path_elements) - 1]
        self.__parser.import_tests_from_file(attributes['source'])

    def start_test(self, name: str, attributes: dict):
        external_id: str = hashlib.sha256((name + self.__current_file).encode('utf-8')).hexdigest()
        self.__current_test_case_id = str(self.__connector.get_test_case_by_external_id(external_id)['id'])
        self.__current_execution_id: str = self.__connector.start_execution(self.__current_test_case_id)
        self.__current_execution = self.__connector.get_execution_by_id(self.__current_test_case_id, self.__current_execution_id)
        self.__current_execution_counter = 0

    def end_keyword(self, name: str, attributes: dict):
        test_step_status: str = APIConnector.test_step_status_passed if attributes['status'] == 'PASS' else APIConnector.test_step_status_failed
        self.__connector.report_step_result(self.__current_test_case_id, str(self.__current_execution['id']), self.__current_execution['testSequence']['testStepBlocks'][2]['steps'][self.__current_execution_counter]['id'] , test_step_status)
        self.__current_execution_counter += 1

    def end_test(self, name: str, attributes: dict):
        self.__connector.update_execution_status(self.__current_test_case_id, self.__current_execution_id, 'Finished')
        test_status: str = APIConnector.test_status_passed if attributes['status'] == 'PASS' else APIConnector.test_status_failed
        print('Der Test ist aus, wir gehn nach Haus')
        self.__connector.report_test_case_result(self.__current_test_case_id, str(self.__current_execution['id']), test_status)

    def log_message(self, log: str):
        #print('Log Message vom Listener:', log.get('message'))
        message = log.get('message')
        #print('Plain Message:', message)
        #print(self.__current_execution)
        #print("=="*25)
        #print("TestCaseID:", self.__current_execution['testCase']['id'], ", ExecutionID:", self.__current_execution_id, ", TestStepID:", self.__current_execution['testSequence']['testStepBlocks'][2]['steps'][self.__current_execution_counter]['id'])
        defect_id = self.__connector.create_defect("TestCaseName", "TestStepName", message)['defectId']
        #print('Habe nen Defect erstellt mit der ID:', defect_id)
        self.__connector.assign_defect(self.__current_execution['testCase']['id'], self.__current_execution_id, self.__current_execution['testSequence']['testStepBlocks'][2]['steps'][self.__current_execution_counter]['id'], defect_id)
        #print('Habe an den ')

