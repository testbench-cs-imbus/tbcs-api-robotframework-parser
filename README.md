# Robot Framework Integration for TestBench CS
## Preconditions:
Python (with pip) version 3 installed and running.
Robot Framework Version 3.2.x installed and running.


Note: This wrapper has been tested with Version 3.2.1 and 3.2.2 of Robot Framework.
It will not run with older versions of Robot Framework.
It may run with Versions 3.2.x of Robot Framework that will be released in the future but we did not test this.

This wrapper will be tested for running with Version 4.0.* of Robot Framework as soon as we find it used in one of our Projects.

## How to install:
The wrapper will currently be installed from test.pypi.org
You should install it with adminstrator role or PATH may not be set correct.

CMD: `pip install --extra-index-url https://test.pypi.org/simple/ tbcs-rf-wrapper`


Note: On some versions of Ubuntu there exists a bug that prevents pip from using the extra-index-url.
If you get the error message `Client Error: Not Found for url: https://pypi.org/simple/tbcs-rf-wrapper/`
you need to install the dependencies manually and use index-url instead:

CMD: `pip install requests`

CMD: `pip install robotframework`

CMD: `pip install --index-url https://test.pypi.org/simple/ tbcs-rf-wrapper`


## How to configure:
The wrapper uses Robot Frameworks listener API and requires a JSON file for configuration.
The config file has to have the following fields:
```
{
  "server_address": <my.testbench.instance: String>,                        # e.g. "cloud01-eu.testbench.com"
  "tenant_name": <my.tenant: String>,                                       # e.g. "demouser_xy"
  "product_id": <my.product.id: Int>,                                       # e.g. 3
  "tenant_user": <my.user: String>,                                         # e.g. "demouser_xy"
  "password": <my.password: String>,                                        # e.g. "123456"
  "use_system_proxy": <use.proxy: Boolean>,                                 # e.g. true ## must be false if there is a proxy configured for your system that must be ignored
  "truststore_path": <my.truststore: String>                                # e.g. "/usr/lib/python3/dist-packages/certifi/cacert.pem" ## value is ignored when used with windows 10, but field has to be available anyway
}
```

## Reporting test results:
To import tests and test results from one or multiple robot tests into TestBench CS a specific listener is applied. As with other listeners the listener class must be handed over a a parameter when the tests are started. Further on you have to navigate to the path where the config.json is in to hand the file over to the listener. Execute Robot Framework like this:

CMD: `robot --listener <path.to.listener.class>:<name.of.the.config.json> <path.to.dir.containing.robot.tests>`

If the module was installed globally the command could look like this using Ubuntu:

CMD: `robot --listener /usr/local/lib/python3.6/dist-packages/robot_listener/RobotListener.py:config.json myTests/`


When needed, the install path for the listener can be found using python shell - for example with Ubuntu:
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

## Known issues:
### Line Continuation
New lines continued by '...' are set as new test steps