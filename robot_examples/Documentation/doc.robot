*** Settings ***
#Suite Setup    Should Be Equal    1    1
Test Setup    Should Be Equal    20    20
Test Teardown    Should Be Equal    40    40
#Suite Teardown    Should Be Equal    5    5

*** Test Cases ***
Setup Teardown Fixing 3
    [Setup]    Should Be Equal    2    2
    Should Be Equal    3    3 
    [Teardown]    Should Be Equal    4    4

