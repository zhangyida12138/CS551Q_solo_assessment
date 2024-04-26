Feature: admin view orders

    Scenario: admin view a order1
        Given the user is logged in1 
        When the user clicks view detail button
        Then the user can see the details 