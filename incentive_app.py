"""
Streamlit application for Gujarat Terce Laboratories incentive calculations.

This app mirrors the calculation logic provided in various incentive circulars
for the fiscal year 2025‑26. It covers calculators for:

1. Hyterce dual opportunity incentive (Syrup and Drops)
2. MR (Medical Representative) annual incentive
3. MR volume incentive (quarterly and annual)
4. MR annual Eminent 11 brand incentive
5. MR quarterly brand‑specific incentive
6. ASM (Area Sales Manager) incentive
7. RSM/BM (Regional/Business Manager) incentive
8. ZBM (Zonal Business Manager) incentive
9. Resplash Super 30 incentive (precision growth and excellence)

To run this app locally you need streamlit installed. You can install it via:

    pip install streamlit

and then execute:

    streamlit run incentive_app.py

The app is designed for ease of use: each section appears in an expandable
accordion. Enter the required values and the incentive will be calculated
immediately. All calculations follow the slabs, multipliers and flat
amounts specified in the official incentive circulars. Where special
eligibility requirements exist (e.g. minimum percentage of team members
earning incentives), the app highlights them.

Author: OpenAI ChatGPT
"""

import streamlit as st

# Define concise terms & conditions for each incentive calculator. These
# summaries mirror the key points from the official circulars and are
# displayed at the bottom of each calculator.
TERMS = {
    "hyterce": [
        "Plan effective Jun–Aug 2025; only Medical Representatives are eligible.",
        "Incentive based on primary PCPM units; separate slabs for Syrup and Drops.",
        "Secondary sales Jun–Sep must be ≥90 % of Jun–Aug primary; Sep primary ≥70 % of PCPM; returns within 6 months reduce incentive."
    ],
    "mr_annual": [
        "PCPM uses FY 2025‑26 net primary sale after expiry deduction.",
        "Gross salary as on 31‑Dec‑2025 is considered for multiplier.",
        "Doctor coverage must remain >90 % for two‑thirds of the tenure; decimals like 104.96 % do not qualify."
    ],
    "mr_volume": [
        "HQ unit growth must exceed 4 % and value growth 7 % to qualify.",
        "Eminent 11 brand achievement must exceed 85 % for quarterly and annual incentives.",
        "To claim quarterly incentives, ≥85 % of target must be achieved in the following month; the 4th quarter requires Apr‑26 sales ≥85 % of FY 2025‑26 average."
    ],
    "mr_brand": [
        "Based on annual achievement of Eminent 11 brand groups.",
        "Brand group count depends on product families with 100 % target achievement.",
        "Degrowth versus FY 2024‑25 disqualifies the incentive; free goods are excluded."
    ],
    "mr_quarterly_brand": [
        "Applies only to Acolate, Tynol, Vitfol and DFS brands.",
        "Brand group PCPM must exceed 10 000 units irrespective of percentage achievement.",
        "Brand growth should be >7 % value and >4 % unit; HQ achievement must exceed 95 %; subsequent month achievement ≥75 % of the quarter average."
    ],
    "ASM": [
        "Manager incentive derived from MR incentives; at least 60 % of MRs must earn incentives.",
        "Achievement of 95–99.99 % yields 1× average MR incentive; >100 % yields 1.5×.",
        "Secondary sales should be ≥90 % of net primary sales; team doctor coverage ≥85 %."
    ],
    "RSM/BM": [
        "Manager incentive derived from MR incentives; at least 50 % of MRs must earn incentives.",
        "Achievement of 95–99.99 % yields 1× average MR incentive; >100 % yields 1.3×.",
        "Secondary sales should be ≥90 % of net primary sales; other general conditions apply."
    ],
    "ZBM": [
        "Manager incentive derived from MR incentives; at least 40 % of MRs must earn incentives.",
        "Achievement of 95–99.99 % yields 1× average MR incentive; >100 % yields 1.2×.",
        "Secondary sales should be ≥90 % of net primary sales; other general conditions apply."
    ],
    "resplash": [
        "Plan effective 01 Mar 2025 to 30 Jun 2025; incremental units only.",
        "Minimum 1 500 incremental units required for precision incentive; 7 500 for excellence (top 3 achievers).",
        "Secondary sales (Mar–Jun 25) must be ≥85 % of primary; July sales ≥70 % of Mar–Jun average; HQ must achieve ≥95 % of target."
    ],
}


