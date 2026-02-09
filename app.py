"""
app.py — Streamlit entry point for the Sustainable Resource Management System.

Launch with:
    streamlit run app.py

This file wires the UI to the same business‑logic classes used by main.py,
demonstrating clean separation between core logic and presentation.

Design Choices
──────────────
• White / off-white background with nature-inspired accent colours.
• Each resource has a dedicated colour: blue (water), amber (energy),
  brown-green (waste), reinforcing environmental identity at a glance.
• Cards use soft shadows, rounded corners, and generous spacing for a
  modern dashboard aesthetic similar to smart-city control panels.
• Sidebar is reserved for the single user-action (consume); the main
  canvas is read-only overview — keeps the layout uncluttered.
• All data comes from the OOP model layer; zero business logic here.
"""

from __future__ import annotations

import streamlit as st
from models.resource import WaterResource, EnergyResource, WasteResource
from models.consumer import Consumer


# ══════════════════════════════════════════════════════════════════════════════
# Custom CSS — white theme, nature palette, card system
# ══════════════════════════════════════════════════════════════════════════════
_CUSTOM_CSS = """
<style>
/* ── Global overrides ───────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
    scroll-behavior: smooth;
}

/* Force light background everywhere */
.stApp {
    background: linear-gradient(160deg, #f8faf8 0%, #eef5ee 100%);
    background-attachment: fixed;
}

/* Remove default Streamlit top padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
}

/* ── Keyframe Animations ────────────────────────────────────────────── */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes progressFill {
    from { width: 0%; }
    to { width: 100%; }
}

/* ── Sidebar styling ────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f0f7f0 100%);
    border-right: 2px solid #d4e8d4;
    animation: slideInLeft 0.6s ease-out;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h4 {
    color: #2e7d32;
}

/* ── Card component ─────────────────────────────────────────────────── */
.resource-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.5rem 1.4rem 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 5px solid;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 0.5rem;
    animation: fadeInUp 0.6s ease-out;
    animation-fill-mode: both;
    position: relative;
    overflow: hidden;
}

.resource-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.resource-card:hover::before {
    left: 100%;
}

.resource-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.resource-card.water  { 
    border-left-color: #1976d2;
    animation-delay: 0.1s;
}
.resource-card.energy { 
    border-left-color: #f9a825;
    animation-delay: 0.2s;
}
.resource-card.waste  { 
    border-left-color: #6d4c41;
    animation-delay: 0.3s;
}

.card-icon {
    font-size: 2.4rem;
    margin-bottom: 0.3rem;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
}

.card-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.4rem;
    line-height: 1.3;
}

.card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1b1b1b;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}

.card-sub {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 0.9rem;
    line-height: 1.4;
}

.card-detail {
    font-size: 0.79rem;
    color: #777;
    line-height: 1.5;
}

/* ── Progress bar colours ───────────────────────────────────────────── */
.water-bar  .stProgress > div > div { 
    background: linear-gradient(90deg, #1976d2, #42a5f5) !important;
}
.energy-bar .stProgress > div > div { 
    background: linear-gradient(90deg, #f9a825, #ffc107) !important;
}
.waste-bar  .stProgress > div > div { 
    background: linear-gradient(90deg, #6d4c41, #8d6e63) !important;
}

/* style the progress track */
.stProgress > div {
    background-color: #e8e8e8 !important;
    border-radius: 10px !important;
    height: 12px !important;
    overflow: hidden;
}
.stProgress > div > div {
    border-radius: 10px !important;
    height: 12px !important;
    animation: progressFill 1.5s ease-out;
    transition: all 0.3s ease;
}

/* ── Section headers ────────────────────────────────────────────────── */
.section-header {
    font-size: 1.35rem;
    font-weight: 700;
    color: #2e7d32;
    margin: 2.2rem 0 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    animation: fadeIn 0.8s ease-out;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e0f2e0;
}
.section-header .icon { 
    font-size: 1.4rem;
    animation: pulse 2s ease-in-out infinite;
}

/* ── Hero / Header ──────────────────────────────────────────────────── */
.hero-container {
    background: linear-gradient(135deg, #2e7d32 0%, #43a047 60%, #66bb6a 100%);
    border-radius: 20px;
    padding: 2.5rem 2.8rem;
    margin-bottom: 2rem;
    color: #fff;
    box-shadow: 0 6px 24px rgba(46,125,50,0.28);
    animation: fadeInUp 0.7s ease-out;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 3s ease-in-out infinite;
}

.hero-container h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    color: #ffffff;
    line-height: 1.3;
    position: relative;
    z-index: 1;
}

.hero-container p {
    font-size: 1rem;
    opacity: 0.94;
    margin: 0;
    color: #e8f5e9;
    line-height: 1.5;
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.22);
    border-radius: 25px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 1rem;
    letter-spacing: 0.4px;
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* ── Consumer report cards ──────────────────────────────────────────── */
.consumer-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
    border: 1px solid #e0e8e0;
}

/* ── Mini resource cards in reports ─────────────────────────────────── */
.mini-resource-card {
    background: linear-gradient(135deg, #fafcfa 0%, #f5f9f5 100%);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    border: 1.5px solid #e0e8e0;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.mini-resource-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border-color: #c8e6c9;
}

.mini-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
    display: inline-block;
}

.mini-card-title {
    font-weight: 600;
    color: #333;
    margin: 0.4rem 0 0.3rem;
    font-size: 0.95rem;
}

.mini-card-details {
    font-size: 0.82rem;
    color: #666;
    line-height: 1.6;
}

/* ── Table styling inside expanders ─────────────────────────────────── */
.stTable {
    animation: fadeIn 0.5s ease-out;
}

.stTable table {
    border-radius: 12px;
    overflow: hidden;
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
}

.stTable thead th {
    background: linear-gradient(135deg, #f1f8f1 0%, #e8f5e9 100%) !important;
    color: #2e7d32 !important;
    font-weight: 600;
    font-size: 0.83rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 0.9rem !important;
    border-bottom: 2px solid #c8e6c9 !important;
}

.stTable tbody td {
    font-size: 0.88rem;
    padding: 0.8rem !important;
    border-bottom: 1px solid #f0f0f0 !important;
}

.stTable tbody tr:hover {
    background-color: #f9fdf9 !important;
    transition: background-color 0.2s ease;
}

.stTable tbody tr:last-child td {
    border-bottom: none !important;
}

/* ── Expander styling ───────────────────────────────────────────────── */
details[open] {
    animation: fadeIn 0.3s ease-out;
}

.stExpander {
    border-radius: 12px !important;
    border: 1px solid #e0e8e0 !important;
    background: #ffffff !important;
    margin-bottom: 1rem !important;
    transition: all 0.3s ease;
}

.stExpander:hover {
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

/* ── Metrics styling ────────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #2e7d32 !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #666 !important;
}

/* ── Footer ─────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    color: #999;
    font-size: 0.79rem;
    padding: 2.5rem 0 1rem;
    border-top: 1px solid #e0e0e0;
    margin-top: 3rem;
    line-height: 1.8;
    animation: fadeIn 1s ease-out;
}

/* ── Sidebar button ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.3rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(46,125,50,0.25);
}

section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(46,125,50,0.35);
}

section[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(0);
}

/* ── Alert/Success/Warning boxes ────────────────────────────────────── */
.stAlert {
    animation: fadeInUp 0.4s ease-out !important;
    border-radius: 10px !important;
}

/* ── Info boxes ─────────────────────────────────────────────────────── */
.stInfo {
    background-color: #e8f5e9 !important;
    border-left: 4px solid #43a047 !important;
    animation: fadeIn 0.4s ease-out;
}

/* Hide default Streamlit header / footer */
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* ── Responsive adjustments ─────────────────────────────────────────── */
@media (max-width: 768px) {
    .hero-container {
        padding: 1.8rem 1.5rem;
    }
    .hero-container h1 {
        font-size: 1.5rem;
    }
    .card-value {
        font-size: 1.6rem;
    }
}
</style>
"""

