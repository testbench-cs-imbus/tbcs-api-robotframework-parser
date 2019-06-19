from typing import List
import tbcs_client


class MockAPIConnector(tbcs_client.APIConnector):
    call_counter_remove_test_step: int = 0
    call_counter_add_test_step: int = 0
    call_counter_create_test_case: int = 0
    result_test_steps: List[dict]

    def __init__(
            self,
            init_test_steps: List[dict]
    ):
        self.result_test_steps = init_test_steps
        tbcs_client.APIConnector.__init__(self)

    def add_test_step(
            self,
            test_case_id: str,
            test_step: str,
            previous_test_step_id: str = '-1'
    ) -> str:
        # TODO: previous_test_step_id currently gets ignored
        self.call_counter_add_test_step += 1
        new_id: int = 0 if len(self.result_test_steps) == 0 else self.result_test_steps[-1]['id'] + 1
        self.result_test_steps.append({'id': new_id, 'description': test_step})
        return str(new_id)

    def remove_test_step(
            self,
            test_case_id: str,
            test_step_id: str
    ):
        self.call_counter_remove_test_step += 1
        test_step_exists: bool = False
        for index, step in enumerate(self.result_test_steps):
            if str(step['id']) == test_step_id:
                self.result_test_steps.pop(index)
                test_step_exists = True
                break

        if not test_step_exists:
            raise Exception('invalid test step id')

    def create_test_case(
            self,
            test_case_name: str,
            external_id: str,
            test_steps: List[str]
    ) -> str:
        self.call_counter_create_test_case += 1
        return ''

    def get_test_case_by_external_id(
            self,
            external_id: str
    ) -> dict:
        raise tbcs_client.ItemNotFoundError('This mock doesn\'t provide predefined test cases')
