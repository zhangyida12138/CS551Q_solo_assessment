Feature: admin Login

    Scenario: admin enter website and login successfully
        Given the admin is on Home page
        When the admin click Login
        When the admin input email
        When the admin input password
        When the admin clicks the Login button
        Then the admin can see logout