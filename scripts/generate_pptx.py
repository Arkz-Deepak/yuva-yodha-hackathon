"""
Automated PowerPoint Presentation Generator for EcoCast AI
Generates an 12-slide presentation deck matching Schneider Electric Yuva Yodha 2026 guidelines.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path="docs/EcoCast_AI_Yuva_Yodha_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette
    BG_COLOR = RGBColor(10, 14, 20)        # #0a0e14 Dark Industrial Slate
    CARD_BG = RGBColor(17, 23, 34)         # #111722 Card Background
    SCHNEIDER_GREEN = RGBColor(61, 205, 88) # #3dcd58 Electric Green
    TEXT_WHITE = RGBColor(241, 245, 249)   # #f1f5f9 Crisp White
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94a3b8 Muted Grey
    ACCENT_SKY = RGBColor(56, 189, 248)    # #38bdf8 Sky Blue
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #f59e0b Amber

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, title_text, category_text="CHALLENGE 4: SMART MANUFACTURING"):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"SCHNEIDER ELECTRIC YUVA YODHA 2026 • {category_text}"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SCHNEIDER_GREEN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide1)

    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SCHNEIDER ELECTRIC YUVA YODHA ENERGY TECH HACKATHON 2026"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = SCHNEIDER_GREEN

    p1 = tf1.add_paragraph()
    p1.text = "EcoCast AI"
    p1.font.size = Pt(48)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_before = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Production-Aware AI Digital Twin & Tariff-Synchronized Melting Optimizer for MSME Foundries"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_SKY
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Challenge 4: Smart Manufacturing — Industrial Energy & Process Efficiency\nBenchmark Context: Kolhapur MSME Foundry Cluster, Maharashtra\nTeam: Deepak R (Team Lead) & Saranya Dutta (IIPE)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(25)

    # Helper function for 2-column cards
    def add_card(slide, left, top, width, height, title, items, border_color=SCHNEIDER_GREEN):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        for item in items:
            p_i = tf.add_paragraph()
            p_i.text = f"• {item}"
            p_i.font.size = Pt(12)
            p_i.font.color.rgb = TEXT_MUTED
            p_i.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide2)
    add_header(slide2, "The Problem: Decision-Level Energy Waste in India's MSME Foundries")

    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), 
             "Kolhapur Cluster Baseline", [
                 "300+ MSME units producing 600,000 tonnes of automotive castings annually.",
                 "Consumes ~166,910 tonnes of oil equivalent (toe) annually.",
                 "Energy represents 30% to 50% of total manufacturing costs.",
                 "Induction melting furnaces consume over 70% of total plant power.",
                 "Average Specific Energy Consumption (SEC): 780 to 900 kWh/t."
             ])

    add_card(slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), 
             "The 9–45% Decision-Level Waste", [
                 "Unsynchronized Melting: Molten metal at 1520°C idles 20–60 min waiting for ladles, burning 120–150 kWh every idle hour.",
                 "Time-of-Use Blindness: Melting during evening peak surcharge hours (+₹1.50/unit) instead of night off-peak windows (-₹1.50/unit).",
                 "Crucible Radiation Leak: Operating without automated lid covers wastes 32.7 kWh per batch.",
                 "Diagnosis: Not an equipment deficit—an intelligence and decision-support gap."
             ], border_color=ACCENT_AMBER)

    # -------------------------------------------------------------
    # SLIDE 3: Urgency & Regulatory Pressure
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide3)
    add_header(slide3, "Why It Matters Now: Single-Digit Margins & EU CBAM Carbon Tariffs")

    add_card(slide3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Thin Profit Margins (4–8%)", [
                 "Foundry survival depends on unit electricity costs.",
                 "A 10% reduction in power consumption directly doubles foundry operating profit margins.",
                 "Energy bills reach up to 19% of total turnover in typical Kolhapur units.",
                 "Payback periods for operational energy savings are proven to be under 6–12 months."
             ])

    add_card(slide3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "EU CBAM Enforcement (2026 Crisis)", [
                 "Nearly 30% of Kolhapur's castings are exported to EU, US, and Middle East markets.",
                 "Full CBAM implementation began in 2026, penalizing high carbon intensity.",
                 "Indian steel emits ~2.5 tCO2/t versus the EU benchmark of 1.5 tCO2/t.",
                 "Non-compliant exporters face carbon tariffs of €79.68/tCO2 (up to €173/t steel duty).",
                 "Verifiable Scope 2 carbon auditing is now mandatory to protect export revenue."
             ], border_color=ACCENT_SKY)

    # -------------------------------------------------------------
    # SLIDE 4: Alignment with Schneider Electric
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide4)
    add_header(slide4, "Strategic Fit: Extending EcoStruxure to 5,000+ MSME Foundries")

    add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "The Enterprise vs MSME Gap", [
                 "Schneider's EcoStruxure™ Power & Process serves enterprise facilities with multi-crore instrumentation budgets.",
                 "India's 5,000+ MSME manufacturing units cannot afford or absorb heavy enterprise SCADA platforms.",
                 "They have thin capital, yet consume massive electrical loads and desperately require decision intelligence."
             ])

    add_card(slide4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "EcoCast as the 'EcoStruxure Edge MSME Gateway'", [
                 "Non-invasive software layer connecting directly to Schneider EasyLogic™ PM5350 and PowerLogic™ ION meters via Modbus-TCP.",
                 "Turns raw meter telemetry into actionable furnace operational decisions.",
                 "Creates a recurring hardware on-ramp for Schneider smart meters, variable speed drives (Altivar), and edge gateways.",
                 "Directly aligns with SE Ventures' thesis on industrial decarbonization."
             ], border_color=SCHNEIDER_GREEN)

    # -------------------------------------------------------------
    # SLIDE 5: The Proposed Solution
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide5)
    add_header(slide5, "The Proposed Solution: EcoCast AI Overview & Core Innovation")

    add_card(slide5, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "1. 3D Digital Twin", [
                 "Three.js WebGL visualization of crucible thermal gradient.",
                 "Real-time dynamic incandescence based on pyrometer bath temp.",
                 "Visual warning waves when insulated lid is open (+32.7 kW loss).",
                 "Hydraulic tilting animation during metal tapping."
             ])

    add_card(slide5, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "2. Holding Guard & ToU", [
                 "Watchdog detects when metal reaches 1520°C but is held idle.",
                 "Real-time burn ticker: ₹/minute and kg CO2/min wasted.",
                 "MSEDCL tariff optimizer recommends optimal batch start times to hit night rebate window (-₹1.50/unit)."
             ], border_color=ACCENT_AMBER)

    add_card(slide5, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "3. Verified Certification", [
                 "Auto-generates Form CA-26 compliance certificates upon tapping.",
                 "Cryptographic SHA-256 digital stamp for tamper-proof audits.",
                 "Quantifies EU CBAM duty savings in Euros (€) and INR (₹).",
                 "Calculates BEE PAT ESCerts for IEX exchange trading."
             ], border_color=ACCENT_SKY)

    # -------------------------------------------------------------
    # SLIDE 6: Operator User Journey
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide6)
    add_header(slide6, "Operator User Journey: Synchronized Melting from Scrap to Ingot")

    add_card(slide6, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Phase 1: Charge & Ramp", [
                 "1.5 MT scrap loaded.",
                 "AI recommends 3-stage power ramp setpoint (720 kW -> 520 kW -> 640 kW).",
                 "Minimizes peak demand charges and refractory thermal shock."
             ])

    add_card(slide6, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Phase 2: Radiation Guard", [
                 "Bath temperature exceeds 1000°C.",
                 "System alerts if insulated lid is open.",
                 "Preserves 32.7 kWh radiation energy per heat cycle."
             ])

    add_card(slide6, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Phase 3: Holding Guard", [
                 "Bath hits 1520°C tapping temp.",
                 "If crane is delayed, red alarm flashes.",
                 "Live burn rate ticker (₹22.5/min) prompts crew to pour or ramp down."
             ], border_color=ACCENT_AMBER)

    add_card(slide6, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Phase 4: Tap & Certify", [
                 "Crucible tilts and pours.",
                 "Digital weighbridge logs net tonnage.",
                 "Form CA-26 PDF/CSV certificate auto-generated with SHA-256 seal."
             ], border_color=SCHNEIDER_GREEN)

    # -------------------------------------------------------------
    # SLIDE 7: Technical Architecture
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide7)
    add_header(slide7, "Technical Architecture: Edge-Native Industrial IoT Pipeline")

    add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Hardware & Edge Ingestion", [
                 "Schneider EasyLogic™ PM5350 / PowerLogic™ ION meters connected via Modbus-TCP (Port 502).",
                 "Ingests active power (kW), reactive power (kVAR), power factor, and voltage.",
                 "Optical infrared pyrometer feeding 4–20 mA melt bath temperature.",
                 "Runs on edge hardware: Raspberry Pi 4/5, Schneider Harmony iPC, or standard industrial PC."
             ])

    add_card(slide7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Backend Engine & WebSockets", [
                 "FastAPI (Python 3.13) asynchronous gateway.",
                 "WebSockets streaming 1 Hz real-time telemetry packets (/ws/telemetry).",
                 "Thermodynamic physics simulator modeling latent heat of fusion (270 kJ/kg) and convective/radiation losses.",
                 "ReportLab vector engine generating digitally stamped PDF audit certificates."
             ], border_color=ACCENT_SKY)

    # -------------------------------------------------------------
    # SLIDE 8: Machine Learning Engine
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide8)
    add_header(slide8, "Machine Learning Engine: Physics-Informed Predictive Control")

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Dataset & Training Pipeline", [
                 "Calibrated with UCI Steel Industry Energy Dataset (35,040 intervals) and real foundry heat records.",
                 "Features: Scrap mass (kg), initial temp (°C), target temp (°C), power ramp trajectory, lid cover fraction, and ambient temp.",
                 "Models: Scikit-learn RandomForestRegressor and GradientBoostingRegressor pipelines."
             ])

    add_card(slide8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Inference Outputs", [
                 "Estimated Time to Tap (Minutes remaining): Gradient Boosting model predicting completion time within ±2.5 minutes.",
                 "Predicted Specific Energy Consumption (SEC in kWh/t): Random Forest predicting total batch energy consumption.",
                 "Optimal Power Ramp: Recommends multi-stage setpoints to shave peak demand without delaying tap schedule."
             ], border_color=SCHNEIDER_GREEN)

    # -------------------------------------------------------------
    # SLIDE 9: Statutory Compliance (CBAM & BEE PAT)
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide9)
    add_header(slide9, "Statutory Compliance: EU CBAM Carbon Shield & BEE PAT Trading")

    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "EU CBAM Carbon Shield", [
                 "Statutory Equation: Embodied Scope 2 Carbon = SEC x 0.82 kg CO2/kWh (CEA India Baseline).",
                 "Demonstrates total casting carbon intensity of ~0.71 tCO2/t (well below EU 1.50 tCO2/t threshold).",
                 "Shields Kolhapur exporters against €79.68/tCO2 (~₹7,450/t) in European border tariffs.",
                 "Generates export-ready customs verification certificates with SHA-256 cryptographic seals."
             ])

    add_card(slide9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "BEE PAT Scheme Revenue (ESCerts)", [
                 "Complies with India's Energy Conservation Act, 2001 for Designated Consumers.",
                 "Converts verified energy savings into ESCerts (1 ESCert = 1 Mtoe saved).",
                 "Live valuation on the Indian Energy Exchange (IEX) at ~₹2,150 per ESCert.",
                 "Unlocks +₹7.1 Lakhs/year in liquid trading assets for a typical 2,500 MT foundry."
             ], border_color=ACCENT_SKY)

    # -------------------------------------------------------------
    # SLIDE 10: Quantified Impact & ROI
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide10)
    add_header(slide10, "Demonstrable ROI: 6-Month Payback for a Typical MSME Foundry")

    add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Annual Savings Breakdown (2,500 MT/year Foundry)", [
                 "Holding Time Elimination (30 min/heat): Saves 216,000 kWh = ₹18.4 Lakhs/year.",
                 "Time-of-Use Night Tariff Shift (25% load): Saves ₹9.3 Lakhs/year in rebates.",
                 "Lid Automation & Cover Adherence: Saves 52,300 kWh = ₹4.4 Lakhs/year in radiation.",
                 "Total Annual Energy Bill Savings: ₹32 Lakhs to ₹45 Lakhs (12% to 18% reduction).",
                 "Software + Gateway Investment: ~₹1.5 Lakhs (Payback < 6 months)."
             ], border_color=SCHNEIDER_GREEN)

    add_card(slide10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Macro Environmental & Cluster Impact", [
                 "Avoided Carbon Emissions: 350 to 500 tonnes of CO2 per foundry per year.",
                 "Cluster-wide Impact across Kolhapur's 300 units: ₹14 Crore annual savings.",
                 "National Scaling across 5,000 MSME foundries: >150,000 tonnes of avoided CO2 annually.",
                 "Protects international market access against incoming CBAM import duties."
             ], border_color=ACCENT_SKY)

    # -------------------------------------------------------------
    # SLIDE 11: Implementation Roadmap
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide11)
    add_header(slide11, "Implementation Roadmap: From Pilot to Cluster Scale")

    add_card(slide11, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Q1: Pilot Deployment", [
                 "Deploy edge gateways in 3 Kolhapur foundries.",
                 "Calibrate Modbus polling with Schneider PM5350 meters.",
                 "Validate baseline SEC telemetry."
             ])

    add_card(slide11, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Q2: Shopfloor Loop", [
                 "Install mobile HMI tablets on furnace pulpits.",
                 "Implement holding-guard alarms with operator training.",
                 "First CBAM audit exports for EU shipments."
             ])

    add_card(slide11, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Q3: Cluster Rollout", [
                 "Partner with Kolhapur Engineering Association (KEA) & BEE.",
                 "Onboard 50 MSME foundries across Kolhapur & Belgaum.",
                 "Cloud analytics dashboard for multi-furnace plants."
             ], border_color=ACCENT_AMBER)

    add_card(slide11, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Q4: Schneider Ecosystem", [
                 "Publish as certified app on Schneider Electric Exchange.",
                 "Integration with Schneider edge box bundles.",
                 "Expand to Coimbatore, Rajkot, and Belgaum clusters."
             ], border_color=SCHNEIDER_GREEN)

    # -------------------------------------------------------------
    # SLIDE 12: Team & Conclusion
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide12)
    add_header(slide12, "Team & Conclusion: Ready to Power India's Green MSME Transition")

    add_card(slide12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Team Members", [
                 "Deepak R (Team Lead): Systems engineering, edge computing, full-stack architectures, 3D WebGL digital twins, and industrial Modbus/MQTT IoT protocols.",
                 "Saranya Dutta (Team Member): Indian Institute of Petroleum and Energy (IIPE), Roll No: 23CH10028 (saranyadutta@iipe.ac.in). Chemical process engineering, thermodynamic energy balances, SEC benchmarking, and CBAM/BEE compliance modeling."
             ])

    add_card(slide12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "Why EcoCast AI Wins", [
                 "Working Full-Stack Software: Complete FastAPI + Three.js 3D twin running live right now.",
                 "Proven Mathematical Foundation: Built on documented BEE Kolhapur case studies & CEA grid standards.",
                 "Schneider Electric Hardware Synergy: Directly drives Schneider energy meter and drive adoption.",
                 "Verifiable ROI: Sub-6-month payback solving India's most urgent industrial decarbonization challenge."
             ], border_color=SCHNEIDER_GREEN)

    # Save presentation
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}!")

if __name__ == "__main__":
    create_presentation()
