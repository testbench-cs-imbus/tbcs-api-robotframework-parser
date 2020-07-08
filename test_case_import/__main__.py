""" Executing this script will import a set of robot tests into TestBench CS

Running this as a script requires two command line arguments:
1. Path to APIConnector configuration <tbcs.config.json> (can be either relative or absolute)
2. Path to directory containing robot files (can be either relative or absolute)

When executed this will import all tests from all robot files in the given directory (2.) and all it's subdirectories
into the TestBench CS instance specified in your configuration file (1.).

The configuration file needs to be in json format with the following structure:
    {
      "server_address": <testbench.cs.address: str>,
      "tenant_name": <my.tenant: str>,
      "product_id": <target.product.id: int>,
      "tenant_user": <my.tenant.user: str>,
      "password": <my.tenant.user.password: str>,
      "use_system_proxy": <use.system.proxy.settings: bool>
    }
"""


import sys
from tbcs_client import APIConnector
from test_case_import import RobotParser

import ast
import astpretty
from robot.api import get_model


def main() -> int:
    if len(sys.argv) < 3:
        return 1
    else:
        print("Initialising parser...")
        connector: APIConnector = APIConnector(sys.argv[1])
        parser: RobotParser = RobotParser(connector)
        print("Parsing robot files...")
        parser.import_tests_from_directory(sys.argv[2])
        print("Parsing completed")
        return 0
    
if __name__ == '__main__':
    sys.exit(main())