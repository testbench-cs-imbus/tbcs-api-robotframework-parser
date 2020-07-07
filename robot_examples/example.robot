#as seen in https://robot-framework.readthedocs.io/en/v3.2.1/autodoc/robot.parsing.html#module-robot.parsing

*** Test Cases ***
Example
    Keyword    argument

Second example
    Keyword    xxx

*** Keywords ***
Keyword
    [Arguments]    ${arg}
    Log    ${arg}