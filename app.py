import streamlit as st
import pickle
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session state for page routing ───────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "analyzer"

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --cream:   #f7f9f6;
    --white:   #ffffff;
    --green-1: #1a5c3a;
    --green-2: #2d7a52;
    --green-3: #4caf7d;
    --green-4: #a8d5b5;
    --green-5: #e4f5eb;
    --green-6: #f0faf3;
    --text:    #1e3528;
    --muted:   #6b8f76;
    --border:  #d4eadc;
    --shadow:  0 2px 24px rgba(26,92,58,0.08);
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stHeader"]  { background: transparent !important; display: none; }
[data-testid="stSidebar"] { display: none; }
.block-container {
    padding: 0 3rem 5rem !important;
    max-width: 1300px !important;
    margin: 0 auto;
}

/* ── Navbar ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.4rem 0; border-bottom: 1px solid var(--border); margin-bottom: 0;
}
.nav-logo { font-family: 'DM Serif Display', serif; font-size: 1.3rem; color: var(--green-1); }
.nav-logo em { color: var(--green-3); font-style: italic; }
.nav-cta {
    background: var(--green-1); color: #fff;
    border-radius: 999px; padding: 8px 22px;
    font-size: 0.78rem; font-weight: 600;
}

/* ── Global button base — comes FIRST so nav-pill overrides it below ── */
[data-testid="stButton"] > button {
    width: 100% !important; background: var(--green-1) !important;
    color: #fff !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: .88rem !important;
    letter-spacing: .04em !important; border: none !important;
    border-radius: 12px !important; height: 3.4rem !important;
    transition: background .2s, transform .15s, box-shadow .2s !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--green-2) !important; transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(26,92,58,.22) !important;
}

/* ── Nav pill buttons — MUST come AFTER global button block ── */
.nav-pill-wrap [data-testid="stButton"] > button,
.nav-pill-active [data-testid="stButton"] > button {
    width: auto !important;
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    border-radius: 6px !important;
    height: 1.6rem !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.03em !important;
    padding: 0 0.7rem !important;
    white-space: nowrap !important;
    box-shadow: none !important;
    text-transform: none !important;
    transform: none !important;
}
.nav-pill-wrap [data-testid="stButton"] > button:hover,
.nav-pill-active [data-testid="stButton"] > button:hover {
    background: var(--green-5) !important;
    color: var(--green-1) !important;
    box-shadow: none !important;
    transform: none !important;
}
.nav-pill-active [data-testid="stButton"] > button {
    background: var(--green-5) !important;
    color: var(--green-1) !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Hero ── */
.hero { text-align: center; padding: 5rem 1rem 3rem; }
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--green-5); border: 1px solid var(--green-4);
    border-radius: 999px; padding: 5px 16px;
    font-size: 0.7rem; font-weight: 600; color: var(--green-2);
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.6rem;
}
.hero-eyebrow::before { content: '●'; color: var(--green-3); animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: clamp(2.6rem, 5vw, 4.2rem) !important;
    font-weight: 400 !important; color: var(--green-1) !important;
    line-height: 1.12 !important; letter-spacing: -0.02em !important; margin-bottom: 1.2rem !important;
}
.hero h1 em { color: var(--green-3); font-style: italic; }
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
    text-align: center !important;
    width: 100%;
    display: block;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex; justify-content: center;
    border: 1px solid var(--border); border-radius: 16px;
    background: var(--white); max-width: 680px;
    margin: 0 auto 3.5rem; overflow: hidden; box-shadow: var(--shadow);
}
.stat-item { flex: 1; padding: 1.25rem 1rem; text-align: center; border-right: 1px solid var(--border); }
.stat-item:last-child { border-right: none; }
.stat-num { font-family: 'DM Serif Display', serif; font-size: 1.9rem; color: var(--green-1); line-height: 1; margin-bottom: 4px; }
.stat-lbl { font-size: 0.68rem; font-weight: 500; color: var(--muted); letter-spacing: 0.06em; text-transform: uppercase; }

/* ── How it works ── */
.how-strip { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin: 1.5rem 0 3rem; }
.how-card { background: var(--white); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; }
.how-num { font-family: 'DM Serif Display', serif; font-size: 2.4rem; color: var(--green-4); line-height: 1; margin-bottom: .5rem; }
.how-title { font-weight: 600; font-size: 0.88rem; color: var(--green-1); margin-bottom: 4px; }
.how-body  { font-size: 0.78rem; color: var(--muted); line-height: 1.6; }

