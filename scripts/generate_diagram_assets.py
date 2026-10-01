"""
Generate high-resolution visual flowcharts, comparison charts, and process diagrams
for the EcoCast AI White-Theme Presentation Deck.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = "docs/assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling Constants for Clean White Corporate Theme
FONT_FAMILY = 'DejaVu Sans'
COLOR_BG = '#ffffff'
COLOR_TEXT_MAIN = '#0f172a'
COLOR_TEXT_MUTED = '#475569'
COLOR_GREEN = '#16a34a'       # Schneider Green
COLOR_DARK_GREEN = '#15803d'
COLOR_RED = '#dc2626'         # High Inefficiency / Waste
COLOR_SKY = '#0284c7'         # Digital / Tech
COLOR_AMBER = '#d97706'       # Warning / Holding
COLOR_CARD_BG = '#f8fafc'
COLOR_BORDER = '#cbd5e1'

plt.rcParams['font.family'] = FONT_FAMILY
plt.rcParams['axes.edgecolor'] = COLOR_BORDER
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------------------
# 1. PROBLEM FLOWCHART (How MSMEs Currently Waste 9-45% Energy)
# -------------------------------------------------------------------------
def generate_problem_flowchart():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.axis('off')

    steps = [
        {"title": "1. Cold Scrap Loading", "desc": "1.5 MT steel scrap loaded into crucible\nNo ramp optimization", "color": COLOR_SKY, "x": 0.08},
        {"title": "2. Uncontrolled Melting", "desc": "Fixed max power regardless of ToU tariff\nOpen lid leaks 32.7 kWh radiation", "color": COLOR_AMBER, "x": 0.32},
        {"title": "3. Idle Molten Holding", "desc": "Metal ready at 1520°C but crane delayed!\nBurns 140 kW idle (₹22.50 / min wasted)", "color": COLOR_RED, "x": 0.58},
        {"title": "4. Cost & Carbon Penalty", "desc": "SEC hits 850+ kWh/t (vs 625 target)\nFace ₹7,450/t export carbon duty", "color": COLOR_RED, "x": 0.84}
    ]

    for i, s in enumerate(steps):
        # Card box
        box = patches.FancyBboxPatch(
            (s["x"], 0.2), 0.20, 0.6,
            boxstyle="round,pad=0.03,rounding_size=0.04",
            facecolor='#fff1f2' if s["color"] == COLOR_RED else ('#fffbeb' if s["color"] == COLOR_AMBER else '#f0f9ff'),
            edgecolor=s["color"],
            linewidth=2.0
        )
        ax.add_patch(box)

        # Header Title
        ax.text(s["x"] + 0.10, 0.70, s["title"], color=s["color"], fontsize=11, fontweight='bold', ha='center', va='center')
        
        # Description
        ax.text(s["x"] + 0.10, 0.44, s["desc"], color=COLOR_TEXT_MAIN, fontsize=8.5, ha='center', va='center', multialignment='center', linespacing=1.4)

        # Arrow to next step
        if i < len(steps) - 1:
            ax.annotate('', xy=(steps[i+1]["x"] - 0.01, 0.5), xytext=(s["x"] + 0.21, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_TEXT_MUTED, lw=2.5, mutation_scale=15))

    ax.set_title("THE ROOT PROBLEM: The Costly Heuristic Melting Cycle in MSME Foundries", 
                 fontsize=13, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig1_problem_flowchart.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

# -------------------------------------------------------------------------
# 2. SYSTEM ARCHITECTURE FLOWCHART
# -------------------------------------------------------------------------
def generate_architecture_flowchart():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.axis('off')

    cols = [
        {"title": "1. Field Ingestion", "items": ["Schneider PM5350 Meter", "Infrared Pyrometer (Temp)", "Digital Weighbridge (Tonnes)", "Modbus-TCP / RS485 (Port 502)"], "color": COLOR_SKY, "x": 0.08},
        {"title": "2. EcoCast Edge AI Gateway", "items": ["FastAPI Asynchronous Gateway", "Induction Physics & Enthalpy Model", "Holding Guard Loss Counter", "MSEDCL ToU Tariff Optimizer", "Scikit-Learn Trajectory Regressors"], "color": COLOR_GREEN, "x": 0.38},
        {"title": "3. Operator HMI & Compliance", "items": ["Three.js 3D Crucible Digital Twin", "Live SEC vs BEE Target (625 kWh/t)", "Holding Alarm (₹/min Burn Ticker)", "One-Click CA-26 PDF Certificate", "EU CBAM & BEE PAT Audit Ledger"], "color": COLOR_DARK_GREEN, "x": 0.72}
    ]

    widths = [0.24, 0.28, 0.24]
    for i, c in enumerate(cols):
        w = widths[i]
        box = patches.FancyBboxPatch(
            (c["x"], 0.12), w, 0.76,
            boxstyle="round,pad=0.03,rounding_size=0.04",
            facecolor='#f0fdf4' if c["color"] in [COLOR_GREEN, COLOR_DARK_GREEN] else '#f0f9ff',
            edgecolor=c["color"],
            linewidth=2.0
        )
        ax.add_patch(box)

        # Title
        ax.text(c["x"] + w/2, 0.80, c["title"], color=c["color"], fontsize=11, fontweight='bold', ha='center', va='center')
        
        # Bullets
        bullet_text = "\n\n".join([f"• {it}" for it in c["items"]])
        ax.text(c["x"] + 0.02, 0.44, bullet_text, color=COLOR_TEXT_MAIN, fontsize=8.5, ha='left', va='center', multialignment='left', linespacing=1.2)

        # Arrows
        if i < len(cols) - 1:
            next_x = cols[i+1]["x"]
            ax.annotate('', xy=(next_x - 0.01, 0.50), xytext=(c["x"] + w + 0.01, 0.50),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_GREEN, lw=3.0, mutation_scale=16))

    ax.set_title("ECOCAST AI ARCHITECTURE: Edge Hardware to Cloud-Verifiable Audit", 
                 fontsize=13, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig2_solution_architecture.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

# -------------------------------------------------------------------------
# 3. 4-STEP OPERATOR JOURNEY
# -------------------------------------------------------------------------
def generate_operator_journey():
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.axis('off')

    stages = [
        {"num": "STEP 1", "title": "Smart Charge & Ramp", "desc": "AI calculates 720 kW optimal\npower ramp to hit target temp\nwith minimum peak surcharge.", "color": COLOR_SKY, "x": 0.06},
        {"num": "STEP 2", "title": "Radiation Guard", "desc": "Digital twin alerts operator\nif insulated lid is left open.\nSaves 32.7 kWh per batch!", "color": COLOR_GREEN, "x": 0.30},
        {"num": "STEP 3", "title": "Holding Elimination", "desc": "At 1520°C, holding watchdog\nflashes live ₹/min loss ticker.\nPrompts immediate pouring.", "color": COLOR_AMBER, "x": 0.54},
        {"num": "STEP 4", "title": "Tap & Digital Seal", "desc": "Crucible tilts & pours.\nAuto-generates Form CA-26\nverified audit certificate.", "color": COLOR_DARK_GREEN, "x": 0.78}
    ]

    for i, st in enumerate(stages):
        box = patches.FancyBboxPatch(
            (st["x"], 0.15), 0.20, 0.70,
            boxstyle="round,pad=0.03,rounding_size=0.04",
            facecolor='#f8fafc',
            edgecolor=st["color"],
            linewidth=2.2
        )
        ax.add_patch(box)

        # Step badge
        ax.text(st["x"] + 0.10, 0.76, st["num"], color=st["color"], fontsize=10, fontweight='bold', ha='center', va='center')
        ax.text(st["x"] + 0.10, 0.64, st["title"], color=COLOR_TEXT_MAIN, fontsize=10.5, fontweight='bold', ha='center', va='center')
        ax.text(st["x"] + 0.10, 0.38, st["desc"], color=COLOR_TEXT_MUTED, fontsize=8.5, ha='center', va='center', multialignment='center', linespacing=1.3)

        if i < len(stages) - 1:
            ax.annotate('', xy=(stages[i+1]["x"] - 0.01, 0.50), xytext=(st["x"] + 0.21, 0.50),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_TEXT_MUTED, lw=2.0, mutation_scale=12))

    ax.set_title("OPERATOR USER JOURNEY: Guided Decision-Making at the Furnace Pulpit", 
                 fontsize=13, fontweight='bold', color=COLOR_TEXT_MAIN, pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig3_operator_journey.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

# -------------------------------------------------------------------------
# 4. TIME OF USE TARIFF & HOLDING COST CURVE
# -------------------------------------------------------------------------
def generate_tou_holding_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)

    # 1. 24-Hour Tariff Curve
    hours = np.arange(24)
    # 22-06: 7.00, 06-18: 8.50, 18-22: 10.00
    tariffs = []
    for h in hours:
        if h >= 22 or h < 6:
            tariffs.append(7.00)
        elif 18 <= h < 22:
            tariffs.append(10.00)
        else:
            tariffs.append(8.50)

    colors_list = ['#16a34a' if (h >= 22 or h < 6) else ('#dc2626' if 18 <= h < 22 else '#0284c7') for h in hours]
    bars = ax1.bar(hours, tariffs, color=colors_list, width=0.85, edgecolor='none')
    ax1.set_facecolor('#f8fafc')
    ax1.set_ylim(0, 12)
    ax1.set_xlabel("Hour of the Day (00:00 - 23:00)", fontsize=9, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax1.set_ylabel("Tariff Rate (₹ / kWh)", fontsize=9, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax1.set_title("MSEDCL Industrial Time-of-Use Tariffs", fontsize=11, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax1.axhline(8.50, color='#64748b', linestyle='--', linewidth=1, label="Base Rate (₹8.50)")
    ax1.legend(loc='lower left', fontsize=8)

    # Annotations
    ax1.text(3, 7.5, "Off-Peak Night\nRebate (₹7.00)", color='#16a34a', fontsize=8, fontweight='bold', ha='center')
    ax1.text(20, 10.5, "Peak Surcharge\n(₹10.00)", color='#dc2626', fontsize=8, fontweight='bold', ha='center')

    # 2. Cumulative Holding Waste Curve
    hold_mins = np.linspace(0, 60, 61)
    hold_kwh = (135.0 / 60.0) * hold_mins
    cost_inr = hold_kwh * 9.0  # Avg weighted tariff ₹9/kWh

    ax2.set_facecolor('#f8fafc')
    ax2.plot(hold_mins, cost_inr, color=COLOR_RED, linewidth=2.5, label="Cumulative Rupees Lost (₹)")
    ax2.fill_between(hold_mins, 0, cost_inr, color='#fee2e2', alpha=0.6)
    ax2.set_xlabel("Idle Holding Duration (Minutes)", fontsize=9, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax2.set_ylabel("Money Burned Doing Zero Work (₹)", fontsize=9, fontweight='bold', color=COLOR_RED)
    ax2.set_title("Unproductive Molten Holding Cost Leak", fontsize=11, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax2.grid(True, linestyle=':', alpha=0.6)

    # Callout at 45 mins
    ax2.scatter([45], [cost_inr[45]], color=COLOR_RED, s=60, zorder=5)
    ax2.annotate('45 min hold:\n₹911 / batch wasted!\n(101 kWh)', xy=(45, cost_inr[45]), xytext=(15, cost_inr[45] + 150),
                 arrowprops=dict(arrowstyle="->", color=COLOR_RED, lw=1.5),
                 fontsize=8.5, fontweight='bold', color=COLOR_RED, bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec=COLOR_RED, lw=1))

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig4_tou_holding_chart.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

# -------------------------------------------------------------------------
# 5. CBAM CARBON SHIELD BAR CHART
# -------------------------------------------------------------------------
def generate_cbam_comparison_chart():
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor('#f8fafc')

    categories = [
        "Unoptimized MSME\n(850 kWh/t, Old Heuristics)",
        "Kolhapur Cluster Avg\n(780 kWh/t Baseline)",
        "EU CBAM Benchmark\n(Maximum Allowed Level)",
        "EcoCast AI Optimized\n(625 kWh/t BEE Target)"
    ]
    intensities = [2.78, 2.50, 1.50, 0.71]
    bar_colors = [COLOR_RED, '#f97316', '#64748b', COLOR_GREEN]

    bars = ax.bar(categories, intensities, color=bar_colors, width=0.55, edgecolor=COLOR_BORDER, linewidth=1.2)
    ax.axhline(1.50, color=COLOR_RED, linestyle='--', linewidth=1.5, label="EU CBAM Import Penalty Threshold (1.50 tCO2/t)")

    # Values above bars
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.08, f"{h:.2f} t", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_TEXT_MAIN)

    # Annotations
    ax.annotate('Carbon Tariff Liability:\n+₹7,450/t penalty duty', xy=(1, 2.50), xytext=(0.8, 3.1),
                arrowprops=dict(arrowstyle="->", color=COLOR_RED, lw=1.5),
                fontsize=8.5, fontweight='bold', color=COLOR_RED, bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec=COLOR_RED))

    ax.annotate('100% CBAM EXEMPT:\nSave ₹7,450/tonne on EU exports!', xy=(3, 0.71), xytext=(2.6, 1.8),
                arrowprops=dict(arrowstyle="->", color=COLOR_GREEN, lw=1.5),
                fontsize=8.5, fontweight='bold', color=COLOR_GREEN, bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec=COLOR_GREEN))

    ax.set_ylim(0, 3.6)
    ax.set_ylabel("Embodied Carbon Intensity (tCO2 / Tonne Casting)", fontsize=9.5, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax.set_title("EU CBAM Compliance Shield: Protecting Kolhapur's 30% Export Volume", fontsize=12, fontweight='bold', color=COLOR_TEXT_MAIN, pad=12)
    ax.legend(loc='upper right', fontsize=8.5)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig5_cbam_carbon_chart.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

# -------------------------------------------------------------------------
# 6. FINANCIAL ROI WATERFALL (Annual ₹36 Lakhs Savings)
# -------------------------------------------------------------------------
def generate_roi_breakdown():
    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor('#f8fafc')

    items = [
        "Holding Time\nElimination",
        "Time-of-Use\nNight Shift",
        "Crucible Lid\nRadiation Cover",
        "BEE PAT\nESCerts Trading",
        "TOTAL ANNUAL\nSAVINGS"
    ]
    savings_lakhs = [18.4, 9.3, 4.4, 4.0, 36.1]
    bar_colors = [COLOR_GREEN, COLOR_SKY, COLOR_AMBER, '#8b5cf6', COLOR_DARK_GREEN]

    bars = ax.bar(items, savings_lakhs, color=bar_colors, width=0.55, edgecolor=COLOR_BORDER, linewidth=1.2)

    for bar, val in zip(bars, savings_lakhs):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.8, f"₹{val:.1f} Lakhs", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_TEXT_MAIN)

    ax.set_ylim(0, 44)
    ax.set_ylabel("Annual Financial Impact (₹ Lakhs / Year)", fontsize=9.5, fontweight='bold', color=COLOR_TEXT_MAIN)
    ax.set_title("Quantified Annual Savings Breakdown (Typical 2,500 MT Foundry with ₹2.5 Cr Power Bill)", fontsize=11, fontweight='bold', color=COLOR_TEXT_MAIN, pad=12)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    # Payback Callout
    ax.text(4, 25, "Software Payback:\nUNDER 6 MONTHS!\n(Zero Heavy CapEx)", 
            color=COLOR_DARK_GREEN, fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="#ecfdf5", ec=COLOR_GREEN, lw=1.5))

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig6_financial_roi_breakdown.png")
    plt.savefig(path, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print("Generated", path)

if __name__ == "__main__":
    generate_problem_flowchart()
    generate_architecture_flowchart()
    generate_operator_journey()
    generate_tou_holding_chart()
    generate_cbam_comparison_chart()
    generate_roi_breakdown()
    print("All 6 presentation diagrams generated successfully in docs/assets/!")
