from tbcs_client import APIConnector
from test_case_import import RobotParser

def test_get_tests():
    print()
    connector = APIConnector()
    RobotParser(connector).import_tests('/home/jjjmeter/work/examples')
