#as seen in https://robot-framework.readthedocs.io/en/v3.2.1/autodoc/robot.parsing.html#module-robot.parsing

*** Test Cases ***
11ExampleTestCase
    OwnKeyword 1    argument
    Own Keyword 2

Second example
    OwnKeyword    xxx

*** Keywords ***
OwnKeyword
    [Arguments]    ${arg}
    Log    ${arg}