/* ── Section head ── */
.section-head { margin-bottom: 1.5rem; }
.section-head h2 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.7rem !important; font-weight: 400 !important;
    color: var(--green-1) !important; margin-bottom: .3rem !important;
}
.section-head p { color: var(--muted); font-size: 0.85rem; }
.section-tag {
    font-family: 'DM Mono', monospace; font-size: 0.62rem;
    color: var(--green-3); letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: .4rem; display: block;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] label {
    font-family: 'DM Sans', sans-serif !important; font-size: 0.75rem !important;
    font-weight: 600 !important; color: var(--green-1) !important;
    text-transform: uppercase !important; letter-spacing: .02em !important;
}
[data-testid="stNumberInput"] input {
    background: var(--green-6) !important; border: 1.5px solid var(--green-4) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'DM Mono', monospace !important; font-size: .93rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--green-3) !important;
    box-shadow: 0 0 0 3px rgba(76,175,125,.18) !important; outline: none !important;
}
[data-testid="stSlider"] label {
    font-family: 'DM Sans', sans-serif !important; font-size: 0.75rem !important;
    font-weight: 600 !important; color: var(--green-1) !important;
    text-transform: uppercase !important; letter-spacing: .02em !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--green-5) !important; border: 1px solid var(--green-4) !important;
    border-radius: 12px !important; padding: 4px !important; gap: 4px !important; margin-bottom: .5rem !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif !important; font-size: .78rem !important;
    font-weight: 600 !important; color: var(--muted) !important;
    border-radius: 8px !important; padding: 9px 20px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--white) !important; color: var(--green-1) !important;
    box-shadow: 0 1px 6px rgba(26,92,58,.1) !important;
}
[data-testid="stTabs"] [data-testid="stTabPanel"] { padding-top: 1.5rem !important; }

/* ── Verdict ── */
.verdict { display: flex; align-items: flex-start; gap: 1rem; border-radius: 16px; padding: 1.5rem 1.75rem; margin-bottom: 1.25rem; }
.verdict-fraud { background: #fff5f5; border: 1.5px solid #f5c2c2; }
.verdict-ok    { background: var(--green-5); border: 1.5px solid var(--green-4); }
.verdict-icon  { font-size: 2rem; line-height: 1; margin-top: 2px; }
.verdict-title { font-family: 'DM Serif Display', serif; font-size: 1.25rem; color: var(--green-1); margin-bottom: 4px; }
.verdict-fraud .verdict-title { color: #b91c1c; }
.verdict-body  { font-size: .82rem; color: var(--muted); line-height: 1.6; }

/* ── Prob bar ── */
.prob-label { display:flex; justify-content:space-between; font-size:.75rem; font-weight:600; color:var(--green-1); margin-bottom:6px; font-family:'DM Mono',monospace; }
.prob-track { background:var(--green-5); border-radius:999px; height:10px; overflow:hidden; border:1px solid var(--green-4); }
.prob-fill  { height:100%; border-radius:999px; transition:width 1s cubic-bezier(.4,0,.2,1); }

/* ── Threshold info box ── */
.thresh-box {
    background: var(--green-6); border: 1px solid var(--green-4);
    border-radius: 10px; padding: .75rem 1rem;
    display: flex; align-items: center; gap: .75rem;
    font-size: .78rem; color: var(--muted); margin-top: .75rem;
}
.thresh-box strong { color: var(--green-1); font-family: 'DM Mono', monospace; }

/* ── Detail table ── */
.detail-row { display:flex; justify-content:space-between; padding:.55rem 0; border-bottom:1px solid var(--green-5); font-size:.8rem; }
.detail-row:last-child { border-bottom:none; }
.detail-key { color:var(--muted); font-weight:500; }
.detail-val { font-family:'DM Mono',monospace; color:var(--green-1); font-size:.78rem; }

/* ── Expander ── */
[data-testid="stExpander"] { background:var(--green-6) !important; border:1px solid var(--border) !important; border-radius:12px !important; }
[data-testid="stExpander"] summary { font-family:'DM Sans',sans-serif !important; font-size:.8rem !important; font-weight:600 !important; color:var(--green-1) !important; }

/* ── Alert ── */
[data-testid="stAlert"] { background:var(--green-5) !important; border:1px solid var(--green-4) !important; border-radius:10px !important; color:var(--muted) !important; font-size:.8rem !important; }

hr { border:none !important; border-top:1px solid var(--border) !important; margin:2.5rem 0 !important; }

/* ── Info box ── */
.info-callout {
    background: var(--green-6); border: 1px solid var(--green-4);
    border-left: 4px solid var(--green-3);
    border-radius: 10px; padding: 1rem 1.25rem;
    font-size: .8rem; color: var(--muted); line-height: 1.6; margin-bottom: 1.5rem;
}
.info-callout strong { color: var(--green-1); }

/* ── Knowledge Hub ── */
.kb-hero {
    background: linear-gradient(135deg, var(--green-1) 0%, var(--green-2) 100%);
    border-radius: 24px; padding: 4rem 3rem; margin: 2rem 0 3rem;
    position: relative; overflow: hidden;
}
.kb-hero::before {
    content: '✚'; position: absolute; right: 3rem; top: 50%; transform: translateY(-50%);
    font-size: 12rem; color: rgba(255,255,255,0.04); line-height: 1;
}
.kb-hero h1 { font-family: 'DM Serif Display', serif !important; font-size: 2.8rem !important; color: #fff !important; font-weight: 400 !important; margin-bottom: .75rem !important; }
.kb-hero h1 em { color: var(--green-4); font-style: italic; }
.kb-hero p { color: rgba(255,255,255,0.65); font-size: .95rem; max-width: 500px; line-height: 1.7; }

.kb-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.25rem; margin-bottom: 2.5rem; }
.kb-grid-2 { grid-template-columns: repeat(2,1fr); }

.article-card {
    background: var(--white); border: 1px solid var(--border);
    border-radius: 20px; padding: 1.75rem; display: flex;
    flex-direction: column; gap: .75rem; transition: box-shadow .2s, transform .2s;
}
.article-card:hover { box-shadow: var(--shadow); transform: translateY(-3px); }
.article-tag {
    display: inline-flex; align-items: center; gap: 5px;
    background: var(--green-5); border-radius: 999px;
    padding: 3px 12px; font-size: .65rem; font-weight: 600;
    color: var(--green-2); letter-spacing: .06em; text-transform: uppercase; width: fit-content;
}
.article-icon { font-size: 2rem; line-height: 1; }
.article-title { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: var(--green-1); line-height: 1.3; }
.article-body { font-size: .8rem; color: var(--muted); line-height: 1.7; flex: 1; }
.article-footer {
    display: flex; align-items: center; justify-content: space-between;
    padding-top: .75rem; border-top: 1px solid var(--green-5);
    font-size: .7rem; color: #b0c4b8; font-family: 'DM Mono', monospace;
}
.read-more { font-size: .75rem; font-weight: 600; color: var(--green-2); }

.stat-insight-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin: 2rem 0 3rem; }
.insight-card { background: var(--white); border: 1px solid var(--border); border-radius: 16px; padding: 1.4rem; text-align: center; }
.insight-num { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: var(--green-1); line-height: 1; }
.insight-num span { font-size: 1.2rem; color: var(--green-3); }
.insight-desc { font-size: .72rem; color: var(--muted); margin-top: 5px; line-height: 1.4; }

.tips-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 1rem; margin-bottom: 3rem; }
.tip-card { background: var(--green-6); border: 1px solid var(--green-4); border-radius: 16px; padding: 1.5rem; display: flex; gap: 1rem; align-items: flex-start; }
.tip-num { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: var(--green-4); line-height: 1; min-width: 2rem; }
.tip-title { font-weight: 600; font-size: .88rem; color: var(--green-1); margin-bottom: 4px; }
.tip-body  { font-size: .78rem; color: var(--muted); line-height: 1.6; }

