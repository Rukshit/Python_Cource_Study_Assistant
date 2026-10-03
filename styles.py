"""
styles.py - Obsidian Studio & Cyber-Glass Educational Design System
A distinctive, high-end UI with glassmorphism, electric neon accents,
macOS terminal window styling, and seamless visual hierarchy.
"""

def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Typography & Reset */
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #030712 !important;
        color: #f1f5f9;
    }

    code, pre, .stCodeBlock, .stCodeBlock code {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Ambient Background Glow */
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.06) 35%, transparent 75%),
                    radial-gradient(circle at 10% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                    #030712 !important;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
    }

    /* Glassmorphism Cards */
    .glass-card, .edu-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.42);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .glass-card:hover, .edu-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.55), 0 0 15px rgba(99, 102, 241, 0.15);
    }

    .glass-card-interactive {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.25rem;
    }

    /* Gradient Borders & Neon Accents */
    .neon-indigo, .card-accent-blue {
        border-left: 4px solid #6366f1 !important;
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }
    .neon-cyan {
        border-left: 4px solid #06b6d4 !important;
        background: linear-gradient(135deg, rgba(8, 51, 68, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }
    .neon-emerald, .card-accent-emerald {
        border-left: 4px solid #10b981 !important;
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }
    .neon-amber, .card-accent-amber {
        border-left: 4px solid #f59e0b !important;
        background: linear-gradient(135deg, rgba(69, 26, 3, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }
    .neon-rose, .card-accent-rose {
        border-left: 4px solid #f43f5e !important;
        background: linear-gradient(135deg, rgba(76, 5, 25, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }
    .card-accent-purple {
        border-left: 4px solid #a855f7 !important;
        background: linear-gradient(135deg, rgba(59, 7, 100, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    }

    /* Top Studio Command Bar */
    .studio-bar {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 14px;
        padding: 12px 20px;
        margin-bottom: 1.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    /* Modern Pipeline Tracker */
    .pipeline-track {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 9px 14px;
        background: rgba(3, 7, 18, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        overflow-x: auto;
        min-width: 820px;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
    }

    .pipeline-step {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 5px 11px;
        border-radius: 8px;
        white-space: nowrap;
        color: #64748b;
        background: transparent;
        transition: all 0.2s ease;
    }

    .pipeline-step.active {
        background: rgba(99, 102, 241, 0.25);
        color: #c7d2fe;
        border: 1px solid #6366f1;
        box-shadow: 0 0 14px rgba(99, 102, 241, 0.45);
    }

    .pipeline-step.completed {
        background: rgba(16, 185, 129, 0.18);
        color: #6ee7b7;
        border: 1px solid #10b981;
    }

    .pipeline-arrow {
        color: #334155;
        font-size: 0.75rem;
    }

    /* Badges & Pills */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 11px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-indigo { background: rgba(99, 102, 241, 0.22); color: #c7d2fe; border: 1px solid rgba(99, 102, 241, 0.45); }
    .badge-cyan { background: rgba(6, 182, 212, 0.22); color: #a5f3fc; border: 1px solid rgba(6, 182, 212, 0.45); }
    .badge-green { background: rgba(16, 185, 129, 0.22); color: #a7f3d0; border: 1px solid rgba(16, 185, 129, 0.45); }
    .badge-amber { background: rgba(245, 158, 11, 0.22); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.45); }
    .badge-red { background: rgba(239, 68, 68, 0.22); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.45); }
    .badge-gray { background: rgba(51, 65, 85, 0.45); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.09); }
    .badge-purple { background: rgba(168, 85, 247, 0.22); color: #e9d5ff; border: 1px solid rgba(168, 85, 247, 0.45); }
    .badge-blue { background: rgba(59, 130, 246, 0.22); color: #bfdbfe; border: 1px solid rgba(59, 130, 246, 0.45); }

    /* macOS Terminal Window Frame */
    .terminal-window {
        background: #070c18;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        overflow: hidden;
        margin: 1.2rem 0;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
    }

    .terminal-header {
        background: #0f172a;
        padding: 9px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .terminal-dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-red { background: #ef4444; box-shadow: 0 0 6px rgba(239, 68, 68, 0.6); }
    .dot-yellow { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.6); }
    .dot-green { background: #10b981; box-shadow: 0 0 6px rgba(16, 185, 129, 0.6); }

    .terminal-title {
        font-size: 0.76rem;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 8px;
        letter-spacing: 0.03em;
    }

    .terminal-body {
        padding: 16px 20px;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.65;
        margin: 0;
        background: #030712;
        overflow-x: auto;
    }

    /* 3D Glass Flashcard */
    .flashcard-3d, .flashcard {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.65) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 20px;
        padding: 2.8rem 2.2rem;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 14px 45px rgba(0, 0, 0, 0.55), 0 0 20px rgba(99, 102, 241, 0.15);
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .flashcard-topic {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #a5b4fc;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .flashcard-question-text, .flashcard-content {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.55;
    }

    /* Metric Glass Pill & KPI Tile */
    .kpi-tile, .metric-pill {
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .kpi-tile:hover, .metric-pill:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    .kpi-title, .metric-label {
        font-size: 0.73rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-val, .metric-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 4px;
        letter-spacing: -0.01em;
    }

    /* Callout Card */
    .guidance-box {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 27, 75, 0.75) 100%);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 14px;
        padding: 18px 24px;
        margin-top: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }

    /* Sidebar adjustments */
    section[data-testid="stSidebar"] {
        background-color: #040816 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    /* Interactive Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(6, 182, 212, 0.45) !important;
    }

    .stButton > button[kind="secondary"] {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #6366f1 !important;
        color: #ffffff !important;
        background: rgba(30, 27, 75, 0.6) !important;
    }

    /* Form inputs */
    input[type="text"], input[type="password"], textarea, select {
        background-color: #090e1c !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
    }

    /* Streamlit metrics styling */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.72) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: #94a3b8 !important;
    }

    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.25) !important;
        color: #ffffff !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }
    ::-webkit-scrollbar-track {
        background: #030712;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    .dashboard-footer {
        text-align: center;
        color: #64748b;
        font-size: 0.84rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.07);
        margin-top: 3.5rem;
    }
    </style>
    """

def render_studio_banner(team_no="11", venue="MB306", problem="Problem 21", theme="Theme E: Applied Prompt-Based Workflows"):
    """
    Renders the modern Cyber-Glass Studio Command Bar for Problem 21 Hackathon.
    """
    return f"""
    <div class="studio-bar">
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <span class="badge badge-indigo" style="font-size: 0.8rem; padding: 4px 10px;">⚡ {problem}</span>
            <span style="color: #f8fafc; font-size: 1.15rem; font-weight: 800; letter-spacing: -0.01em;">
                PyPedagogy <span style="background: linear-gradient(135deg, #818cf8 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Studio</span>
            </span>
            <span class="badge badge-cyan" style="font-size: 0.72rem;">Obsidian Cyber-Glass UI</span>
            <span class="badge badge-gray" style="font-size: 0.72rem;">{theme}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px; font-size: 0.86rem; color: #94a3b8; flex-wrap: wrap;">
            <span>Team: <strong style="color: #38bdf8; font-weight: 700;">{team_no}</strong></span>
            <span style="color: #334155;">•</span>
            <span>Venue: <strong style="color: #38bdf8; font-weight: 700;">{venue}</strong></span>
            <span style="color: #334155;">•</span>
            <span class="badge badge-green">● Live Autonomous Engine</span>
        </div>
    </div>
    """

def render_workflow_bar(active_step="learn"):
    """
    Renders the exact 9-step workflow required:
    User Input -> Difficulty Selection -> AI Explanation -> Quiz -> Accuracy
    -> Diagnostic Assessment -> Weak Topic Detection -> Personalised Learning Path -> Revision Plan
    """
    steps = [
        ("input", "1. Input"),
        ("difficulty", "2. Level"),
        ("learn", "3. Lesson"),
        ("quiz", "4. Quiz (5 Items)"),
        ("accuracy", "5. Accuracy"),
        ("diagnostic", "6. Diagnostic"),
        ("weakness", "7. Weak Topics"),
        ("roadmap", "8. Learning Path"),
        ("revision", "9. Revision Plan"),
    ]

    step_order = ["input", "difficulty", "learn", "quiz", "accuracy", "diagnostic", "weakness", "roadmap", "revision"]
    curr_idx = step_order.index(active_step) if active_step in step_order else 2

    html = '<div style="margin-bottom: 1.3rem; overflow-x: auto;"><div class="pipeline-track">'
    for i, (key, label) in enumerate(steps):
        if i < curr_idx:
            status = "completed"
            icon = "✓"
        elif i == curr_idx:
            status = "active"
            icon = "●"
        else:
            status = "pending"
            icon = "○"

        html += f'<div class="pipeline-step {status}"><span>{icon}</span> {label}</div>'
        if i < len(steps) - 1:
            html += '<span class="pipeline-arrow">➔</span>'

    html += '</div></div>'
    return html

def render_header(title, subtitle, icon="🧠", step_badge_text="", step_number=""):
    """
    Renders standard section header with badge support.
    Accepts both step_badge_text and step_number for safe compatibility.
    """
    badge_val = step_badge_text or step_number
    badge_html = f'<span class="badge badge-indigo" style="margin-right: 8px;">{badge_val}</span>' if badge_val else ''
    return f"""
    <div style="margin-bottom: 1.4rem;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 10px; letter-spacing: -0.02em;">
            <span>{icon}</span> {badge_html}{title}
        </h1>
        <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 1rem; line-height: 1.5;">{subtitle}</p>
    </div>
    """

def render_next_step(title, description, button_text=""):
    return f"""
    <div class="guidance-box">
        <div>
            <div style="font-size: 0.74rem; text-transform: uppercase; color: #a5b4fc; font-weight: 800; letter-spacing: 0.08em;">NEXT IN WORKFLOW PIPELINE</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 1.12rem; margin-top: 3px;">{title}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; margin-top: 3px;">{description}</div>
        </div>
    </div>
    """

def render_terminal_output(code_output_text, title="terminal ~ python3 execution_trace.py"):
    """
    Renders code output in a stylish macOS-style terminal window.
    """
    return f"""
    <div class="terminal-window">
        <div class="terminal-header">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
            <span class="terminal-title">{title}</span>
        </div>
        <pre class="terminal-body">{code_output_text}</pre>
    </div>
    """
