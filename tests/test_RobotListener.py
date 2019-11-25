import hashlib
from . import MockAPIConnector
from robot_listener import RobotListener
from robot.api import TestSuiteBuilder


def test_listener():
    connector: MockAPIConnector = MockAPIConnector()
    listener: RobotListener = RobotListener('../tbcs.config.json')
    listener.set_connector(connector)
    suite = TestSuiteBuilder().build('../robot_examples/toplevel.robot')

    suite.run(listener=listener)
    assert(connector.call_counter_create_test_case == 1)
    assert(connector.call_counter_get_test_case_by_external_id == 2)
    assert(connector.call_counter_report_step_result == 1)
    assert(connector.call_counter_report_test_case_result == 1)
    assert(connector.call_counter_start_execution == 1)
    assert(connector.test_cases == [{
        'id': 0,
        'name': 'Example test',
        'testCaseType': connector.test_case_type_structured,
        'externalId': hashlib.sha256(('Example test' + 'toplevel.robot').encode('utf-8')).hexdigest(),
        'testSteps': [{
            'id': 0,
            'description': 'Should Be Equal'
        }],
        'executions': [{
            'id': 0,
            'result': 'Passed',
            'testSequence': {
                'testStepBlocks': [{}, {}, {
                    'steps': [{
                        'id': 0,
                        'description': 'Should Be Equal',
                        'result': 'Passed'
                    }]
                }]
            }
        }]
    }])
