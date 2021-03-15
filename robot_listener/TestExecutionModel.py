from typing import List, Dict
from tbcs_client import APIError, ItemNotFoundError, APIConnector


class TestStepModel:
    __identifier: str
    __description: str
    __result: str
    __error_message: str
    test_steps: List['TestStepModel']

    def __init__(self, identifier: str, description: str, result: str = APIConnector.TEST_STEP_STATUS_UNDEFINED, error_message: str = ''):
        self.__identifier = identifier
        self.__description = description
        self.__result = result
        self.__error_message = error_message

    def get_identifier(self) -> str:
        return self.__identifier

    def set_identifier(self, identifier: str) -> None:
        self.__identifier = identifier

    def get_description(self) -> str:
        return self.__description

    def get_result(self) -> str:
        return self.__result

    def get_error_message(self) -> str:
        return self.__error_message

    def set_result(self, result: str, error_message: str = '') -> None:
        self.__result = result
        self.__error_message = error_message

    def write_to_testbench(self, connector: APIConnector, test_case_id: str, test_block: str, previous_test_step_id: str = '-1') -> None:
        # TODO support nested test steps
        self.__identifier = connector.add_test_step(test_case_id, self.__description, previous_test_step_id, test_block)

    def report_to_testbench(self, connector: APIConnector, test_case_id: str, execution_id: str) -> None:
        # TODO support nested test steps
        connector.report_step_result(test_case_id, execution_id, self.__identifier, self.__result)

        if self.__result == APIConnector.TEST_STEP_STATUS_FAILED:
            defect_id: str = connector.create_defect(f'Execution {execution_id} - {self.__description}', self.__error_message)
            connector.assign_defect(test_case_id, execution_id, self.__identifier, defect_id)