.warning-banner {
    background: #fffbeb; border: 1.5px solid #fcd34d;
    border-radius: 16px; padding: 1.5rem 2rem;
    display: flex; gap: 1.25rem; align-items: flex-start; margin-bottom: 3rem;
}
.warning-body { font-size: .85rem; color: #78350f; line-height: 1.6; }
.warning-body strong { color: #92400e; display: block; font-size: .95rem; margin-bottom: .3rem; }

/* ── Emergency card ── */
.emergency-card {
    background: var(--green-1); border-radius: 20px; padding: 3rem;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 2rem; margin-top: 1rem; margin-bottom: 3rem;
}
.emergency-left h3 {
    font-family: 'DM Serif Display', serif; font-size: 1.9rem;
    color: #fff; font-weight: 400; margin-bottom: .5rem;
}
.emergency-left h3 em { color: var(--green-4); font-style: italic; }
.emergency-left p { color: rgba(255,255,255,0.55); font-size: .85rem; max-width: 460px; line-height: 1.7; }
.emergency-phone {
    background: var(--green-2); border-radius: 16px;
    padding: 1.5rem 2.5rem; text-align: center; min-width: 220px;
}
.emergency-phone-lbl {
    font-size: .65rem; letter-spacing: .1em; text-transform: uppercase;
    color: var(--green-4); font-weight: 600; margin-bottom: .4rem;
}
.emergency-phone-num {
    font-family: 'DM Serif Display', serif; font-size: 1.7rem; color: #fff;
}
.emergency-phone-tag { font-size: .7rem; color: rgba(255,255,255,0.45); margin-top: .3rem; }

.footer { display:flex; justify-content:space-between; padding:1.5rem 0; border-top:1px solid var(--border); margin-top:4rem; font-size:.72rem; color:#b0c4b8; flex-wrap:wrap; gap:.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    with open('models/lr_model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['threshold'], data['feature_names']

model, threshold, all_feature_cols = load_assets()

# The 8 key features shown to the user — rest are filled with 0
KEY_FEATURES = [
    'TotalReimbursed',
    'ClaimsPerBeneficiary',
    'InpatientRatio',
    'ReimbursementCV',
    'MeanDiagnosisCount',
    'PctDeceasedPatients',
    'MeanChronicConds',
    'UniquePhysicians',
]


# ── Navbar ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="navbar">', unsafe_allow_html=True)
nav_l, nav_r = st.columns([3, 4])

with nav_l:
    st.markdown('<div class="nav-logo">🩺 HealthGuard <em>AI</em></div>', unsafe_allow_html=True)

with nav_r:
    r1, r2, r3 = st.columns([1.2, 1.5, 2])
    with r1:
        cls1 = "nav-pill-active" if st.session_state.page == "analyzer" else "nav-pill-wrap"
        st.markdown(f'<div class="{cls1}">', unsafe_allow_html=True)
        if st.button("Analyzer"):
            st.session_state.page = "analyzer"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r2:
        cls2 = "nav-pill-active" if st.session_state.page == "knowledge" else "nav-pill-wrap"
        st.markdown(f'<div class="{cls2}">', unsafe_allow_html=True)
        if st.button("Knowledge Hub"):
            st.session_state.page = "knowledge"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r3:
        st.markdown('<div style="text-align:right;padding-top:4px"><div class="nav-cta">CSS 324 · Final Project</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYZER
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "analyzer":

    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">AI-Powered Fraud Detection</div>
        <h1>Protect healthcare,<br><em>one claim at a time.</em></h1>
        <p class="hero-sub" style="text-align:center;margin-left:auto;margin-right:auto;">
            An intelligent audit system that analyses medical provider activity
            and flags anomalies before fraudulent claims are paid out.
        </p>
    </div>
    <div class="stats-strip">
        <div class="stat-item"><div class="stat-num">8</div><div class="stat-lbl">Key features</div></div>
        <div class="stat-item"><div class="stat-num">LR</div><div class="stat-lbl">Model type</div></div>
        <div class="stat-item"><div class="stat-num">71%</div><div class="stat-lbl">F1 score</div></div>
        <div class="stat-item"><div class="stat-num">96.6%</div><div class="stat-lbl">ROC-AUC</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="how-strip">
        <div class="how-card">
            <div class="how-num">01</div>
            <div class="how-title">Enter provider data</div>
            <div class="how-body">Fill in the 8 key financial and clinical statistics for the provider you want to audit.</div>
        </div>
        <div class="how-card">
            <div class="how-num">02</div>
            <div class="how-title">AI analyses patterns</div>
            <div class="how-body">The Logistic Regression model evaluates all features using an optimised F1 decision threshold.</div>
        </div>
        <div class="how-card">
            <div class="how-num">03</div>
            <div class="how-title">Review the verdict</div>
            <div class="how-body">Get an instant fraud risk score and an actionable recommendation for your audit team.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
        <span class="section-tag">Step 1 — Provider Parameters</span>
        <h2>Enter provider data</h2>
        <p>The 8 most predictive features from the trained Logistic Regression model.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-callout">
        <strong>Why only 8 features?</strong>
        From the full set of 24 engineered features, these 8 carry the strongest signal in the LR model —
        capturing financial anomalies, clinical complexity, and patient risk simultaneously.
        All other features are set to their training-set means automatically.
    </div>
    """, unsafe_allow_html=True)

    user_input = {}

    # ── Demo preset values via session state ─────────────────────────────
    DEMO_LEGIT = {
        'TotalReimbursed': 90000.0, 'ClaimsPerBeneficiary': 1.2,
        'ReimbursementCV': 0.55, 'UniquePhysicians': 8,
        'InpatientRatio': 0.15, 'MeanDiagnosisCount': 2.5,
        'MeanChronicConds': 2.8, 'PctDeceasedPatients': 0.03,
    }
    DEMO_FRAUD = {
        'TotalReimbursed': 1200000.0, 'ClaimsPerBeneficiary': 6.1,
        'ReimbursementCV': 2.1, 'UniquePhysicians': 3,
        'InpatientRatio': 0.78, 'MeanDiagnosisCount': 8.4,
        'MeanChronicConds': 6.9, 'PctDeceasedPatients': 0.23,
    }
    DEFAULTS = {
        'TotalReimbursed': 15000.0, 'ClaimsPerBeneficiary': 1.5,
        'ReimbursementCV': 0.5, 'UniquePhysicians': 5,
        'InpatientRatio': 0.20, 'MeanDiagnosisCount': 3.0,
        'MeanChronicConds': 4.0, 'PctDeceasedPatients': 0.05,
    }
    # Initialize session state defaults for inputs
    for feat, default_val in DEFAULTS.items():
        key = f"inp_{feat}"
        if key not in st.session_state:
            st.session_state[key] = default_val

    # Apply demo preset if requested
    if st.session_state.get("_apply_demo"):
        preset = st.session_state["_apply_demo"]
        for feat, val in preset.items():
            st.session_state[f"inp_{feat}"] = val
        st.session_state["_apply_demo"] = None

    tab1, tab2 = st.tabs([
        "💰  Financial & Activity",
        "🏥  Clinical & Patient"
    ])

    with tab1:
        st.markdown("<div style='margin-top:.5rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            user_input['TotalReimbursed'] = st.number_input(
                "Total Reimbursed ($)",
                min_value=0.0, step=1000.0,
                key="inp_TotalReimbursed",
                help="Total dollar amount reimbursed to this provider across all claims"
            )
        with c2:
            user_input['ClaimsPerBeneficiary'] = st.number_input(
                "Claims per Beneficiary",
                min_value=0.0, step=0.1,
                key="inp_ClaimsPerBeneficiary",
                help="Average number of claims submitted per unique patient. >3 is suspicious."
            )
        with c3:
            user_input['ReimbursementCV'] = st.number_input(
                "Reimbursement CV (Std/Mean)",
                min_value=0.0, step=0.05,
                key="inp_ReimbursementCV",
                help="Coefficient of variation of reimbursements. High CV = inconsistent billing."
            )
        st.markdown("<div style='margin-top:.75rem'></div>", unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            user_input['UniquePhysicians'] = st.number_input(
                "Unique Physicians",
                min_value=0, step=1,
                key="inp_UniquePhysicians",
                help="Number of distinct physicians billing under this provider. Very few or very many is a red flag."
            )
        with c5:
            user_input['InpatientRatio'] = st.number_input(
                "Inpatient Ratio (0–1)",
                min_value=0.0, max_value=1.0, step=0.01,
                key="inp_InpatientRatio",
                help="Fraction of total claims that are inpatient. Fraudsters often inflate this (>0.5)."
            )

    with tab2:
        st.markdown("<div style='margin-top:.5rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            user_input['MeanDiagnosisCount'] = st.number_input(
                "Mean Diagnosis Count",
                min_value=0.0, step=0.1,
                key="inp_MeanDiagnosisCount",
                help="Average number of diagnoses per claim. High values suggest upcoding."
            )
        with c2:
            user_input['MeanChronicConds'] = st.number_input(
                "Mean Chronic Conditions",
                min_value=0.0, step=0.1,
                key="inp_MeanChronicConds",
                help="Average chronic conditions per patient. Fraudsters target patients with more conditions."
            )
        with c3:
            user_input['PctDeceasedPatients'] = st.number_input(
                "% Deceased Patients (0–1)",
                min_value=0.0, max_value=1.0, step=0.01,
                key="inp_PctDeceasedPatients",
                help="Fraction of patients who are deceased. Billing after death is a major fraud signal."
            )

    # Fill ALL model features — key ones from user, rest default to 0
    full_input = {col: 0.0 for col in all_feature_cols}
    for k, v in user_input.items():
        if k in full_input:
            full_input[k] = v

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    col_btn, col_hint = st.columns([2, 3])
    with col_btn:
        run = st.button("🔍  Analyse Provider")
    with col_hint:
        st.markdown(f"""
        <div style="display:flex;align-items:center;height:3.4rem;
             font-size:.78rem;color:#6b8f76;padding-left:.75rem;line-height:1.5;">
            Model evaluates all parameters using the optimised threshold of
            <b style="margin-left:4px">{threshold:.4f}</b> &nbsp;for maximum F1 performance.
        </div>
        """, unsafe_allow_html=True)

    # ── Quick demo presets ────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns([1, 1, 4])
    with d1:
        if st.button("✅  Load Legit Example"):
            st.session_state["_apply_demo"] = DEMO_LEGIT
            st.rerun()
    with d2:
        if st.button("🚨  Load Fraud Example"):
            st.session_state["_apply_demo"] = DEMO_FRAUD
            st.rerun()

    # ── Results ───────────────────────────────────────────────────────────
    if run:
        with st.spinner("Analysing provider data…"):
            time.sleep(0.6)

        input_df    = pd.DataFrame([full_input])[all_feature_cols]
        probability = model.predict_proba(input_df)[0][1]
        prediction  = int(probability >= threshold)
        pct         = probability * 100

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-head">
            <span class="section-tag">Step 2 — Results</span>
            <h2>System verdict</h2>
            <p>Based on the provided parameters, the model has generated the following risk assessment.</p>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([5, 4], gap="large")

        with left:
            if pct < threshold * 100:
                gauge_color = "#2d7a52"; fill_grad = "linear-gradient(90deg,#a8d5b5,#4caf7d)"; zone_lbl = "Low Risk"
            elif pct < 70:
                gauge_color = "#d97706"; fill_grad = "linear-gradient(90deg,#fde68a,#f59e0b)"; zone_lbl = "Moderate Risk"
            else:
                gauge_color = "#dc2626"; fill_grad = "linear-gradient(90deg,#fca5a5,#dc2626)"; zone_lbl = "High Risk"

            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=pct,
                number={'suffix':'%','valueformat':'.1f',
                        'font':{'size':54,'color':gauge_color,'family':'DM Serif Display'}},
                gauge={
                    'axis':{'range':[0,100],'tickwidth':1,'tickcolor':'#d4eadc',
                            'tickfont':{'family':'DM Mono','size':10,'color':'#6b8f76'},'nticks':6},
                    'bar':{'color':gauge_color,'thickness':0.18},
                    'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                    'steps':[
                        {'range':[0, threshold*100],   'color':'#e4f5eb'},
                        {'range':[threshold*100, 70],  'color':'#fef9ec'},
                        {'range':[70, 100],             'color':'#fff5f5'},
                    ],
                    'threshold':{'line':{'color':gauge_color,'width':3},'thickness':0.8,'value':pct}
                },
                domain={'x':[0,1],'y':[0,1]},
                title={'text': f"<b>FRAUD RISK SCORE</b><br><span style='font-size:11px;color:#6b8f76'>{zone_lbl}</span>",
                       'font':{'family':'DM Sans','size':15,'color':'#1e3528'}}
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=320, margin=dict(t=70,b=10,l=30,r=30)
            )
            st.plotly_chart(fig, use_container_width=True)

            thresh_pct = threshold * 100
            st.markdown(f"""
            <div style="display:flex;justify-content:center;gap:1.5rem;font-size:.7rem;
                        font-weight:600;color:#6b8f76;margin-top:-.5rem;">
                <span style="color:#2d7a52">● 0–{thresh_pct:.0f}% Normal</span>
                <span style="color:#d97706">● {thresh_pct:.0f}–70% Review</span>
                <span style="color:#dc2626">● 70–100% Flag</span>
            </div>""", unsafe_allow_html=True)

        with right:
            if prediction == 1:
                st.markdown("""
                <div class="verdict verdict-fraud">
                    <div class="verdict-icon">🚨</div>
                    <div>
                        <div class="verdict-title">Fraud Detected</div>
                        <div class="verdict-body">This provider's activity exceeds the anomaly threshold.
                        We recommend suspending payments and initiating a full documentation audit.</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="verdict verdict-ok">
                    <div class="verdict-icon">✅</div>
                    <div>
                        <div class="verdict-title">Activity Normal</div>
                        <div class="verdict-body">The provider's metrics fall within the expected range.
                        No immediate action is required at this time.</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            bar_color = "#2d7a52" if prediction == 0 else "#dc2626"
            st.markdown(f"""
            <div class="prob-label">
                <span>Anomaly probability</span>
                <span style="color:{bar_color}">{pct:.2f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{pct:.1f}%;background:{fill_grad};"></div>
            </div>
            <div class="thresh-box">
                🎯 <span>Decision threshold: <strong>{threshold:.4f}</strong>
                ({threshold*100:.1f}%) — optimised for max F1</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
            with st.expander("View full analysis details"):
                for k, v in {
                    "Model"              : "Logistic Regression (RobustScaler + SMOTE)",
                    "Features used"      : f"{len(all_feature_cols)} (8 user-defined + defaults)",
                    "P(fraud)"           : f"{probability:.6f}",
                    "P(legitimate)"      : f"{1-probability:.6f}",
                    "Decision threshold" : f"{threshold:.6f}",
                    "Final label"        : "FRAUD" if prediction==1 else "LEGITIMATE",
                    "Risk zone"          : zone_lbl,
                }.items():
                    st.markdown(
                        f'<div class="detail-row">'
                        f'<span class="detail-key">{k}</span>'
                        f'<span class="detail-val">{v}</span></div>',
                        unsafe_allow_html=True
                    )
                st.markdown("<div style='margin-top:.75rem'></div>", unsafe_allow_html=True)
                st.info("This score is a decision-support tool and should be reviewed by a qualified auditor before action is taken.")

        # ── Key risk signal flags ────────────────────────────────────────
        st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-head">
            <span class="section-tag">Step 3 — Risk Signals</span>
            <h2>Key risk flags</h2>
            <p>Automatic rule-based flags raised by the input values.</p>
        </div>""", unsafe_allow_html=True)

        flags = []
        if user_input.get('ClaimsPerBeneficiary', 0) > 3.5:
            flags.append(("⚠️ High claims per patient", f"{user_input['ClaimsPerBeneficiary']:.1f} claims/patient — typical legitimate providers are below 2.0"))
        if user_input.get('InpatientRatio', 0) > 0.5:
            flags.append(("⚠️ Abnormal inpatient ratio", f"{user_input['InpatientRatio']:.0%} inpatient — suggests unnecessary admissions"))
        if user_input.get('ReimbursementCV', 0) > 1.5:
            flags.append(("⚠️ High billing variance", f"CV = {user_input['ReimbursementCV']:.2f} — inconsistent reimbursement pattern"))
        if user_input.get('PctDeceasedPatients', 0) > 0.15:
            flags.append(("🚨 Elevated patient mortality", f"{user_input['PctDeceasedPatients']:.0%} deceased — potential billing-after-death fraud"))
        if user_input.get('MeanDiagnosisCount', 0) > 6:
            flags.append(("⚠️ Excessive diagnosis coding", f"{user_input['MeanDiagnosisCount']:.1f} diagnoses/claim — strong upcoding signal"))
        if user_input.get('UniquePhysicians', 0) <= 2:
            flags.append(("⚠️ Physician concentration risk", f"Only {int(user_input['UniquePhysicians'])} physician(s) — highly concentrated billing"))
        if user_input.get('TotalReimbursed', 0) > 500000:
            flags.append(("⚠️ Very high total reimbursements", f"${user_input['TotalReimbursed']:,.0f} — outlier-level total billing"))

        if not flags:
            st.success("✅ No major risk flags detected. All key metrics appear within normal ranges.")
        else:
            for title, desc in flags:
                color = "#b91c1c" if "🚨" in title else "#92400e"
                bg    = "#fff5f5" if "🚨" in title else "#fffbeb"
                border= "#f5c2c2" if "🚨" in title else "#fcd34d"
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {border};border-radius:10px;
                            padding:.85rem 1.1rem;margin-bottom:.6rem;font-size:.82rem;">
                    <strong style="color:{color}">{title}</strong><br>
                    <span style="color:#6b8f76">{desc}</span>
                </div>""", unsafe_allow_html=True)

        # ── Input values bar chart ────────────────────────────────────────
        st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-head">
            <span class="section-tag">Step 4 — Feature Breakdown</span>
            <h2>Input values overview</h2>
            <p>Your 8 entered feature values, displayed for reference.</p>
        </div>""", unsafe_allow_html=True)

        feat_labels = {
            'TotalReimbursed': 'Total Reimbursed ($)',
            'ClaimsPerBeneficiary': 'Claims / Beneficiary',
            'ReimbursementCV': 'Reimbursement CV',
            'UniquePhysicians': 'Unique Physicians',
            'InpatientRatio': 'Inpatient Ratio',
            'MeanDiagnosisCount': 'Mean Diagnosis Count',
            'MeanChronicConds': 'Mean Chronic Conditions',
            'PctDeceasedPatients': '% Deceased Patients',
        }
        # Normalise for display
        vals_raw = [user_input.get(f, 0) for f in KEY_FEATURES]
        max_val  = max(abs(v) for v in vals_raw) if any(vals_raw) else 1
        vals_norm = [v / max_val for v in vals_raw]
        labels    = [feat_labels[f] for f in KEY_FEATURES]
        colours   = ['#dc2626' if abs(n) > 0.65 else '#d97706' if abs(n) > 0.35 else '#4caf7d'
                     for n in vals_norm]

        fig2 = go.Figure(go.Bar(
            x=vals_raw, y=labels, orientation='h',
            marker=dict(color=colours, line=dict(width=0)),
            text=[f"{v:,.2f}" for v in vals_raw],
            textposition='outside',
            textfont=dict(family='DM Mono', size=10, color='#6b8f76'),
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300, margin=dict(t=10,b=10,l=10,r=80),
            xaxis=dict(showgrid=True, gridcolor='#e4f5eb', zeroline=False,
                       tickfont=dict(family='DM Mono', size=10, color='#6b8f76')),
            yaxis=dict(showgrid=False, tickfont=dict(family='DM Mono', size=10, color='#1e3528')),
            bargap=0.35,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: KNOWLEDGE HUB
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "knowledge":

    st.markdown("""
    <div class="kb-hero">
        <h1>How to prevent<br><em>healthcare fraud.</em></h1>
        <p>Evidence-based strategies, red flag indicators, and best practices
        for auditors, compliance teams, and healthcare administrators.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
        <span class="section-tag">By the numbers</span>
        <h2>The scale of the problem</h2>
        <p>Healthcare fraud costs the global healthcare system hundreds of billions every year.</p>
    </div>
    <div class="stat-insight-grid">
        <div class="insight-card">
            <div class="insight-num">$<span>100B</span></div>
            <div class="insight-desc">Estimated annual cost of healthcare fraud in the U.S. alone</div>
        </div>
        <div class="insight-card">
            <div class="insight-num">3<span>–10%</span></div>
            <div class="insight-desc">Of all healthcare spending lost to fraud, waste, and abuse</div>
        </div>
        <div class="insight-card">
            <div class="insight-num">1<span> in 10</span></div>
            <div class="insight-desc">Medicare claims contains a billing error or fraudulent charge</div>
        </div>
        <div class="insight-card">
            <div class="insight-num">92<span>%</span></div>
            <div class="insight-desc">Of fraud cases involve billing for services never rendered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-banner">
        <div style="font-size:2rem;line-height:1">⚠️</div>
        <div class="warning-body">
            <strong>Why early detection matters</strong>
            For every $1 invested in healthcare fraud detection and prevention programs,
            studies estimate a return of $8–$10 in recovered funds and prevented losses.
            AI-based screening tools like HealthGuard can flag suspicious providers
            before payments are processed — not after.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
        <span class="section-tag">Core articles</span>
        <h2>Understanding fraud patterns</h2>
        <p>The most common schemes and how to recognise them in claim data.</p>
    </div>
    <div class="kb-grid">
        <div class="article-card">
            <div class="article-tag">🏥 Billing Fraud</div>
            <div class="article-icon">🧾</div>
            <div class="article-title">Upcoding & Phantom Billing: The Two Most Common Schemes</div>
            <div class="article-body">Upcoding means billing for a more expensive procedure than actually performed.
            Phantom billing means charging for services never rendered at all. Together, these two schemes
            account for the majority of Medicare and Medicaid fraud cases. Key red flags include a provider's
            average reimbursement being significantly higher than peers in the same specialty and region.</div>
            <div class="article-footer"><span>8 min read · Billing</span></div>
        </div>
        <div class="article-card">
            <div class="article-tag">👨‍⚕️ Provider Patterns</div>
            <div class="article-icon">📊</div>
            <div class="article-title">Statistical Outliers: When Provider Volume Signals Risk</div>
            <div class="article-body">A physician billing for more hours per day than physically possible is a classic
            red flag. Legitimate providers typically see 15–25 patients per day. Providers with extremely high
            patient-to-physician ratios, or those billing for procedures that rarely occur together, should be
            prioritised for audit. Logistic Regression models excel at capturing linear separability in
            provider-level aggregates.</div>
            <div class="article-footer"><span>6 min read · Analytics</span></div>
        </div>
        <div class="article-card">
            <div class="article-tag">🤝 Collusion</div>
            <div class="article-icon">🔗</div>
            <div class="article-title">Provider–Patient Collusion: The Hidden Threat</div>
            <div class="article-body">In collusion schemes, patients knowingly allow their insurance information to be
            used for fictitious claims in exchange for cash kickbacks or free services. Indicators include patients
            visiting an unusual number of providers, or the same beneficiary appearing across multiple suspicious
            provider accounts. Network analysis of shared beneficiary IDs is a powerful detection technique.</div>
            <div class="article-footer"><span>5 min read · Investigations</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
        <span class="section-tag">Prevention guide</span>
        <h2>10 ways to prevent healthcare fraud</h2>
        <p>Practical steps for compliance officers, auditors, and healthcare organisations.</p>
    </div>
    <div class="tips-grid">
        <div class="tip-card"><div class="tip-num">1</div><div>
            <div class="tip-title">Implement real-time claim screening</div>
            <div class="tip-body">Use AI-powered tools to flag suspicious claims automatically before payment is released.
            Pre-payment review is far more effective than post-payment recovery.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">2</div><div>
            <div class="tip-title">Monitor provider billing patterns continuously</div>
            <div class="tip-body">Compare each provider's billing profile against specialty benchmarks.
            Sudden spikes in volume or reimbursement amounts warrant immediate investigation.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">3</div><div>
            <div class="tip-title">Verify credentials and licences regularly</div>
            <div class="tip-body">Fraudulent providers sometimes operate under stolen or revoked licences.
            Cross-referencing provider NPI numbers with national licence databases catches this early.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">4</div><div>
            <div class="tip-title">Conduct random beneficiary outreach</div>
            <div class="tip-body">Calling patients to confirm they actually received billed services is simple but
            highly effective. Beneficiaries often have no idea their information is being misused.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">5</div><div>
            <div class="tip-title">Train clinical and admin staff on red flags</div>
            <div class="tip-body">Employees are often the first to notice unusual billing requests.
            A strong internal reporting culture and whistleblower protection policy are essential assets.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">6</div><div>
            <div class="tip-title">Analyse diagnosis and procedure code combinations</div>
            <div class="tip-body">Certain code combinations are clinically implausible.
            Automated rule engines flag these instantly before a claim reaches the payment stage.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">7</div><div>
            <div class="tip-title">Use network analysis to find collusion rings</div>
            <div class="tip-body">Graph-based analysis reveals clusters of providers and beneficiaries with abnormally
            high interconnectedness — a key signature of organised fraud rings.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">8</div><div>
            <div class="tip-title">Establish a fraud hotline and reward reporting</div>
            <div class="tip-body">Anonymous tip lines encourage insiders and patients to report suspicious activity.
            The False Claims Act allows whistleblowers to share in federal recovery amounts.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">9</div><div>
            <div class="tip-title">Perform regular external audits</div>
            <div class="tip-body">Third-party audits provide an independent view that internal teams may miss.
            Rotate audit firms periodically to prevent familiarity bias.</div>
        </div></div>
        <div class="tip-card"><div class="tip-num">10</div><div>
            <div class="tip-title">Invest in data infrastructure and interoperability</div>
            <div class="tip-body">Fraud often hides across system boundaries. Unified data lakes that consolidate
            claims, EHR, and pharmacy data give analysts a complete view of provider activity.</div>
        </div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-head">
        <span class="section-tag">Deep dives</span>
        <h2>Advanced detection techniques</h2>
    </div>
    <div class="kb-grid kb-grid-2">
        <div class="article-card">
            <div class="article-tag">🤖 Machine Learning</div>
            <div class="article-icon">🧠</div>
            <div class="article-title">Why Logistic Regression Achieves the Highest AUC in This Study</div>
            <div class="article-body">Despite its simplicity, Logistic Regression achieved the best ROC-AUC (0.9659)
            in our experiments — outperforming XGBoost, LightGBM, and Random Forest on this dataset.
            With RobustScaler handling outliers and SMOTE addressing class imbalance, LR's linear decision
            boundary generalises well on provider-level aggregates. Optimal threshold selection and F1-tuned
            hyperparameter search pushed the model's recall above 70%.</div>
            <div class="article-footer"><span>12 min read · ML / Technical</span></div>
        </div>
        <div class="article-card">
            <div class="article-tag">⚖️ Compliance</div>
            <div class="article-icon">📋</div>
            <div class="article-title">HIPAA, the False Claims Act, and Your Legal Obligations</div>
            <div class="article-body">Healthcare organisations are legally required to maintain compliance programs
            under the False Claims Act and the Anti-Kickback Statute. HIPAA additionally requires safeguards
            for patient data used in fraud investigations. This guide explains the regulatory landscape,
            the penalties for non-compliance (up to $25,000 per violation per year), and the seven elements
            of an effective compliance program as defined by the OIG.</div>
            <div class="article-footer"><span>10 min read · Legal / Compliance</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Emergency card
    st.markdown("""
    <div class="section-head">
        <span class="section-tag">Report fraud</span>
        <h2>Encountered healthcare fraud?</h2>
        <p>Don't wait. Early reporting protects patients and stops providers from continuing fraudulent operations.</p>
    </div>
    <div class="emergency-card">
        <div class="emergency-left">
            <h3>Report it <em>immediately.</em></h3>
            <p>If you or someone you know has been a victim of healthcare billing fraud,
            or if you work in the industry and have witnessed suspicious activity —
            call the fraud hotline. All reports are confidential and reviewed within 24 hours.
            Available 24/7. No case too small.</p>
        </div>
        <div class="emergency-phone">
            <div class="emergency-phone-lbl">📞 Fraud Hotline</div>
            <div class="emergency-phone-num">+7 775 071 8306</div>
            <div class="emergency-phone-tag">24/7 · Confidential · Free</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>HealthGuard AI · CSS 324 Introduction to Machine Learning · Final Project</span>
    <span>Built with Logistic Regression &amp; Streamlit</span>
</div>
""", unsafe_allow_html=True)