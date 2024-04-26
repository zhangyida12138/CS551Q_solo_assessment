Feature: admin delete accounts

    Scenario: admin delete a account
        Given the user is logged in 3
        When the user clicks customer list button
        When the user clicks delete button3
        Then the user deleted it 1