# ── Resource display configuration (icon, css-class, accent) ─────────────────
_RES_CONFIG = {
    "Water": {
        "icon": "💧",
        "css_class": "water",
        "bar_class": "water-bar",
        "accent": "#1976d2",
        "detail_label": "Source",
        "detail_key": "source",
    },
    "Electricity": {
        "icon": "⚡",
        "css_class": "energy",
        "bar_class": "energy-bar",
        "accent": "#f9a825",
        "detail_label": "Type",
        "detail_key": "energy_type",
    },
    "Waste": {
        "icon": "♻️",
        "css_class": "waste",
        "bar_class": "waste-bar",
        "accent": "#6d4c41",
        "detail_label": "Category",
        "detail_key": "waste_category",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Session state initialisation
# ══════════════════════════════════════════════════════════════════════════════
def _init_state() -> None:
    """Seed Streamlit session state with default resources and consumers."""
    if "resources" not in st.session_state:
        st.session_state.resources = {
            "Water": WaterResource(total_available=10_000, source="River"),
            "Electricity": EnergyResource(total_available=5_000, energy_type="Solar"),
            "Waste": WasteResource(total_available=2_000, waste_category="Recyclable"),
        }

    if "consumers" not in st.session_state:
        water = st.session_state.resources["Water"]
        energy = st.session_state.resources["Electricity"]
        waste = st.session_state.resources["Waste"]

        household = Consumer("C-101", "Residential Block A")
        factory = Consumer("C-202", "Textile Factory B")

        for res in (water, energy, waste):
            household.assign_resource(res)
            factory.assign_resource(res)

        st.session_state.consumers = {
            household.name: household,
            factory.name: factory,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Page configuration & injection
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Sustainable Resource Manager",
    page_icon="🌿",
    layout="wide",
)

_init_state()

# Inject custom CSS
st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="hero-container">
        <h1>🌿 Sustainable Resource Management System</h1>
        <p>An OOP-driven dashboard for tracking urban water, energy, and waste usage</p>
        <span class="hero-badge">🏙️ Smart City &nbsp;·&nbsp; ♻️ Sustainability &nbsp;·&nbsp; 📊 Real-Time Analytics</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Consume Resource Action Panel
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h2 style='color: #2e7d32; margin: 0; font-size: 1.4rem;'>🌱 Resource Console</h2>
            <p style='color:#666; font-size:0.85rem; margin: 0.4rem 0 0;'>
                Select a consumer, pick a resource, and enter the amount to consume.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    consumer_name = st.selectbox(
        "👤  Consumer",
        options=list(st.session_state.consumers.keys()),
        help="Choose which urban entity is consuming the resource.",
    )

    resource_name = st.selectbox(
        "📦  Resource",
        options=list(st.session_state.resources.keys()),
        help="Choose the resource to consume from.",
    )

    # Show unit hint based on selected resource
    unit_hints = {"Water": "litres", "Electricity": "kWh", "Waste": "kg"}
    unit = unit_hints.get(resource_name, "units")

    amount = st.number_input(
        f"🔢  Amount ({unit})",
        min_value=0.0,
        step=10.0,
        help=f"Enter the quantity in {unit} to consume.",
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if st.button("🚀  Consume Resource", type="primary", use_container_width=True):
        consumer = st.session_state.consumers[consumer_name]
        resource = st.session_state.resources[resource_name]
        msg = consumer.use_resource(resource, amount)
        if msg.startswith("✔"):
            st.success(msg, icon="✅")
        else:
            st.warning(msg, icon="⚠️")

    st.markdown("---")

    # Quick sidebar summary with better styling
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 0.8rem;'>
            <h4 style='color: #2e7d32; margin: 0; font-size: 1.1rem;'>📈 Quick Stats</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    total_events = sum(
        len(c.consumption_history)
        for c in st.session_state.consumers.values()
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Events", total_events, help="Total consumption transactions")
    with col2:
        st.metric("Consumers", len(st.session_state.consumers), help="Active consumer entities")
    
    st.metric("Resources", len(st.session_state.resources), help="Tracked resource types")


# ══════════════════════════════════════════════════════════════════════════════
# RESOURCE OVERVIEW CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><span class="icon">📊</span> Resource Overview</div>',
    unsafe_allow_html=True,
)

cols = st.columns(3, gap="large")

for idx, (rname, resource) in enumerate(st.session_state.resources.items()):
    report = resource.report_usage()
    cfg = _RES_CONFIG[rname]
    unit_str = report.get("unit", "units")
    detail_val = report.get(cfg["detail_key"], "—")

    with cols[idx]:
        # Card HTML
        st.markdown(
            f"""
            <div class="resource-card {cfg['css_class']}">
                <div class="card-icon">{cfg['icon']}</div>
                <div class="card-title">{report['name']} ({unit_str})</div>
                <div class="card-value">{report['total_available']:,.0f}</div>
                <div class="card-sub">
                    Consumed: <strong>{report['consumed']:,.0f}</strong> {unit_str}
                </div>
                <div class="card-detail">
                    {cfg['detail_label']}: {detail_val} &nbsp;·&nbsp;
                    Renewable: {'Yes ✅' if report['renewable'] else 'No ❌'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Progress bar with colour class wrapper
        st.markdown(f'<div class="{cfg["bar_class"]}">', unsafe_allow_html=True)
        st.progress(
            min(report["utilisation_pct"] / 100, 1.0),
            text=f"Utilisation: {report['utilisation_pct']}%",
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONSUMER REPORTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header"><span class="icon">👥</span> Consumer Reports</div>',
    unsafe_allow_html=True,
)

for cname, consumer in st.session_state.consumers.items():
    with st.expander(f"📋  {cname}  —  ID: {consumer.consumer_id}", expanded=False):

        report = consumer.generate_usage_report()

        # ── Summary metrics row with improved styling ────────────────────
        st.markdown(
            """
            <div style='background: linear-gradient(135deg, #f1f8f1 0%, #e8f5e9 100%); 
                        padding: 1rem; border-radius: 10px; margin-bottom: 1.2rem;'>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        m1, m2, m3 = st.columns(3)
        total_consumed = sum(r["consumed"] for r in report["resources"])
        
        with m1:
            st.metric("📦 Assigned Resources", len(report["resources"]))
        with m2:
            st.metric("📊 Consumption Events", report["total_consumption_events"])
        with m3:
            st.metric("⚡ Total Consumed", f"{total_consumed:,.0f}", help="Combined consumption across all resources")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # ── Per-resource mini cards ──────────────────────────────────────
        if report["resources"]:
            st.markdown(
                """
                <div style='margin: 1.2rem 0 0.8rem; padding-bottom: 0.3rem; border-bottom: 2px solid #e8f5e9;'>
                    <strong style='color: #2e7d32; font-size: 0.95rem;'>📊 Resource Breakdown</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Fixed 3-column layout for better responsiveness
            rcols = st.columns(3, gap="medium")

            for ridx, r in enumerate(report["resources"]):
                cfg = _RES_CONFIG.get(r["name"], {})
                icon = cfg.get("icon", "📦")
                unit_str = r.get("unit", "units")

                with rcols[ridx]:
                    st.markdown(
                        f"""
                        <div class="mini-resource-card">
                            <div class="mini-card-icon">{icon}</div>
                            <div class="mini-card-title">{r['name']}</div>
                            <div class="mini-card-details">
                                Available: <strong>{r['total_available']:,.0f}</strong> {unit_str}<br>
                                Consumed: <strong>{r['consumed']:,.0f}</strong> {unit_str}<br>
                                Utilisation: <strong>{r['utilisation_pct']}%</strong>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # ── Consumption history table ────────────────────────────────────
        if report["consumption_history"]:
            st.markdown(
                """
                <div style='margin: 1.2rem 0 0.8rem; padding-bottom: 0.3rem; border-bottom: 2px solid #e8f5e9;'>
                    <strong style='color: #2e7d32; font-size: 0.95rem;'>📝 Consumption History</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.table(report["consumption_history"])
        else:
            st.info("No consumption recorded yet for this consumer.", icon="ℹ️")


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="footer">
        Built with <strong>Python OOP</strong> &nbsp;·&nbsp;
        <strong>Streamlit</strong> &nbsp;·&nbsp;
        <strong>Clean Architecture</strong><br>
        🌿 Sustainable Resource Management System &nbsp;© 2026
    </div>
    """,
    unsafe_allow_html=True,
)
