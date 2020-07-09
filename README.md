# Robot Framework Integration for TestBench CS
## Preconditions:
Python (with pip) version 3 installed and running.
Robot Framework Version 3.2.1 installed and running.
...
REMARK: This Wrapper will NOT work with older versions of Robot Framework (and its older API)
...

## How to install:
The wrapper will be currently installed from test.pypi.org
You should install it with adminstrator role because if you do not PATH may not be set correct.

CMD: `pip install --extra-index-url https://test.pypi.org/simple/ tbcs-rf-wrapper`

## Importings Robot tests into TestBench CS:
To import Robots Tests into an instance of TestBench CS you need to hand a JSON config file over to the parser.
The config file needs to have the following fields:
```
{
  "server_address": <my.testbench.instance: String>,                        # e.g. "trynow01-eu.testbench.com"
  "tenant_name": <my.tenant: String>,                                       # e.g. "demouser_xy"
  "product_id": <my.product.id: Int>,                                       # e.g. 3
  "tenant_user": <my.user: String>,                                         # e.g. "demouser_xy"
  "password": <my.password: String>,                                        # e.g. "123456"
  "use_system_proxy": <use.proxy: Boolean>,                                 # e.g. true ## must be false if a proxy is set in your system which must be ignored
  "truststore_path": <my.truststore: String>                                # e.g. "/usr/lib/python3/dist-packages/certifi/cacert.pem" ## is igrnoed whe nused with windows 10, the value must be available
}
```
You need to hand the directory where the testcases are, that should be imported, over to the parser. The parser exports all tests including test steps from all .robot files in the given directory and all subdirectories.

When installed correct tests could be imported into TestBench CS with the following command:

CMD: `robot-parser <path.to.json.config> <path.to.dir.containing.robot.tests>`

## Reporting test results:
To import test results from one or multiple robot tests into TestBench CS a specific listener is applied. As with other listeners the listener class must be handed over a a parameter when the tests are started. Further on the path to the (or one) JSON config file must also be handed over to the listener like this:

CMD: `robot --listener <path.to.listener.class>:"<path.to.json.config>" <path.to.dir.containing.robot.tests>`

If the module was installed globally the command could look like this using linux:

CMD: `robot --listener /usr/local/lib/python3.6/dist-packages/robot_listener/RobotListener.py:"tbcs.config.json" myTests/`

**REMARK:** When using windows systems the path to the listener should always use '/', and NOT '\\'.

CMD: `robot --listener C:/temp/RobotListener.py:"C:/temp/tbcs.config.json" C:\temp\myTests\`


When needed the install path for the listener can be found using python shell (for example with Ubuntu):
```
user@host:/# python3
Python 3.6.8 (default, Jan 14 2019, 11:02:34) 
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from robot_listener import RobotListener
>>> import sys, os
>>> os.path.abspath(sys.modules[RobotListener.__module__].__file__)
'/usr/local/lib/python3.6/dist-packages/robot_listener/RobotListener.py'
```