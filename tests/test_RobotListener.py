import pytest

from tests.MockAPIConnector import MockAPIConnector
from robot_listener import RobotListener, TestCaseModel, TestStepModel
from robot.api import TestSuiteBuilder


def test_synchronization_new_test_case_no_error():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('one', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('two', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    connector: MockAPIConnector = MockAPIConnector()

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 1)
    assert (connector.call_counter_add_test_step == 2)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 2)
    assert (connector.call_counter_create_defect == 0)
    assert (connector.call_counter_assign_defect == 0)
    assert (test_case.get_identifier() == "1")
    assert (test_case.test_block_test[0].get_identifier() == "1")


def test_synchronization_new_test_case_with_error():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('one', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('two', 'second step', MockAPIConnector.TEST_STEP_STATUS_FAILED))

    connector: MockAPIConnector = MockAPIConnector()

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 1)
    assert (connector.call_counter_add_test_step == 2)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 2)
    assert (connector.call_counter_create_defect == 1)
    assert (connector.call_counter_assign_defect == 1)


def test_synchronization_existing_test_case_no_changes():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('one', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('two', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    old_test_case: TestCaseModel = TestCaseModel('1', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    old_test_case.test_block_test.append(TestStepModel('1', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    old_test_case.test_block_test.append(TestStepModel('2', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    connector: MockAPIConnector = MockAPIConnector()
    connector.test_cases.append(old_test_case)

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 0)
    assert (connector.call_counter_add_test_step == 0)
    assert (connector.call_counter_remove_test_step == 0)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 2)
    assert (test_case.get_identifier() == "1")
    assert (test_case.test_block_test[0].get_identifier() == "1")


def test_synchronization_existing_test_case_additional_test_steps():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('one', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('two', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('three', 'third step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    old_test_case: TestCaseModel = TestCaseModel('1', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    old_test_case.test_block_test.append(TestStepModel('1', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    old_test_case.test_block_test.append(TestStepModel('2', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    connector: MockAPIConnector = MockAPIConnector()
    connector.test_cases.append(old_test_case)

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 0)
    assert (connector.call_counter_add_test_step == 3)
    assert (connector.call_counter_remove_test_step == 2)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 3)
    assert (test_case.test_block_test[2].get_identifier() == "3")


def test_synchronization_existing_test_case_missing_test_steps():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('one', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    old_test_case: TestCaseModel = TestCaseModel('1', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    old_test_case.test_block_test.append(TestStepModel('1', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    old_test_case.test_block_test.append(TestStepModel('2', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    connector: MockAPIConnector = MockAPIConnector()
    connector.test_cases.append(old_test_case)

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 0)
    assert (connector.call_counter_add_test_step == 1)
    assert (connector.call_counter_remove_test_step == 2)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 1)


def test_synchronization_existing_test_case_test_steps_changed():
    test_case: TestCaseModel = TestCaseModel('one', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    test_case.test_block_test.append(TestStepModel('three', 'third step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    test_case.test_block_test.append(TestStepModel('four', 'fourth step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    old_test_case: TestCaseModel = TestCaseModel('1', 'test', 'description', MockAPIConnector.TEST_CASE_TYPE_STRUCTURED, '1')
    old_test_case.test_block_test.append(TestStepModel('1', 'first step', MockAPIConnector.TEST_STEP_STATUS_PASSED))
    old_test_case.test_block_test.append(TestStepModel('2', 'second step', MockAPIConnector.TEST_STEP_STATUS_PASSED))

    connector: MockAPIConnector = MockAPIConnector()
    connector.test_cases.append(old_test_case)

    test_case.write_to_testbench(connector)
    assert (connector.call_counter_create_test_case == 0)
    assert (connector.call_counter_add_test_step == 2)
    assert (connector.call_counter_remove_test_step == 2)
    assert (connector.call_counter_start_execution == 1)
    assert (connector.call_counter_report_step_result == 2)


@pytest.mark.dependency(depends=["test_synchronization_new_test_case_with_error", "test_synchronization_existing_test_case_no_changes"])
def test_listener():
    connector: MockAPIConnector = MockAPIConnector()
    listener: RobotListener = RobotListener('../tbcs.config.json')
    listener.set_connector(connector)
    suite = TestSuiteBuilder().build('../robot_examples')

    suite.run(listener=listener)

    assert (connector.call_counter_get_test_case_by_external_id == 3)
    assert (connector.call_counter_create_test_case == 3)
    assert (connector.call_counter_remove_test_step == 0)
    assert (connector.call_counter_add_test_step == 7)
    assert (connector.call_counter_start_execution == 3)
    assert (connector.call_counter_report_step_result == 7)
    assert (connector.call_counter_create_defect == 1)
    assert (connector.call_counter_assign_defect == 1)
