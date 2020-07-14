*** Settings ***
Suite Setup    SuiteSetupText    #das Setup und der Teardown sind nur einmal erlaubt!
Test Setup    TestSetup in der Suite
Test Teardown    TestTeardown in der Suite
Suite Teardown    der Satz richtig angezeigt wird

*** Test Cases ***
_Description Anpassung
    [Setup]    TestCaseSetup!!!!Like a boasdfss    #das Setup und der Teardown sind nur einmal erlaubt!
    [Documentation]    Das hier soll geändert werden; hat funktioniert!2!asdf
    Mein Keyword
    Apfel
    Muss
    [Teardown]    TestCaseTeardownText

New Test
    Dein Keyword

Warum geht das nicht??
    [Documentation]    Doku Dako
    Komisch
    Nochmal
    Und nochmal

Also gehen neue Tests doch
    Oder?

Wenn es, nur einen Test gibt
    [Setup]    Hör auf sein Lied
    Ich hoffe, du kannt es hörn

Bist mir so vertraut
    [Setup]    Obwohl ich dich nie
    getestet hab
    [Teardown]    Kennst meinen Teardown 

Nun sollte
    [Setup]    Der Teardown
    richtig rum
    [Teardown]    sein, sodass

*** Keywords ***
Mein Keyword
    Should Be Equal    5    5