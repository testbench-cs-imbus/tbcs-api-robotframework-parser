from typing import List
from test_case_import import RobotParser
from tests.MockAPIConnector import MockAPIConnector


def test_import_tests_from_directory():
    connector = MockAPIConnector()
    RobotParser(connector).import_tests_from_directory('../robot_examples')
    assert(connector.call_counter_create_test_case == 3)


def test_import_tests_from_file():
    connector = MockAPIConnector()
    RobotParser(connector).import_tests_from_file('../robot_examples/toplevel.robot')
    assert(connector.call_counter_create_test_case == 1)


def test_update_test_steps_unchanged():
    old_test_cases: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }]
    }]
    new_steps: List[str] = ['step']
    connector: MockAPIConnector = MockAPIConnector(old_test_cases.copy())

    RobotParser(connector).update_test_steps('1', new_steps, old_test_cases[0]['testSteps'].copy())

    assert(connector.call_counter_add_test_step == 0)
    assert(connector.call_counter_remove_test_step == 0)
    assert(connector.test_cases == old_test_cases)


def test_update_test_steps_added():
    old_test_cases: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }]
    }]
    new_steps: List[str] = ['step', 'another']
    connector: MockAPIConnector = MockAPIConnector(old_test_cases.copy())

    RobotParser(connector).update_test_steps('1', new_steps, old_test_cases[0]['testSteps'].copy())

    expected: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }, {
            'id': 1,
            'description': 'another'
        }]
    }]
    assert (connector.call_counter_add_test_step == 1)
    assert (connector.call_counter_remove_test_step == 0)
    assert (connector.test_cases == expected)


def test_update_test_steps_removed():
    old_test_cases: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }, {
            'id': 1,
            'description': 'another'
        }]
    }]
    new_steps: List[str] = ['step']
    connector: MockAPIConnector = MockAPIConnector(old_test_cases.copy())

    RobotParser(connector).update_test_steps('1', new_steps, old_test_cases[0]['testSteps'].copy())

    expected: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }]
    }]
    assert (connector.call_counter_add_test_step == 0)
    assert (connector.call_counter_remove_test_step == 1)
    assert (connector.test_cases == expected)


def test_update_test_steps_replaced():
    old_test_cases: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }, {
            'id': 1,
            'description': 'another'
        }]
    }]
    new_steps: List[str] = ['step', 'creative']
    connector: MockAPIConnector = MockAPIConnector(old_test_cases.copy())

    RobotParser(connector).update_test_steps('1', new_steps, old_test_cases[0]['testSteps'].copy())

    expected: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }, {
            'id': 1,
            'description': 'creative'
        }]
    }]
    assert (connector.call_counter_add_test_step == 1)
    assert (connector.call_counter_remove_test_step == 1)
    assert (connector.test_cases == expected)


def test_update_test_steps_reordered():
    old_test_cases: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'step'
        }, {
            'id': 1,
            'description': 'another'
        }]
    }]
    new_steps: List[str] = ['another', 'step']
    connector: MockAPIConnector = MockAPIConnector(old_test_cases.copy())

    RobotParser(connector).update_test_steps('1', new_steps, old_test_cases[0]['testSteps'].copy())

    expected: List[dict] = [{
        'id': 1,
        'name': 'Some test',
        'externalId': 'Some test',
        'testSteps': [{
            'id': 0,
            'description': 'another'
        }, {
            'id': 1,
            'description': 'step'
        }]
    }]
    assert (connector.call_counter_add_test_step == 2)
    assert (connector.call_counter_remove_test_step == 2)
    assert (connector.test_cases == expected)
