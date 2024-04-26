Feature: admin change password

    Scenario: admin change password
        Given the user is logged in 4
        When the user clicks customer list button2
        When the user enter a new password
        When the user clicks update button
        Then the user changed it6