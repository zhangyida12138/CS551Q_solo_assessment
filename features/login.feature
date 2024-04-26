Feature: User Login

    Scenario: user enter website and login successfully
        Given the user is on Home page
        When the user click Login
        When the user input email
        When the user input password
        When the user clicks the Login button
        Then the user can see logout