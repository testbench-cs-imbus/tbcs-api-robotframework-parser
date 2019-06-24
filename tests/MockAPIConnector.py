from typing import List
import tbcs_client


class MockAPIConnector(tbcs_client.APIConnector):
    call_counter_remove_test_step: int = 0
    call_counter_add_test_step: int = 0
    call_counter_create_test_case: int = 0
    call_counter_get_test_case_by_external_id: int = 0
    call_counter_start_execution: int = 0
    call_counter_report_step_result: int = 0
    call_counter_report_test_case_result: int = 0
    test_cases: List[dict]

    def __init__(
            self,
            init_test_cases: List[dict] = None
    ):
        self.test_cases = init_test_cases if init_test_cases is not None else []
        tbcs_client.APIConnector.__init__(self)

    def add_test_step(
            self,
            test_case_id: str,
            test_step: str,
            previous_test_step_id: str = '-1'
    ) -> str:
        self.call_counter_add_test_step += 1
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                new_index: int = self.__find_next_index(test_case['testSteps'])
                test_case['testSteps'].append({'id': new_index, 'description': test_step})
                return str(new_index)

    def remove_test_step(
            self,
            test_case_id: str,
            test_step_id: str
    ):
        self.call_counter_remove_test_step += 1
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                for index, step in enumerate(test_case['testSteps']):
                    if str(step['id']) == test_step_id:
                        test_case['testSteps'].pop(index)
                        return
                raise tbcs_client.ItemNotFoundError(f'Test step {test_step_id} not found in test case {test_case_id}.')
        raise tbcs_client.ItemNotFoundError(f'No test case found with Id {test_case_id}.')

    def create_test_case(
            self,
            test_case_name: str,
            external_id: str,
            test_steps: List[str]
    ) -> str:
        self.call_counter_create_test_case += 1
        new_index: int = self.__find_next_index(self.test_cases)
        test_case: dict =  {
            'id': new_index,
            'name': test_case_name,
            'externalId': external_id,
            'testSteps': [],
            'executions': []
        }
        for index, test_step in enumerate(test_steps):
            test_case['testSteps'].append({
                'id': index,
                'description': test_step
            })
        self.test_cases.append(test_case)
        return str(new_index)

    def get_test_case_by_external_id(
            self,
            external_id: str
    ) -> dict:
        self.call_counter_get_test_case_by_external_id += 1
        for test_case in self.test_cases:
            if test_case['externalId'] == external_id:
                return test_case
        raise tbcs_client.ItemNotFoundError(f'No item with external ID {external_id} found.')

    def start_execution(
            self,
            test_case_id: str
    ) -> str:
        self.call_counter_start_execution += 1
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                new_index: int = self.__find_next_index(test_case['executions'])
                execution: dict = {
                    'id': new_index,
                    'result': self.test_status_in_progress,
                    'testStepBlocks': [{}, {}, {
                        'steps': []
                    }]
                }
                for step in test_case['testSteps']:
                    execution['testStepBlocks'][2]['steps'].append({
                        'id': step['id'],
                        'description': step['description']
                    })
                test_case['executions'].append(execution)
                return str(new_index)
        raise tbcs_client.ItemNotFoundError(f'No test case with ID {test_case_id}.')

    def get_execution_by_id(
            self,
            test_case_id: str,
            execution_id: str
    ) -> dict:
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                for execution in test_case['executions']:
                    if str(execution['id']) == execution_id:
                        return execution
                raise tbcs_client.ItemNotFoundError(f'No execution with ID {execution_id}.')
        raise tbcs_client.ItemNotFoundError(f'No test case with ID {test_case_id}.')

    def report_step_result(
            self,
            test_case_id: str,
            execution_id: str,
            test_step_id: str,
            result: str
    ):
        self.call_counter_report_step_result += 1
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                for execution in test_case['executions']:
                    if str(execution['id']) == execution_id:
                        for step in execution['testStepBlocks'][2]['steps']:
                            if str(step['id']) == test_step_id:
                                step['result'] = result
                                return
                        raise tbcs_client.ItemNotFoundError(f'No test step with ID {test_step_id}.')
                raise tbcs_client.ItemNotFoundError(f'No execution with ID {execution_id}.')
        raise tbcs_client.ItemNotFoundError(f'No test case with ID {test_case_id}.')

    def report_test_case_result(
            self,
            test_case_id: str,
            execution_id: str,
            result: str
    ):
        self.call_counter_report_test_case_result += 1
        for test_case in self.test_cases:
            if str(test_case['id']) == test_case_id:
                for execution in test_case['executions']:
                    if str(execution['id']) == execution_id:
                        execution['result'] = result
                        return
                raise tbcs_client.ItemNotFoundError(f'No execution with ID {execution_id}.')
        raise tbcs_client.ItemNotFoundError(f'No test case with ID {test_case_id}.')

    @staticmethod
    def __find_next_index(source: List[dict]):
        if len(source) == 0:
            return 0
        else:
            max_index: int = 0
            for item in source:
                if item['id'] > max_index:
                    max_index = item['id']
            return max_index + 1
