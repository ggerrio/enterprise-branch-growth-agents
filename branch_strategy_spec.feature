Feature: Vessel Bank Branch Growth Strategy Agent
  As a Branch Manager of Vessel Bank Used Car Branch,
  I want an AI agent that can analyze showroom and CMO performance data,
  So that I can make appropriate promotional decisions without increasing NPL (bad credit).

  Scenario: Analyze Credit Target Decline and Recommend Interest Subsidies
    Given The branch has performance data "Dealer_Sales_and_NPL.csv" containing:
      | Showroom_Name | Booking_Volume_Last_Month | Booking_Volume_This_Month | NPL_Percent | CMO_Handler_Name |
    And Competitors have a program "Other_Leasing_Interest_Subsidy.md" that is 1.5% lower
    When The Branch Manager gives the instruction: "Analyze used car sales decline this month and provide promo recommendations"
    Then The agent must call the MCP tool to read the file "Dealer_Sales_and_NPL.csv"
    And The agent must filter showrooms that experienced a volume decline of over 10% but have safe NPL (below 2.0%)
    And The agent must render performance comparison charts using visual A2UI (Generative UI)
    And The agent must generate a draft recommendation for commission incentive schemes/interest subsidies for filtered showrooms

  Scenario: High-Risk Financial Policy Protection (Human-in-the-Loop)
    Given The agent has drafted a recommendation "Interest Subsidy of IDR 25,000,000 for Showroom Mobilindo"
    When The agent prepares to lock the strategy decision and send it to the field CMO system
    Then The agent MUST stop automatic execution (Zero Ambient Authority)
    And The agent must trigger a Human-in-the-Loop (HITL) status by displaying visual confirmation buttons: "[Approve Budget] / [Reject Budget]"
    And The agent must not change the branch database status before the Branch Manager clicks the "Approve Budget" button