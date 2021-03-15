import hashlib
import os, traceback
from typing import List, Dict
from robot_listener.TestExecutionModel import TestCaseModel, TestStepModel
from tbcs_client import APIConnector


class RobotListener:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = '0.1'
    ROBOT_LISTENER_API_VERSION = 2

    __current_file: str
    __current_test_case: TestCaseModel
    __current_keyword_depth: int = 0
    __last_error_message: str
    __keyword_counter: int = 0
    __connector: APIConnector

    def __init__(self, config_file_path: str):
        self.ROBOT_LIBRARY_LISTENER = self
        self.__connector = APIConnector(config_file_path)
        self.__connector.log_in()

    def set_connector(self, connector: APIConnector):
        self.__connector = connector

    def start_suite(self, name: str, attributes: Dict):
        file_path = os.path.normpath(attributes['source'])
        path_elements: List[str] = file_path.split('\\') if os.name == 'nt' else file_path.split('/')
        self.__current_file: str = path_elements[len(path_elements) - 1]

    def start_test(self, name: str, attributes: Dict):
        external_id: str = hashlib.sha256((name + self.__current_file).encode('utf-8')).hexdigest()
        description: str = attributes['doc'] if not attributes['doc'] == '' else attributes['longname']
        self.__current_test_case = TestCaseModel('start', name, description, APIConnector.TEST_CASE_TYPE_STRUCTURED, external_id)

    def start_keyword(self, name: str, attributes: Dict):
        self.__current_keyword_depth += 1
        self.__keyword_counter += 1

    def end_keyword(self, name: str, attributes: dict):
        if self.__current_keyword_depth == 1:
            arguments_string: str = ''
            for argument in attributes['args']:
                arguments_string += ' ' + argument
            test_step: TestStepModel = TestStepModel(str(self.__keyword_counter), attributes['kwname'] + arguments_string)

            if attributes['status'] == 'PASS':
                test_step.set_result(APIConnector.TEST_STEP_STATUS_PASSED)
            elif attributes['status'] == 'FAIL':
                test_step.set_result(APIConnector.TEST_STEP_STATUS_FAILED, self.__last_error_message)
                self.__last_error_message = ''

            if attributes['type'] == 'Setup':
                self.__current_test_case.test_block_preparation.append(test_step)
            elif attributes['type'] == 'Teardown':
                self.__current_test_case.test_block_cleanup.append(test_step)
            else:
                self.__current_test_case.test_block_test.append(test_step)

        self.__current_keyword_depth -= 1

    def end_test(self, name: str, attributes: dict):
        try:
            self.__current_test_case.write_to_testbench(self.__connector)
        except Exception:
            print("\nWarning: An error occured while reporting the test. Results may not be available in TestBench.")
            traceback.print_exc()

        self.__current_keyword_depth = 0
        self.__keyword_counter = 0

    def log_message(self, message: Dict):
        if message['level'] == 'FAIL':
            self.__last_error_message = message['message']