class TestCaseModel:
    __identifier: str
    __name: str
    __description: str
    __type: str
    __external_id: str
    test_block_preparation: List[TestStepModel]
    test_block_navigation: List[TestStepModel]
    test_block_test: List[TestStepModel]
    test_block_resultCheck: List[TestStepModel]
    test_block_cleanup: List[TestStepModel]

    def __init__(self, identifier: str, name: str, description: str, type: str, external_id: str):
        self.__identifier = identifier
        self.__name = name
        self.__description = description
        self.__type = type
        self.__external_id = external_id
        self.test_block_preparation = []
        self.test_block_navigation = []
        self.test_block_test = []
        self.test_block_resultCheck = []
        self.test_block_cleanup = []

    def get_identifier(self) -> str:
        return self.__identifier

    def get_external_id(self) -> str:
        return self.__external_id

    def get_test_block_by_name(self, test_block_name: str) -> List[TestStepModel]:
        if test_block_name == APIConnector.TEST_BLOCK_PREPARATION_NAME:
            return self.test_block_preparation
        elif test_block_name == APIConnector.TEST_BLOCK_NAVIGATION_NAME:
            return self.test_block_navigation
        elif test_block_name == APIConnector.TEST_BLOCK_TEST_NAME:
            return self.test_block_test
        elif test_block_name == APIConnector.TEST_BLOCK_RESULTCHECK_NAME:
            return self.test_block_resultCheck
        elif test_block_name == APIConnector.TEST_BLOCK_CLEANUP_NAME:
            return self.test_block_cleanup
        else:
            raise APIError(f'TestBlock {test_block_name} does not exist')

    def get_test_step_by_id(self, test_step_id: str) -> TestStepModel:
        # TODO support nested test steps
        for test_step in self.test_block_preparation:
            if test_step.get_identifier() == test_step_id:
                return test_step
        for test_step in self.test_block_navigation:
            if test_step.get_identifier() == test_step_id:
                return test_step
        for test_step in self.test_block_test:
            if test_step.get_identifier() == test_step_id:
                return test_step
        for test_step in self.test_block_resultCheck:
            if test_step.get_identifier() == test_step_id:
                return test_step
        for test_step in self.test_block_cleanup:
            if test_step.get_identifier() == test_step_id:
                return test_step
        raise ItemNotFoundError(f'No test step with ID {test_step_id}.')

    def to_dict(self) -> Dict:
        # TODO support nested test steps
        return {
            'id': self.__identifier,
            'testCaseType': self.__type,
            'name': self.__name,
            'description': self.__description,
            'automation': {
                'externalId': self.__external_id
            },
            'testSequence': {
                'testStepBlocks': [
                    {
                        'id': APIConnector.TEST_BLOCK_PREPARATION_INDEX,
                        'name': APIConnector.TEST_BLOCK_PREPARATION_NAME,
                        'steps': self.__test_block_to_dict(self.test_block_preparation)
                    }, {
                        'id': APIConnector.TEST_BLOCK_NAVIGATION_INDEX,
                        'name': APIConnector.TEST_BLOCK_NAVIGATION_NAME,
                        'steps': self.__test_block_to_dict(self.test_block_navigation)
                    }, {
                        'id': APIConnector.TEST_BLOCK_TEST_INDEX,
                        'name': APIConnector.TEST_BLOCK_TEST_NAME,
                        'steps': self.__test_block_to_dict(self.test_block_test)
                    },{
                        'id': APIConnector.TEST_BLOCK_RESULTCHECK_INDEX,
                        'name': APIConnector.TEST_BLOCK_RESULTCHECK_NAME,
                        'steps': self.__test_block_to_dict(self.test_block_resultCheck)
                    }, {
                        'id': APIConnector.TEST_BLOCK_CLEANUP_INDEX,
                        'name': APIConnector.TEST_BLOCK_CLEANUP_NAME,
                        'steps': self.__test_block_to_dict(self.test_block_cleanup)
                    }
                ]
            }
        }

    @staticmethod
    def __test_block_to_dict(test_block: List[TestStepModel]) -> List[Dict]:
        target_list: List[Dict] = []
        for test_step in test_block:
            target_list.append({
                'id': test_step.get_identifier(),
                'description': test_step.get_description()
            })
        return target_list

    def write_to_testbench(self, connector: APIConnector) -> None:
        try:
            remote_test_case: dict = connector.get_test_case_by_external_id(self.__external_id)
            self.__identifier = remote_test_case['id']

            if not remote_test_case['description'] == self.__description:
                connector.update_test_case_description(self.__identifier, self.__description)

            self.__update_test_block_to_testbench(connector, self.test_block_preparation, APIConnector.TEST_BLOCK_PREPARATION_NAME, remote_test_case['testSequence']['testStepBlocks'][APIConnector.TEST_BLOCK_PREPARATION_INDEX]['steps'])
            self.__update_test_block_to_testbench(connector, self.test_block_navigation, APIConnector.TEST_BLOCK_NAVIGATION_NAME, remote_test_case['testSequence']['testStepBlocks'][APIConnector.TEST_BLOCK_NAVIGATION_INDEX]['steps'])
            self.__update_test_block_to_testbench(connector, self.test_block_test, APIConnector.TEST_BLOCK_TEST_NAME, remote_test_case['testSequence']['testStepBlocks'][APIConnector.TEST_BLOCK_TEST_INDEX]['steps'])
            self.__update_test_block_to_testbench(connector, self.test_block_resultCheck, APIConnector.TEST_BLOCK_RESULTCHECK_NAME, remote_test_case['testSequence']['testStepBlocks'][APIConnector.TEST_BLOCK_RESULTCHECK_INDEX]['steps'])
            self.__update_test_block_to_testbench(connector, self.test_block_cleanup, APIConnector.TEST_BLOCK_CLEANUP_NAME, remote_test_case['testSequence']['testStepBlocks'][APIConnector.TEST_BLOCK_CLEANUP_INDEX]['steps'])
        except ItemNotFoundError:
            self.__identifier = connector.create_test_case(self.__name, self.__description, self.__type, self.__external_id)
            for test_step in self.test_block_preparation:
                test_step.write_to_testbench(connector, self.__identifier, APIConnector.TEST_BLOCK_PREPARATION_NAME)
            for test_step in self.test_block_navigation:
                test_step.write_to_testbench(connector, self.__identifier, APIConnector.TEST_BLOCK_NAVIGATION_NAME)
            for test_step in self.test_block_test:
                test_step.write_to_testbench(connector, self.__identifier, APIConnector.TEST_BLOCK_TEST_NAME)
            for test_step in self.test_block_resultCheck:
                test_step.write_to_testbench(connector, self.__identifier, APIConnector.TEST_BLOCK_RESULTCHECK_NAME)
            for test_step in self.test_block_cleanup:
                test_step.write_to_testbench(connector, self.__identifier, APIConnector.TEST_BLOCK_CLEANUP_NAME)

        execution_id: str = connector.start_execution(self.__identifier)
        for test_step in self.test_block_preparation:
            test_step.report_to_testbench(connector, self.__identifier, execution_id)
        for test_step in self.test_block_navigation:
            test_step.report_to_testbench(connector, self.__identifier, execution_id)
        for test_step in self.test_block_test:
            test_step.report_to_testbench(connector, self.__identifier, execution_id)
        for test_step in self.test_block_resultCheck:
            test_step.report_to_testbench(connector, self.__identifier, execution_id)
        for test_step in self.test_block_cleanup:
            test_step.report_to_testbench(connector, self.__identifier, execution_id)

    def __update_test_block_to_testbench(self, connector: APIConnector, test_block: List[TestStepModel], test_block_name: str, remote_test_steps: List[Dict]) -> None:
        # TODO support nested test steps
        needs_update: bool = False
        if len(test_block) != len(remote_test_steps):
            needs_update = True
        else:
            for index, test_step in enumerate(test_block):
                if test_step.get_description() == remote_test_steps[index]['description']:
                    test_step.set_identifier(remote_test_steps[index]['id'])
                else:
                    needs_update = True
                    break

        if not needs_update:
            return
        else:
            for remote_test_step in remote_test_steps:
                connector.remove_test_step(self.get_identifier(), remote_test_step['id'], test_block_name)
            for test_step in test_block:
                test_step.write_to_testbench(connector, self.__identifier, test_block_name)
