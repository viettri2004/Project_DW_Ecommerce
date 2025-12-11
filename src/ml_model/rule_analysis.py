import pandas as pd
import os

# Set UTF-8 encoding for proper display of Vietnamese characters
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Read data from output_rules file (assumed to be CSV file)
# If your file is Excel, change to pd.read_excel('output_rules.xlsx')
try:
    # Use absolute path to ensure we find the file
    csv_path = os.path.join(os.path.dirname(__file__), 'output_rules.csv')
    rules = pd.read_csv(csv_path)
    print("Successfully loaded data!")
except FileNotFoundError:
    print("Could not find 'output_rules.csv' file. Please check the file name or path.")
    exit()

# Ensure required columns exist
required_columns = ['antecedents', 'consequents', 'support', 'lift']
if not all(col in rules.columns for col in required_columns):
    print(f"File missing required columns: {required_columns}")
else:
    # ---------------------------------------------------------
    # REQUIREMENT 1: Find product pairs with Support > 3% and lowest Lift
    # ---------------------------------------------------------
    
    # Filter rules with Support > 0.03
    high_support_rules = rules[rules['support'] > 0.03]

    if not high_support_rules.empty:
        # Sort by Lift ascending to get lowest Lift
        lowest_lift_rule = high_support_rules.sort_values(by='lift', ascending=True).iloc[0]
        
        print("\n=== SAMPLE PRODUCT PAIR (Support > 3%, Lowest Lift) ===")
        print(f"Product A (Antecedents): {lowest_lift_rule['antecedents']}")
        print(f"Product B (Consequents): {lowest_lift_rule['consequents']}")
        print(f"Support: {lowest_lift_rule['support']:.4f} ({lowest_lift_rule['support']*100:.2f}%)")
        print(f"Lift:    {lowest_lift_rule['lift']:.4f}")
    else:
        print("\nNo rules found with Support > 3%.")

    # ---------------------------------------------------------
    # REQUIREMENT 2: Count number of rules in 3 Lift groups
    # ---------------------------------------------------------
    
    # Group 1: Lift > 20
    count_lift_gt_20 = len(rules[rules['lift'] > 20])
    
    # Group 2: Lift from 10 to 20 (10 <= Lift <= 20)
    count_lift_10_to_20 = len(rules[(rules['lift'] >= 10) & (rules['lift'] <= 20)])
    
    # Group 3: Lift < 10
    count_lift_lt_10 = len(rules[rules['lift'] < 10])
    
    print("\n=== RULE COUNT STATISTICS BY LIFT ===")
    print(f"Lift > 20:       {count_lift_gt_20} rules")
    print(f"Lift 10 - 20:    {count_lift_10_to_20} rules")
    print(f"Lift < 10:       {count_lift_lt_10} rules")
    
    # Total check
    total_checked = count_lift_gt_20 + count_lift_10_to_20 + count_lift_lt_10
    print(f"Total:           {total_checked} / {len(rules)} rules")