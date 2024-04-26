Feature: User buy something

    Scenario: user select a product and pay
        Given the user is on Home page2
        When the user choose a product and click View Product
        When the user click add to cart button
        When the user clicks the Process to Checkout button
        Then the user can see the alter