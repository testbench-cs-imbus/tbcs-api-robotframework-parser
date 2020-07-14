*** Settings ***
Suite Setup    Should Be Equal    1    1
#Suite Teardown    Should Be Equal    6    6

*** Test Cases ***
Funktionierender Test
    [Documentation]    Ein funktionierender TEst
    #[Setup]    Should Be Equal    2    2
    Should Be Equal    3    4
    #[Teardown]    Should Be Equal    4    4