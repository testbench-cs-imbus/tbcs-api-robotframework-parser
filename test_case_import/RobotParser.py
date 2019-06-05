import os
from tbcs_client import APIConnector
from typing import List
from robot.parsing.model import TestCaseFile


class RobotParser:
    __tbcs_api_connector: APIConnector

    def __init__(self, tbcs_api_connector: APIConnector):
        self.__tbcs_api_connector = tbcs_api_connector

    def import_tests(self, test_root_path: str):
        for dirName, subdirList, fileList in os.walk(test_root_path):
            for fileName in fileList:
                if fileName.endswith('.robot'):
                    test_cases = TestCaseFile(parent=None, source=os.path.join(dirName, fileName)).populate()
                    for test_case in test_cases.testcase_table.tests:
                        external_id: str = test_case.name
                        steps: List[str] = []
                        for step in test_case.steps:
                            steps.append(step.name)
                        if not self.__check_test_exists(external_id):
                            self.__tbcs_api_connector.create_test_case(test_case.name, external_id, steps)

    def __check_test_exists(self, external_id) -> bool:
        # TODO: Use externalID for check -> not yet implemented in CS
        return False
