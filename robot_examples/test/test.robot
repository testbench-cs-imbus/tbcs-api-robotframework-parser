*** Settings ***
Test Setup    Should Be Equal    1    1
Test Teardown    Should Be Equal    2    3

*** Test Cases ***
First Test
    [Documentation]    This test illustrates the documentation and the Setup&Teardown functionality; feel free to comment out pieces of steps here - especially [Setup] and [Teardown].
    [Setup]    Should Be Equal    3    3
    Should Be Equal    4    3
    Should Be Equal    5    5
    #[Teardown]    Should Be Equal    6    6