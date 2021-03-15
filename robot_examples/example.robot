*** Settings ***
Resource    example.resource
Test Setup    Should Be Equal    1    1
Test Teardown    Should Be Equal    2    2

*** Test Cases ***
First Test
    [Documentation]    This test illustrates the documentation and the Setup&Teardown functionality; feel free to comment out pieces of steps here - especially [Setup] and [Teardown].
    [Setup]    Should Be Equal    3    3
    Should Be Equal    4    4
    Should Be Equal    5    5
    Do Something
    [Teardown]    Should Be Equal    6    6