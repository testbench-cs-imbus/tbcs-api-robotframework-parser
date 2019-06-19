from typing import List
from test_case_import import RobotParser
from . import MockAPIConnector


def test_import_tests():
    connector = MockAPIConnector([])
    RobotParser(connector).import_tests('../robot_examples')
    assert(connector.call_counter_create_test_case == 3)


def test_update_test_steps_unchanged():
    old_steps: List[dict] = [{
        'id': 0,
        'description': 'step'
    }]
    new_steps: List[str] = ['step']
    connector: MockAPIConnector = MockAPIConnector(old_steps.copy())

    RobotParser(connector).update_test_steps('-1', new_steps, old_steps)

    assert(connector.call_counter_add_test_step == 0)
    assert(connector.call_counter_remove_test_step == 0)
    assert(connector.result_test_steps == old_steps)


def test_update_test_steps_added():
    old_steps: List[dict] = [{
        'id': 0,
        'description': 'step'
    }]
    new_steps: List[str] = ['step', 'another']
    connector: MockAPIConnector = MockAPIConnector(old_steps.copy())

    RobotParser(connector).update_test_steps('-1', new_steps, old_steps)

    expected: List[dict] = [{
        'id': 0,
        'description': 'step'
    }, {
        'id': 1,
        'description': 'another'
    }]
    assert (connector.call_counter_add_test_step == 1)
    assert (connector.call_counter_remove_test_step == 0)
    assert (connector.result_test_steps == expected)


def test_update_test_steps_removed():
    old_steps: List[dict] = [{
        'id': 0,
        'description': 'step'
    }, {
        'id': 1,
        'description': 'another'
    }]
    new_steps: List[str] = ['step']
    connector: MockAPIConnector = MockAPIConnector(old_steps.copy())

    RobotParser(connector).update_test_steps('-1', new_steps, old_steps)

    expected: List[dict] = [{
        'id': 0,
        'description': 'step'
    }]
    assert (connector.call_counter_add_test_step == 0)
    assert (connector.call_counter_remove_test_step == 1)
    assert (connector.result_test_steps == expected)


def test_update_test_steps_replaced():
    old_steps: List[dict] = [{
        'id': 0,
        'description': 'step'
    }, {
        'id': 1,
        'description': 'another'
    }]
    new_steps: List[str] = ['step', 'creative']
    connector: MockAPIConnector = MockAPIConnector(old_steps.copy())

    RobotParser(connector).update_test_steps('-1', new_steps, old_steps)

    expected: List[dict] = [{
        'id': 0,
        'description': 'step'
    }, {
        'id': 1,
        'description': 'creative'
    }]
    assert (connector.call_counter_add_test_step == 1)
    assert (connector.call_counter_remove_test_step == 1)
    assert (connector.result_test_steps == expected)


def test_update_test_steps_reordered():
    old_steps: List[dict] = [{
        'id': 0,
        'description': 'step'
    }, {
        'id': 1,
        'description': 'another'
    }]
    new_steps: List[str] = ['another', 'step']
    connector: MockAPIConnector = MockAPIConnector(old_steps.copy())

    RobotParser(connector).update_test_steps('-1', new_steps, old_steps)

    expected: List[dict] = [{
        'id': 0,
        'description': 'another'
    }, {
        'id': 1,
        'description': 'step'
    }]
    assert (connector.call_counter_add_test_step == 2)
    assert (connector.call_counter_remove_test_step == 2)
    assert (connector.result_test_steps == expected)
