Feature: User check orders

    Scenario: user select a product and pay11
        Given the user is logged in and brought something
        When the user click Orders button
        Then the user can see the orders