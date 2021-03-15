from typing import List
from tbcs_client import APIConnector, ItemNotFoundError
from robot_listener import TestCaseModel, TestStepModel


# TODO write unit tests for this
class MockAPIConnector(APIConnector):
    call_counter_create_test_case: int = 0
    call_counter_add_test_step: int = 0
    call_counter_remove_test_step: int = 0
    call_counter_get_test_case_by_external_id: int = 0
    call_counter_get_test_case_by_id: int = 0
    call_counter_start_execution: int = 0
    call_counter_report_step_result: int = 0
    call_counter_create_defect: int = 0
    call_counter_assign_defect: int = 0
    test_cases: List[TestCaseModel]

    def __init__(self):
        APIConnector.__init__(self)
        self.test_cases = []

    def create_test_case(
            self,
            test_case_name: str,
            test_case_description: str,
            test_case_type: str,
            external_id: str,
    ) -> str:
        self.call_counter_create_test_case += 1
        new_index: str = str(self.call_counter_create_test_case)
        self.test_cases.append(TestCaseModel(
            new_index,
            test_case_name,
            test_case_description,
            test_case_description,
            external_id
        ))

        return new_index

    def add_test_step(
            self,
            test_case_id: str,
            test_step: str,
            previous_test_step_id: str = '-1',
            test_block_name: str = APIConnector.TEST_BLOCK_TEST_NAME
    ) -> str:
        self.call_counter_add_test_step += 1
        new_index = str(self.call_counter_add_test_step)
        test_case: TestCaseModel = self.__get_test_case_by_id(test_case_id)
        test_block: List[TestStepModel] = test_case.get_test_block_by_name(test_block_name)
        new_test_step: TestStepModel = TestStepModel(str(self.call_counter_add_test_step), test_step)
        if previous_test_step_id == '-1':
            test_block.append(new_test_step)
            return new_index
        else:
            for ts_index, test_step in enumerate(test_block):
                if test_step.get_identifier() == previous_test_step_id:
                    test_block.insert(ts_index, new_test_step)
                    return new_index
        raise ItemNotFoundError(f'Test step {previous_test_step_id} not found in test case {test_case_id}.')

    def remove_test_step(
            self,
            test_case_id: str,
            test_step_id: str,
            test_block_name: str = APIConnector.TEST_BLOCK_TEST_NAME
    ) -> None:
        self.call_counter_remove_test_step += 1
        test_case: TestCaseModel = self.__get_test_case_by_id(test_case_id)
        test_block: List[TestStepModel] = test_case.get_test_block_by_name(test_block_name)
        for ts_index, test_step in enumerate(test_block):
            if test_step.get_identifier() == test_step_id:
                test_block.remove(test_step)
                return
        raise ItemNotFoundError(f'Test step {test_step_id} not found in test case {test_case_id}.')

    def get_test_case_by_external_id(
            self,
            external_id: str
    ) -> dict:
        self.call_counter_get_test_case_by_external_id += 1
        for tc_index, test_case in enumerate(self.test_cases):
            if test_case.get_external_id() == external_id:
                return test_case.to_dict()
        raise ItemNotFoundError(f'No test case found with externalId {external_id}.')

    def get_test_case_by_id(
            self,
            test_case_id: str
    ) -> dict:
        self.call_counter_get_test_case_by_id += 1
        return self.__get_test_case_by_id(test_case_id).to_dict()

    def start_execution(
            self,
            test_case_id: str
    ) -> str:
        self.call_counter_start_execution += 1
        self.__get_test_case_by_id(test_case_id)
        return str(self.call_counter_start_execution)

    def report_step_result(
            self,
            test_case_id: str,
            execution_id: str,
            test_step_id: str,
            result: str
    ) -> None:
        self.call_counter_report_step_result += 1
        self.__get_test_case_by_id(test_case_id).get_test_step_by_id(test_step_id).set_result(result)

    def create_defect(
            self,
            name: str,
            message: str
    ) -> str:
        self.call_counter_create_defect += 1

        return str(self.call_counter_create_defect)

    def assign_defect(
            self,
            test_case_id: str,
            execution_id: str,
            test_step_id: str,
            defect_id: str
    ) -> None:
        self.call_counter_assign_defect += 1
        self.__get_test_case_by_id(test_case_id).get_test_step_by_id(test_step_id)

    def __get_test_case_by_id(
            self,
            test_case_id: str
    ) -> TestCaseModel:
        for tc_index, test_case in enumerate(self.test_cases):
            if test_case.get_identifier() == test_case_id:
                return test_case
        raise ItemNotFoundError(f'No test case with ID {test_case_id}.')