def hyterce_calculator():
    st.header("Hyterce: Dual Opportunity Incentive")
    product = st.selectbox(
        "Select Product", ["", "Syrup", "Drops"], index=0, key="hyterce_product"
    )
    total_units = st.number_input(
        "Total primary units (Jun–Aug 2025)",
        min_value=0,
        step=1,
        value=0,
        key="hyterce_total_units",
    )
    months = st.number_input(
        "Number of months (default 3)",
        min_value=1,
        max_value=3,
        value=3,
        key="hyterce_months",
    )
    if product:
        pcpm = total_units / months if months else 0
        # Determine slab and per‑unit incentive
        slab = "No Incentive"
        rate = 0
        if pcpm >= 200:
            if pcpm < 400:
                slab = "Slab 1"
            elif pcpm < 600:
                slab = "Slab 2"
            else:
                slab = "Slab 3"
            if product == "Syrup":
                if slab == "Slab 1":
                    rate = 4
                elif slab == "Slab 2":
                    rate = 6
                else:
                    rate = 8
            else:  # Drops
                if slab == "Slab 1":
                    rate = 3
                elif slab == "Slab 2":
                    rate = 4
                else:
                    rate = 5
        incentive = pcpm * rate
        st.write(f"**PCPM:** {pcpm:.2f} units per month")
        st.write(f"**Slab:** {slab}")
        st.write(f"**Per unit incentive:** ₹{rate:.2f}")
        st.write(f"**Total incentive:** ₹{incentive:.2f}")
        st.info(
            "Example: 2100 units of Syrup across three months results in a PCPM of 700. "
            "This falls into Slab 3 with an 8 Rs rate, yielding 700 × 8 = ₹5600."
        )
    else:
        st.write("Please select a product and enter units to calculate the incentive.")
    # Display terms
    if TERMS.get("hyterce"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["hyterce"]:
            st.markdown(f"- {line}")


def mr_annual_incentive():
    st.header("MR Annual Incentive")
    pcpm = st.number_input(
        "PCPM (Lakhs)", min_value=0.0, step=0.01, value=0.0, key="mr_annual_pcpm"
    )
    achievement = st.number_input(
        "Achievement %", min_value=0.0, step=0.1, value=0.0, key="mr_annual_achievement"
    )
    salary = st.number_input(
        "Monthly gross salary (Rs)",
        min_value=0.0,
        step=1000.0,
        value=0.0,
        key="mr_annual_salary",
    )
    group = ""
    if pcpm:
        if pcpm < 1.5:
            group = "Group A"
        elif pcpm < 2.5:
            group = "Group B"
        elif pcpm < 4.0:
            group = "Group C"
        else:
            group = "Group D"
    multiplier = 0
    if achievement >= 110:
        if group == "Group A":
            multiplier = 1
        elif group == "Group B":
            multiplier = 1.1
        elif group == "Group C":
            multiplier = 1.25
        elif group == "Group D":
            multiplier = 1.5
    elif achievement >= 105:
        if group == "Group A":
            multiplier = 0.75
        elif group == "Group B":
            multiplier = 0.8
        elif group == "Group C":
            multiplier = 0.9
        elif group == "Group D":
            multiplier = 1
    incentive = salary * multiplier
    if group:
        st.write(f"**Group:** {group}")
        if multiplier > 0:
            st.write(f"**Multiplier:** {multiplier}× monthly salary")
            st.write(f"**Incentive:** ₹{incentive:,.2f}")
        else:
            st.warning("Achievement below 105% does not qualify for annual incentive.")
    else:
        st.write("Enter PCPM to determine group and incentive.")
    # Display terms
    if TERMS.get("mr_annual"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["mr_annual"]:
            st.markdown(f"- {line}")


def mr_volume_incentive():
    st.header("MR Volume Incentive (Quarterly/Annual)")
    period = st.selectbox(
        "Period",
        ["", "Quarter", "Annual"],
        index=0,
        key="mr_volume_period",
    )
    pcpm = st.number_input(
        "PCPM (Lakhs)", min_value=0.0, step=0.01, value=0.0, key="mr_volume_pcpm"
    )
    achievement = st.number_input(
        "Achievement %", min_value=0.0, step=0.1, value=0.0, key="mr_volume_achievement"
    )
    sale = st.number_input(
        "Net primary sale (Rs)",
        min_value=0.0,
        step=1000.0,
        value=0.0,
        key="mr_volume_sale",
    )
    group = ""
    if pcpm:
        if pcpm < 1.5:
            group = "Group A"
        elif pcpm < 2.5:
            group = "Group B"
        elif pcpm < 4.0:
            group = "Group C"
        else:
            group = "Group D"
    rate = 0
    if period and group:
        def lookup_rate(ach, grp):
            # helper function to return rate for quarter/annual
            if ach >= 110:
                return {
                    "Group A": 0.75,
                    "Group B": 0.90,
                    "Group C": 1.00,
                    "Group D": 1.20,
                }[grp]
            elif ach >= 105:
                return {
                    "Group A": 0.62,
                    "Group B": 0.70,
                    "Group C": 0.87,
                    "Group D": 1.00,
                }[grp]
            elif ach >= 100:
                return {
                    "Group A": 0.50,
                    "Group B": 0.60,
                    "Group C": 0.75,
                    "Group D": 0.80,
                }[grp]
            elif ach >= 95:
                return {
                    "Group A": 0.25,
                    "Group B": 0.30,
                    "Group C": 0.35,
                    "Group D": 0.40,
                }[grp]
            else:
                return 0
        rate = lookup_rate(achievement, group)
        incentive = sale * rate / 100
        st.write(f"**Group:** {group}")
        if rate > 0:
            st.write(f"**Rate:** {rate}% of net primary sale")
            st.write(f"**Incentive:** ₹{incentive:,.2f}")
        else:
            st.warning("Achievement below 95% does not qualify for volume incentive.")
    else:
        st.write("Select period and enter PCPM to determine incentive.")
    # Display terms
    if TERMS.get("mr_volume"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["mr_volume"]:
            st.markdown(f"- {line}")


def mr_brand_incentive():
    st.header("MR Eminent 11 Brand Incentive")
    pcpm = st.number_input(
        "Annual PCPM (Lakhs)", min_value=0.0, step=0.01, value=0.0, key="mr_brand_pcpm"
    )
    num_groups = st.number_input(
        "Number of brand groups achieving 100% target",
        min_value=1,
        max_value=11,
        step=1,
        value=1,
        key="mr_brand_groups",
    )
    group = ""
    if pcpm:
        if pcpm < 1.5:
            group = "Group A"
        elif pcpm < 2.5:
            group = "Group B"
        elif pcpm < 4.0:
            group = "Group C"
        else:
            group = "Group D"
    # Flat amounts table
    amounts = {
        "Group A": [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000],
        "Group B": [0, 1500, 3000, 4500, 6000, 7500, 9000, 10500, 12000, 13500, 15000, 16500],
        "Group C": [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 22000],
        "Group D": [0, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 22500, 25000, 27500],
    }
    incentive = 0
    if group:
        index = int(num_groups)
        incentive = amounts[group][index]
        st.write(f"**Group:** {group}")
        st.write(f"**Flat incentive:** ₹{incentive:,}")
        st.info(
            "Brand groups are counted based on product families where 100% of target is achieved."
        )
    else:
        st.write("Enter PCPM to determine group and incentive.")
    # Display terms
    if TERMS.get("mr_brand"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["mr_brand"]:
            st.markdown(f"- {line}")


def mr_quarterly_brand_incentive():
    st.header("MR Quarterly Brand‑Specific Incentive")
    pcpm = st.number_input(
        "PCPM for the quarter (Lakhs)",
        min_value=0.0,
        step=0.01,
        value=0.0,
        key="mr_qb_pcpm",
    )
    num_brands = st.number_input(
        "Number of brands achieving 100% target",
        min_value=1,
        max_value=4,
        step=1,
        value=1,
        key="mr_qb_brands",
    )
    group = ""
    if pcpm:
        if pcpm < 1.5:
            group = "Group A"
        elif pcpm < 2.5:
            group = "Group B"
        elif pcpm < 4.0:
            group = "Group C"
        else:
            group = "Group D"
    amounts = {
        "Group A": [0, 500, 1000, 1500, 2000],
        "Group B": [0, 750, 1500, 2250, 3000],
        "Group C": [0, 1000, 2000, 3000, 4000],
        "Group D": [0, 1500, 3000, 4500, 6000],
    }
    if group:
        incentive = amounts[group][int(num_brands)]
        st.write(f"**Group:** {group}")
        st.write(f"**Flat incentive:** ₹{incentive:,}")
        st.info(
            "Only the brands Acolate, Tynol, Vitfol and DFS are considered for the quarterly brand‑specific incentive."
        )
    else:
        st.write("Enter PCPM to determine group and incentive.")
    # Display terms
    if TERMS.get("mr_quarterly_brand"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["mr_quarterly_brand"]:
            st.markdown(f"- {line}")


def manager_incentive(role_name, threshold, high_multiplier):
    """Generic calculator for ASM, RSM/BM and ZBM roles."""
    st.header(f"{role_name} Incentive")
    # Generate unique keys based on role name to avoid duplicate element IDs
    key_base = role_name.replace("/", "_").replace(" ", "_")
    achievement = st.number_input(
        "Achievement %",
        min_value=0.0,
        step=0.1,
        value=0.0,
        key=f"{key_base}_achievement",
    )
    total_mr_incentive = st.number_input(
        "Total MR incentive amount (Rs)",
        min_value=0.0,
        step=1000.0,
        value=0.0,
        key=f"{key_base}_total",
    )
    num_mrs = st.number_input(
        "Number of MRs in team",
        min_value=1,
        step=1,
        value=1,
        key=f"{key_base}_count",
    )
    pct_mrs = st.number_input(
        "Percentage of MRs earning incentives (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        value=0.0,
        key=f"{key_base}_pct",
    )
    eligible = pct_mrs >= threshold
    multiplier = 0
    if eligible:
        if achievement >= 100:
            multiplier = high_multiplier
        elif achievement >= 95:
            multiplier = 1
    incentive = 0
    if multiplier > 0:
        average_mr_incentive = total_mr_incentive / num_mrs if num_mrs else 0
        incentive = average_mr_incentive * multiplier
    st.write(f"**Eligible?** {'Yes' if eligible else 'No'} (requires ≥{threshold}% MRs with incentives)")
    if eligible:
        st.write(f"**Multiplier:** {multiplier}× average MR incentive")
        st.write(f"**Average MR incentive:** ₹{(total_mr_incentive/num_mrs):,.2f}")
        st.write(f"**{role_name} incentive:** ₹{incentive:,.2f}")
    else:
        st.warning(
            f"Eligibility not met: at least {threshold}% of team MRs must earn incentives."
        )
    # Terms for manager roles
    role_key = role_name
    if TERMS.get(role_key):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS[role_key]:
            st.markdown(f"- {line}")


def resplash_incentive():
    st.header("Resplash Super 30 Incentive")
    base_units = st.number_input(
        "Base sale units (Mar–Jun 2024)",
        min_value=0,
        step=1,
        value=0,
        key="resplash_base_units",
    )
    current_units = st.number_input(
        "Sale units (Mar–Jun 2025)",
        min_value=0,
        step=1,
        value=0,
        key="resplash_current_units",
    )
    incremental_units = current_units - base_units if current_units > base_units else 0
    if incremental_units > 0:
        if incremental_units < 1500:
            slab = "No Incentive"
            rate = 0
        elif incremental_units < 3000:
            slab = "Aspire"
            rate = 0.75
        elif incremental_units < 4500:
            slab = "Eminence"
            rate = 1.00
        elif incremental_units < 6000:
            slab = "Pinnacle"
            rate = 1.25
        else:
            slab = "Summit"
            rate = 1.50
        precision_incentive = incremental_units * rate
        excellence_eligible = incremental_units >= 7500
        st.write(f"**Incremental units:** {incremental_units}")
        st.write(f"**Slab:** {slab}")
        st.write(f"**Per‑unit rate:** ₹{rate:.2f}")
        st.write(f"**Precision incentive:** ₹{precision_incentive:,.2f}")
        st.write(
            f"**Eligible for excellence?** {'Yes' if excellence_eligible else 'No'}"
        )
        if excellence_eligible:
            st.success(
                "You meet the minimum 7,500 incremental units requirement for the "
                "Excellence incentive. Final rewards are reserved for the top 3 achievers."
            )
        else:
            st.info(
                "Reach at least 7,500 incremental units to qualify for the Excellence incentive."
            )
    else:
        st.write(
            "Incremental units must exceed zero. Enter your base and current units to calculate."
        )
    # Display terms
    if TERMS.get("resplash"):
        st.markdown("\n**Terms & Conditions**")
        for line in TERMS["resplash"]:
            st.markdown(f"- {line}")


def main():
    st.title("Gujarat Terce Incentive Calculators (FY 2025–26)")
    st.write(
        "Use the sections below to compute different types of incentives. The app "
        "closely follows the official circulars."
    )
    # Expandable sections for each calculator
    with st.expander("Hyterce Dual Opportunity Incentive"):
        hyterce_calculator()
    with st.expander("MR Annual Incentive"):
        mr_annual_incentive()
    with st.expander("MR Volume Incentive (Qtr/Annual)"):
        mr_volume_incentive()
    with st.expander("MR Eminent 11 Brand Incentive"):
        mr_brand_incentive()
    with st.expander("MR Quarterly Brand‑Specific Incentive"):
        mr_quarterly_brand_incentive()
    with st.expander("ASM Incentive"):
        manager_incentive("ASM", threshold=60, high_multiplier=1.5)
    with st.expander("RSM/BM Incentive"):
        manager_incentive("RSM/BM", threshold=50, high_multiplier=1.3)
    with st.expander("ZBM Incentive"):
        manager_incentive("ZBM", threshold=40, high_multiplier=1.2)
    with st.expander("Resplash Super 30 Incentive"):
        resplash_incentive()


if __name__ == "__main__":
    main()