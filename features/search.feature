Feature: User search something

    Scenario: user searches something and see it
        Given the user is on Home page3
        When the user enter a product name
        When the user click the search button
        Then the user can see the products