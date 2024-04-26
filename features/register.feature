Feature: User register

    Scenario: user enter website and register successfully
        Given the user is on Home page1
        When the user click Register
        When the user inputs email
        When the user sets password
        When the user input password agian
        When the user clicks the Register button
        Then the user can logout