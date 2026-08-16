import random
import time
import streamlit as st
from src.data_loader import load_data
from src.database import (
    get_global_leaderboard,
    get_user_career_stats,
    init_db,
    login_user,
    register_user,
    save_user_score,
)
from src.draft import create_team
from src.simulation import simulate_season

# Initialize database
init_db()

st.set_page_config(
    page_title="Apex Grand Prix: F1 Draft Manager",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# ENHANCED F1 DARK THEME & STYLING OVERHAUL
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

header[data-testid="stHeader"] { display: none !important; }
footer { visibility: hidden; }

.stApp {
    background: linear-gradient(180deg, #090A0F 0%, #12151E 100%);
    color: #F1F5F9;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 100% !important;
}

div[data-testid="stTable"] th,
div[data-testid="stTable"] td {
    text-align: center !important;
}

/* Brand Headers */
.brand-hero {
    text-align: center;
    padding: 1.8rem 1rem 1.2rem 1rem;
    background: radial-gradient(circle at center, rgba(225, 6, 0, 0.18) 0%, rgba(15, 23, 42, 0) 70%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 1.8rem;
}
.brand-title {
    color: #FF1801 !important;
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.08em;
    margin-bottom: 4px !important;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(225, 6, 0, 0.4);
}
.brand-subtitle {
    color: #94A3B8;
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 650px;
    margin: 0 auto;
}

/* Section Titles */
h1 {
    font-weight: 900 !important;
    color: #FFFFFF !important;
    text-align: center;
    letter-spacing: 1px;
    font-size: 2.2rem !important;
    margin-bottom: 4px !important;
}
h2 {
    font-weight: 800 !important;
    color: #FFFFFF !important;
    font-size: 1.4rem !important;
    margin-top: 1rem !important;
    margin-bottom: 0.8rem !important;
    border-bottom: 2px solid #E10600;
    padding-bottom: 6px;
}
h3 {
    font-weight: 700 !important;
    color: #FFC107 !important;
    font-size: 1.15rem !important;
    margin-top: 0.8rem !important;
    margin-bottom: 0.5rem !important;
}
h4 {
    font-weight: 700 !important;
    color: #94A3B8 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px !important;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-weight: 500;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

/* Cards & Panels */
.mode-box, .ui-panel {
    background-color: #141721;
    border: 1px solid #232838;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.stat-card {
    background: #141721;
    border: 1px solid #232838;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}
.stat-card .val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 800;
    color: #FFC107;
}
.stat-card .lbl {
    font-size: 0.78rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

.driver-card {
    background: #181C28;
    border: 1px solid #282E40;
    border-left: 4px solid #E10600;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}
.driver-card h3 {
    margin: 0 !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
}
.driver-meta {
    color: #94A3B8;
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 4px;
}

.ovr-badge {
    background: linear-gradient(135deg, #FFC107 0%, #FF8F00 100%);
    color: #0A0C10;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 900;
    font-size: 0.82rem;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-top: 8px;
}

.vacant-card {
    background: #0E1017;
    border: 1px dashed #2E3446;
    border-radius: 10px;
    color: #64748B;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

/* Custom Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(135deg, #2A3042 0%, #1E2333 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #3A4259 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.2rem !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton > button:hover {
    border-color: #E10600 !important;
    transform: translateY(-1px);
}

div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #E10600 0%, #B80500 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 14px rgba(225, 6, 0, 0.35) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #FF1801 0%, #D10500 100%) !important;
    box-shadow: 0 6px 20px rgba(225, 6, 0, 0.45) !important;
}

.info-pill {
    background: #0F172A;
    color: #38BDF8;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.88rem;
    margin-bottom: 14px;
}

.stTextInput>div>div>input {
    background-color: #1A1D27 !important;
    border: 1px solid #2E3446 !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
    padding: 10px 14px !important;
}
.stTextInput>div>div>input:focus {
    border-color: #E10600 !important;
    box-shadow: 0 0 10px rgba(225, 6, 0, 0.3) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ========== DATA & SESSION STATE ==========
drivers, principals, cars = load_data()

if "current_page" not in st.session_state:
    st.session_state.current_page = "game"  # "game" or "account"

if "user" not in st.session_state:
    st.session_state.user = None

if "draft" not in st.session_state:
    st.session_state.draft = {"d1": None, "d2": None, "car": None, "p": None}
if "available" not in st.session_state:
    st.session_state.available = drivers.copy()
if "result" not in st.session_state:
    st.session_state.result = None

# Track slot machine rolled years
if "rolled_year_d1" not in st.session_state:
    st.session_state.rolled_year_d1 = None
if "rolled_year_d2" not in st.session_state:
    st.session_state.rolled_year_d2 = None
if "rolled_year_car" not in st.session_state:
    st.session_state.rolled_year_car = None
if "rolled_year_p" not in st.session_state:
    st.session_state.rolled_year_p = None

if "team_name" not in st.session_state:
    st.session_state.team_name = "My Racing Team"
if "rerolls_left" not in st.session_state:
    st.session_state.rerolls_left = 1

# ==================== TOP NAVIGATION HEADER ====================
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    if st.button("🎮 Play / Draft", use_container_width=True):
        st.session_state.current_page = "game"
        st.rerun()

with top_col2:
    account_label = (
        "👤 My Account"
        if not st.session_state.user
        else f"👤 {st.session_state.user['username']}"
    )
    if st.button(
        account_label,
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.current_page == "account"
            else "secondary"
        ),
    ):
        st.session_state.current_page = "account"
        st.rerun()

st.markdown(
    "<hr style='border: none; border-top: 1px solid #232838; margin: 10px 0 20px 0;'>",
    unsafe_allow_html=True,
)

# ==============================================================================
# PAGE 1: ACCOUNT & "YOUR 24-0" PROFILE
# ==============================================================================
if st.session_state.current_page == "account":
    st.markdown("<h1>👤 PADDOCK CAREER HUB</h1>", unsafe_allow_html=True)

    if st.session_state.user is None:
        st.markdown(
            '<p class="subtitle">Log in or sign up to access your F1'
            ' career stats and save your season records.</p>',
            unsafe_allow_html=True,
        )

        tab_login, tab_signup = st.tabs(["🔒 Log In", "📝 Sign Up"])

        with tab_login:
            login_u = st.text_input("Username", key="acc_login_u")
            login_p = st.text_input("Password", type="password", key="acc_login_p")
            if st.button("Log In", type="primary", use_container_width=True):
                success, res = login_user(login_u, login_p)
                if success:
                    st.session_state.user = res
                    st.success(f"Welcome back, {res['username']}!")
                    st.rerun()
                else:
                    st.error(res)

        with tab_signup:
            signup_u = st.text_input("Choose Username", key="acc_signup_u")
            signup_p = st.text_input(
                "Choose Password", type="password", key="acc_signup_p"
            )
            if st.button("Create Account", type="primary", use_container_width=True):
                success, msg = register_user(signup_u, signup_p)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    else:
        # LOGGED IN CAREER DASHBOARD
        u_id = st.session_state.user["id"]
        username = st.session_state.user["username"]

        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.markdown("## 🏁 Your 24-0 Career Statistics")
        with c_right:
            if st.button("🚪 Log Out", use_container_width=True):
                st.session_state.user = None
                st.rerun()

        stats = get_user_career_stats(u_id)

        if not stats:
            st.info(
                "👋 You haven't completed any season simulations yet! Return to the"
                " draft page and complete a season to generate your 'Your 24-0' career"
                " stats."
            )
        else:
            # METRICS GRID
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["total_wins"]}</div><div class="lbl">Race'
                    " Wins</div></div>",
                    unsafe_allow_html=True,
                )
            with m2:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["wdc_count"]}</div><div class="lbl">WDC'
                    " Titles</div></div>",
                    unsafe_allow_html=True,
                )
            with m3:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["wcc_count"]}</div><div class="lbl">WCC'
                    " Titles</div></div>",
                    unsafe_allow_html=True,
                )
            with m4:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["podium_count"]}</div><div'
                    ' class="lbl">Podium Finishes</div></div>',
                    unsafe_allow_html=True,
                )

            m5, m6, m7, m8 = st.columns(4)
            with m5:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["win_rate"]}%</div><div class="lbl">Win'
                    " Rate</div></div>",
                    unsafe_allow_html=True,
                )
            with m6:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["avg_points"]}</div><div class="lbl">Avg Pts'
                    " / Season</div></div>",
                    unsafe_allow_html=True,
                )
            with m7:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["highest_score"]}</div><div'
                    ' class="lbl">Best Season Pts</div></div>',
                    unsafe_allow_html=True,
                )
            with m8:
                st.markdown(
                    '<div class="stat-card"><div'
                    f' class="val">{stats["seasons_played"]}</div><div'
                    ' class="lbl">Seasons Played</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("### 🌟 Most Frequent Roster Selections")
            f1, f2, f3 = st.columns(3)
            with f1:
                st.markdown(
                    '<div class="mode-box" style="text-align: center;"><p'
                    ' style="color:#94A3B8; margin:0; font-size:0.85rem;">MOST USED'
                    ' DRIVER</p><h3 style="margin:6px 0 0'
                    f' 0;">{stats["most_used_driver"]}</h3></div>',
                    unsafe_allow_html=True,
                )
            with f2:
                st.markdown(
                    '<div class="mode-box" style="text-align: center;"><p'
                    ' style="color:#94A3B8; margin:0; font-size:0.85rem;">MOST USED'
                    ' CHASSIS</p><h3 style="margin:6px 0 0'
                    f' 0;">{stats["most_used_car"]}</h3></div>',
                    unsafe_allow_html=True,
                )
            with f3:
                st.markdown(
                    '<div class="mode-box" style="text-align: center;"><p'
                    ' style="color:#94A3B8; margin:0; font-size:0.85rem;">MOST USED'
                    ' PRINCIPAL</p><h3 style="margin:6px 0 0'
                    f' 0;">{stats["most_used_principal"]}</h3></div>',
                    unsafe_allow_html=True,
                )

            # ALL-TIME SEASON ARCHIVE & VIEWER
            st.markdown("### 📜 All-Time Season Archive & Replays")

            season_labels = [
                f"Season #{idx+1} — {run[1]} ({run[6]} Pts, P{run[7]}, {run[8]} Wins)"
                f" [{run[13][:10]}]"
                for idx, run in enumerate(reversed(stats["history"]))
            ]
            season_labels.reverse()  # Most recent first

            selected_season_str = st.selectbox(
                "Select Season to View Details:", season_labels
            )

            if selected_season_str:
                selected_idx = season_labels.index(selected_season_str)
                selected_run = stats["history"][selected_idx]

                # Render season detailed card
                st.markdown(
                    f"""
                    <div class="mode-box">
                        <h3 style="margin-top:0; color:#FFC107 !important;">🔍 Detailed Season Recap: {selected_run[1]}</h3>
                        <p style="margin:4px 0;"><b>Drivers:</b> {selected_run[2]} & {selected_run[3]}</p>
                        <p style="margin:4px 0;"><b>Chassis:</b> {selected_run[4]}</p>
                        <p style="margin:4px 0;"><b>Team Principal:</b> {selected_run[5]}</p>
                        <hr style="border-color:#232838; margin:10px 0;"/>
                        <p style="margin:4px 0;"><b>Constructors Finish:</b> P{selected_run[7]}</p>
                        <p style="margin:4px 0;"><b>Total Points:</b> {selected_run[6]} PTS</p>
                        <p style="margin:4px 0;"><b>Race Victories:</b> {selected_run[8]} WINS</p>
                        <p style="margin:4px 0;"><b>Podiums:</b> {selected_run[9]}</p>
                        <p style="margin:4px 0;"><b>Drivers Title (WDC):</b> {'🏆 Won' if selected_run[10] else '❌ No'}</p>
                        <p style="margin:4px 0;"><b>Constructors Title (WCC):</b> {'🏆 Won' if selected_run[11] else '❌ No'}</p>
                        <p style="margin:4px 0; color:#94A3B8; font-size:0.85rem;"><b>Public Leaderboard Status:</b> {'Public' if selected_run[14] else 'Private'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### 📊 Complete Season History Table")
            history_table = []
            for run in stats["history"]:
                history_table.append({
                    "Date": run[13][:10],
                    "Team": run[1],
                    "Lineup": f"{run[2]} & {run[3]}",
                    "Chassis": run[4],
                    "Finish": f"P{run[7]}",
                    "Wins": run[8],
                    "Points": run[6],
                    "Public": "Yes" if run[14] else "No",
                })
            st.table(history_table)

# ==============================================================================
# PAGE 2: MAIN GAME / DRAFT ENGINE
# ==============================================================================
else:
    # ========== HEADER ==========
    st.markdown(
        """
        <div class="brand-hero">
            <div class="brand-title">APEX GRAND PRIX</div>
            <div class="brand-subtitle">Draft two drivers, an iconic car chassis, and a Team Principal. Conquer the grid.</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # ========== LEADERBOARD AT TOP ==========
    st.markdown("## 🏆 Global Hall of Fame Leaderboard")
    global_board = get_global_leaderboard()
    if global_board:
        leaderboard_view = []
        for rank, entry in enumerate(global_board, 1):
            leaderboard_view.append({
                "Rank": f"#{rank}",
                "Player": entry[0],
                "Team": entry[1],
                "Lineup": entry[2],
                "Car": entry[3],
                "Points": entry[4],
                "Finish": f"P{entry[5]}",
            })
        st.table(leaderboard_view)
    else:
        st.caption(
            "No public records logged yet. Opt-in after completing a simulation to"
            " feature on the Global Leaderboard!"
        )

    st.markdown(
        "<hr style='border: none; border-top: 1px solid #232838; margin: 20px 0 24px 0;'>",
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns(2, gap="large")

    # ==================== LEFT COLUMN: GARAGE ====================
    with left_col:
        st.markdown("## 🛠️ Current Garage")

        st.markdown("#### Driver 1")
        if st.session_state.draft["d1"] is None:
            st.markdown(
                '<div class="vacant-card">➕ VACANT DRIVER SLOT</div>',
                unsafe_allow_html=True,
            )
        else:
            d = st.session_state.draft["d1"]
            st.markdown(
                f'<div class="driver-card"><h3>{d.name}</h3><div'
                f' class="driver-meta">{d.team} • {d.year}</div><div'
                f' class="ovr-badge">OVR {d.ovr}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Driver 2")
        if st.session_state.draft["d2"] is None:
            st.markdown(
                '<div class="vacant-card">➕ VACANT DRIVER SLOT</div>',
                unsafe_allow_html=True,
            )
        else:
            d = st.session_state.draft["d2"]
            st.markdown(
                f'<div class="driver-card"><h3>{d.name}</h3><div'
                f' class="driver-meta">{d.team} • {d.year}</div><div'
                f' class="ovr-badge">OVR {d.ovr}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Car Chassis")
        if st.session_state.draft["car"] is None:
            st.markdown(
                '<div class="vacant-card">➕ VACANT CHASSIS SLOT</div>',
                unsafe_allow_html=True,
            )
        else:
            c = st.session_state.draft["car"]
            st.markdown(
                f'<div class="driver-card"><h3>{c.name}</h3><div'
                f' class="driver-meta">{c.team} • {c.year}</div><div'
                f' class="ovr-badge">OVR {c.ovr}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Team Principal")
        if st.session_state.draft["p"] is None:
            st.markdown(
                '<div class="vacant-card">➕ VACANT PRINCIPAL SLOT</div>',
                unsafe_allow_html=True,
            )
        else:
            p = st.session_state.draft["p"]
            st.markdown(
                f'<div class="driver-card"><h3>{p.name}</h3><div'
                f' class="driver-meta">{p.special}</div><div class="ovr-badge">OVR'
                f" {p.ovr}</div></div>",
                unsafe_allow_html=True,
            )

    # ==================== RIGHT COLUMN: DRAFT SECTOR ====================
    with right_col:
        st.markdown("## 🎯 Live Sector")

        st.session_state.team_name = st.text_input(
            "Team Name",
            value=st.session_state.team_name,
            max_chars=25,
            help=(
                "Customize your team's franchise name displayed on timing sheets"
                " and standings."
            ),
        )

        st.markdown(
            '<div class="info-pill">🔄 <b>Available Re-rolls:'
            f" {st.session_state.rerolls_left}</b> &nbsp;|&nbsp; <i>Use re-rolls"
            " to spin again.</i></div>",
            unsafe_allow_html=True,
        )

        active_slot = None
        if st.session_state.draft["d1"] is None:
            active_slot = "d1"
        elif st.session_state.draft["d2"] is None:
            active_slot = "d2"
        elif st.session_state.draft["car"] is None:
            active_slot = "car"
        elif st.session_state.draft["p"] is None:
            active_slot = "p"

        if active_slot is None:
            st.info(
                "✅ Draft sequence complete! Click the button below to launch the"
                " season simulation engine."
            )

        elif active_slot == "d1":
            st.markdown("### Drafting Driver 1")
            if st.session_state.rolled_year_d1 is None:
                if st.button(
                    "🎲 Spin Season Matrix",
                    use_container_width=True,
                    key="spin_btn_d1",
                    type="primary",
                ):
                    available_years = list(
                        set([d.year for d in st.session_state.available])
                    )
                    if available_years:
                        placeholder = st.empty()
                        for i in range(1, 10):
                            ticker_year = random.choice(available_years)
                            placeholder.markdown(
                                '<div class="driver-card" style="text-align: center;"><h2'
                                ' style="margin:0; color:#FFC107 !important;'
                                f' border:none;">{ticker_year}</h2></div>',
                                unsafe_allow_html=True,
                            )
                            time.sleep(i * 0.03)
                        placeholder.empty()
                        st.session_state.rolled_year_d1 = random.choice(available_years)
                        st.rerun()
            else:
                year = st.session_state.rolled_year_d1
                st.markdown(f"**Rolled Season Matrix:** `{year}`")

                if st.session_state.rerolls_left > 0:
                    if st.button(
                        "🔄 Expend Re-roll Token",
                        key="re_d1",
                        use_container_width=True,
                        help=(
                            "Discard this rolled season and roll for a new year matrix."
                        ),
                    ):
                        st.session_state.rolled_year_d1 = None
                        st.session_state.rerolls_left -= 1
                        st.rerun()

                st.write("Select a driver profile to lock in Driver 1:")
                drivers_in_year = [
                    d for d in st.session_state.available if d.year == year
                ]
                for target_driver in drivers_in_year:
                    card_label = (
                        f"{target_driver.name} | {target_driver.team} (OVR"
                        f" {target_driver.ovr})"
                    )
                    if st.button(
                        card_label,
                        use_container_width=True,
                        key=f"select_d1_{target_driver.name}",
                    ):
                        st.session_state.draft["d1"] = target_driver
                        st.session_state.available = [
                            item
                            for item in st.session_state.available
                            if item.name != target_driver.name
                        ]
                        st.rerun()

        elif active_slot == "d2":
            st.markdown("### Drafting Driver 2")
            if st.session_state.rolled_year_d2 is None:
                if st.button(
                    "🎲 Spin Season Matrix",
                    use_container_width=True,
                    key="spin_btn_d2",
                    type="primary",
                ):
                    available_years = list(
                        set([d.year for d in st.session_state.available])
                    )
                    if available_years:
                        placeholder = st.empty()
                        for i in range(1, 10):
                            ticker_year = random.choice(available_years)
                            placeholder.markdown(
                                '<div class="driver-card" style="text-align: center;"><h2'
                                ' style="margin:0; color:#FFC107 !important;'
                                f' border:none;">{ticker_year}</h2></div>',
                                unsafe_allow_html=True,
                            )
                            time.sleep(i * 0.03)
                        placeholder.empty()
                        st.session_state.rolled_year_d2 = random.choice(available_years)
                        st.rerun()
            else:
                year = st.session_state.rolled_year_d2
                st.markdown(f"**Rolled Season Matrix:** `{year}`")

                if st.session_state.rerolls_left > 0:
                    if st.button(
                        "🔄 Expend Re-roll Token",
                        key="re_d2",
                        use_container_width=True,
                        help=(
                            "Discard this rolled season and roll for a new year matrix."
                        ),
                    ):
                        st.session_state.rolled_year_d2 = None
                        st.session_state.rerolls_left -= 1
                        st.rerun()

                st.write("Select a driver profile to lock in Driver 2:")
                drivers_in_year = [
                    d for d in st.session_state.available if d.year == year
                ]
                for target_driver in drivers_in_year:
                    card_label = (
                        f"{target_driver.name} | {target_driver.team} (OVR"
                        f" {target_driver.ovr})"
                    )
                    if st.button(
                        card_label,
                        use_container_width=True,
                        key=f"select_d2_{target_driver.name}",
                    ):
                        st.session_state.draft["d2"] = target_driver
                        st.session_state.available = [
                            item
                            for item in st.session_state.available
                            if item.name != target_driver.name
                        ]
                        st.rerun()

        elif active_slot == "car":
            st.markdown("### Drafting Car Chassis")
            if st.session_state.rolled_year_car is None:
                if st.button(
                    "🎲 Spin Car Matrix",
                    use_container_width=True,
                    key="spin_btn_car",
                    type="primary",
                ):
                    available_years = list(set([c.year for c in cars]))
                    if available_years:
                        placeholder = st.empty()
                        for i in range(1, 10):
                            ticker_year = random.choice(available_years)
                            placeholder.markdown(
                                '<div class="driver-card" style="text-align: center;"><h2'
                                ' style="margin:0; color:#FFC107 !important;'
                                f' border:none;">{ticker_year}</h2></div>',
                                unsafe_allow_html=True,
                            )
                            time.sleep(i * 0.03)
                        placeholder.empty()
                        st.session_state.rolled_year_car = random.choice(available_years)
                        st.rerun()
            else:
                year = st.session_state.rolled_year_car
                st.markdown(f"**Rolled Chassis Matrix:** `{year}`")

                if st.session_state.rerolls_left > 0:
                    if st.button(
                        "🔄 Expend Re-roll Token",
                        key="re_car",
                        use_container_width=True,
                        help=(
                            "Discard this rolled car season and roll for a new chassis"
                            " matrix."
                        ),
                    ):
                        st.session_state.rolled_year_car = None
                        st.session_state.rerolls_left -= 1
                        st.rerun()

                st.write("Select a car chassis:")
                cars_in_year = [c for c in cars if c.year == year]
                for target_car in cars_in_year:
                    card_label = (
                        f"{target_car.name} | {target_car.team} (OVR {target_car.ovr})"
                    )
                    if st.button(
                        card_label,
                        use_container_width=True,
                        key=f"select_car_{target_car.name}",
                    ):
                        st.session_state.draft["car"] = target_car
                        st.rerun()

        elif active_slot == "p":
            st.markdown("### Drafting Team Principal")
            if st.session_state.rolled_year_p is None:
                if st.button(
                    "🎲 Spin Management Matrix",
                    use_container_width=True,
                    key="spin_btn_p",
                    type="primary",
                ):
                    available_years = list(set([p.year for p in principals]))
                    if available_years:
                        placeholder = st.empty()
                        for i in range(1, 10):
                            ticker_year = random.choice(available_years)
                            placeholder.markdown(
                                '<div class="driver-card" style="text-align: center;"><h2'
                                ' style="margin:0; color:#FFC107 !important;'
                                f' border:none;">{ticker_year}</h2></div>',
                                unsafe_allow_html=True,
                            )
                            time.sleep(i * 0.03)
                        placeholder.empty()
                        st.session_state.rolled_year_p = random.choice(available_years)
                        st.rerun()
            else:
                year = st.session_state.rolled_year_p
                st.markdown(f"**Rolled Management Matrix:** `{year}`")

                if st.session_state.rerolls_left > 0:
                    if st.button(
                        "🔄 Expend Re-roll Token",
                        key="re_p",
                        use_container_width=True,
                        help=(
                            "Discard this rolled season and roll for a new year matrix."
                        ),
                    ):
                        st.session_state.rolled_year_p = None
                        st.session_state.rerolls_left -= 1
                        st.rerun()

                st.write("Select a principal profile to lock in management:")
                principals_in_year = [p for p in principals if p.year == year]
                for target_p in principals_in_year:
                    card_label = (
                        f"{target_p.name} | {target_p.special} (OVR {target_p.ovr})"
                    )
                    if st.button(
                        card_label,
                        use_container_width=True,
                        key=f"select_p_{target_p.name}",
                    ):
                        st.session_state.draft["p"] = target_p
                        st.rerun()

    st.markdown(
        "<hr style='border: none; border-top: 1px solid #232838; margin: 24px 0 20px 0;'>",
        unsafe_allow_html=True,
    )

    # ========== SIMULATION RUN ENGINE ==========
    if all(st.session_state.draft.values()):
        if st.button(
            "🚀 SIMULATE FULL SEASON", type="primary", use_container_width=True
        ):
            team = create_team(
                st.session_state.draft["d1"],
                st.session_state.draft["d2"],
                st.session_state.draft["car"],
                st.session_state.draft["p"],
            )
            team.name = st.session_state.team_name

            sim_data = simulate_season(team)

            st.markdown("## 🏎️ Live Race Simulation Feed")
            live_log = st.empty()
            d1_acc, d2_acc = 0, 0

            # Calculate podium finishes
            podiums_count = 0
            for idx in range(len(sim_data["races"])):
                p1 = sim_data["d1_pts_list"][idx]
                p2 = sim_data["d2_pts_list"][idx]
                if p1 in [25, 18, 15]:
                    podiums_count += 1
                if p2 in [25, 18, 15]:
                    podiums_count += 1

            for idx, race in enumerate(sim_data["races"]):
                d1_acc += sim_data["d1_pts_list"][idx]
                d2_acc += sim_data["d2_pts_list"][idx]

                live_log.markdown(
                    f"""
                       <div class="mode-box" style="text-align: center; border-left: 4px solid #E10600;">
                           <h3 style="color: #FFC107 !important; margin: 0;">ROUND {idx+1}: GRAND PRIX OF {race.upper()}</h3>
                           <hr style="border-color: #232838; margin: 12px 0;"/>
                           <p style="font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; color: #FFFFFF; margin: 4px 0;">
                               <b>{sim_data['d1_name']}</b>: +{sim_data['d1_pts_list'][idx]} PTS (Total: {d1_acc} PTS)
                           </p>
                           <p style="font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; color: #FFFFFF; margin: 4px 0;">
                               <b>{sim_data['d2_name']}</b>: +{sim_data['d2_pts_list'][idx]} PTS (Total: {d2_acc} PTS)
                           </p>
                       </div>
                   """,
                    unsafe_allow_html=True,
                )
                time.sleep(0.35)

            live_log.empty()
            st.session_state.result = sim_data
            st.session_state.podiums_count = podiums_count
            st.rerun()

    # ========== RESULTS SECTION ==========
    if st.session_state.result:
        res = st.session_state.result
        st.markdown("## 📊 Season Statistics & Performance Summary")

        won_wcc = res["c_pos"] == 1
        user_drivers = [res["d1_name"], res["d2_name"]]
        won_wdc = res["driver_standings"][0][0] in user_drivers

        if won_wcc or won_wdc:
            d1_pts_total = sum(res["d1_pts_list"])
            d2_pts_total = sum(res["d2_pts_list"])
            star_driver = (
                res["d1_name"] if d1_pts_total >= d2_pts_total else res["d2_name"]
            )
            champion_driver = res["driver_standings"][0][0]

            if won_wcc and won_wdc:
                broadcast_quote = (
                    f"{star_driver.upper()} WINS THE GRAND PRIX AND SECURES THE DRIVERS'"
                    f" CHAMPIONSHIP IN THE {res['car_name'].upper()}!"
                    f" {res['team_name'].upper()} ARE THE CONSTRUCTORS' CHAMPIONS OF"
                    " THE WORLD!"
                )
            elif won_wcc and not won_wdc:
                broadcast_quote = (
                    f"{champion_driver.upper()} SEALS THE DRIVERS' TITLE AT THE FINISH"
                    f" LINE! BUT {res['team_name'].upper()} CLINCH THE CONSTRUCTORS'"
                    f" CHAMPIONSHIP WITH THE {res['car_name'].upper()}!"
                )
            else:
                broadcast_quote = (
                    f"{star_driver.upper()} CROSSES THE LINE TO BECOME THE DRIVERS'"
                    f" CHAMPION OF THE WORLD IN THE {res['car_name'].upper()}!"
                )

            st.markdown(
                f"""
               <div style="background: #141721; border: 2px solid #FFC107; border-radius: 12px; padding: 22px; text-align: center; margin-bottom: 20px;">
                   <h1 style="color: #FFC107 !important; font-size: 2rem !important; margin: 0 0 10px 0 !important;">🏆 CHAMPIONSHIP LAURELS SECURED 🏆</h1>
                   <p style="color: #94A3B8; font-size: 0.9rem; font-weight: 600; margin-bottom: 12px;">TRACKSIDE TEAM RADIO TRANSMISSION:</p>
                   <p style="font-family: 'JetBrains Mono', monospace; color: #FFFFFF; font-style: italic; font-size: 0.95rem; line-height: 1.6; max-width: 650px; margin: 0 auto; background: #0B0D13; padding: 14px; border-radius: 8px; border: 1px dashed #E10600;">"{broadcast_quote}"</p>
               </div>
               """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
           <div class="mode-box">
               <h3 style="margin-top:0; color:#FFFFFF !important; font-size: 1.2rem;">Official Timing Analysis: {res['team_name']}</h3>
               <p style="font-size: 0.95rem; color: #E0E0E6; margin: 6px 0;"><b>Constructors Position:</b> P{res['c_pos']}</p>
               <p style="font-size: 0.95rem; color: #E0E0E6; margin: 6px 0;"><b>Car Chassis:</b> {res['car_name']}</p>
               <p style="font-size: 0.95rem; color: #E0E0E6; margin: 6px 0;"><b>Total Points Accounted:</b> {res['total_points']} PTS</p>
               <p style="font-size: 0.95rem; color: #E0E0E6; margin: 6px 0;"><b>Total Race Victories:</b> {res['wins']} WINS</p>
               <div style="background:#0B0D13; padding:12px; border-radius:8px; border:1px solid #232838; color:#E0E0E6; font-size:0.9rem; margin-top:12px; line-height:1.5;">
                   <b>Season Debrief:</b> {res['feedback']}
               </div>
           </div>
           """,
            unsafe_allow_html=True,
        )

        # ==================== CHAMPIONSHIP STANDINGS & RACE BREAKDOWN ====================
        st.markdown("## 🏁 Official Championship Standings & Round Results")

        tab_wdc, tab_wcc, tab_rounds = st.tabs([
            "🏎️ Drivers' Championship (WDC)",
            "🏭 Constructors' Championship (WCC)",
            "🏁 Round-by-Round Breakdown",
        ])

        with tab_wdc:
            st.markdown("### World Drivers' Championship Final Standings")
            wdc_table = []
            for rank, (driver_name, pts, team_name) in enumerate(
                res["driver_standings"], 1
            ):
                is_user_driver = driver_name in user_drivers
                highlight = " ⭐ (Yours)" if is_user_driver else ""
                wdc_table.append({
                    "Pos": f"P{rank}",
                    "Driver": f"{driver_name}{highlight}",
                    "Team": team_name,
                    "Points": f"{pts} PTS",
                })
            st.table(wdc_table)

        with tab_wcc:
            st.markdown("### World Constructors' Championship Final Standings")
            wcc_table = []
            for rank, (team_name, pts) in enumerate(
                res["constructor_standings"], 1
            ):
                is_user_team = team_name == res["team_name"]
                highlight = " ⭐ (Yours)" if is_user_team else ""
                wcc_table.append({
                    "Pos": f"P{rank}",
                    "Constructor": f"{team_name}{highlight}",
                    "Points": f"{pts} PTS",
                })
            st.table(wcc_table)

        with tab_rounds:
            st.markdown("### Grand Prix Race Results Breakdown")
            selected_round_gp = st.selectbox(
                "Select Grand Prix to View Full Classification:",
                res["races"],
                key="round_select_box",
            )

            if selected_round_gp and "race_results" in res:
                round_idx = res["races"].index(selected_round_gp)
                gp_results = res["race_results"][round_idx]

                st.markdown(
                    f"#### 🏆 Official Classification: Round {round_idx+1} —"
                    f" Grand Prix of {selected_round_gp}"
                )

                round_table = []
                for pos, item in enumerate(gp_results, 1):
                    d_name, t_name, pts_awarded = item
                    is_user_driver = d_name in user_drivers
                    highlight = " ⭐ (Yours)" if is_user_driver else ""
                    round_table.append({
                        "Pos": f"P{pos}",
                        "Driver": f"{d_name}{highlight}",
                        "Team": t_name,
                        "Points Earned": f"+{pts_awarded} PTS",
                    })
                st.table(round_table)

        # SAVE TO ACCOUNT & LEADERBOARD OPT-IN
        if st.session_state.user:
            st.markdown("### 💾 Save Season Record")
            is_public_opt_in = st.checkbox(
                "🌐 Submit this score to the Global Leaderboard", value=False
            )

            if st.button(
                "💾 Confirm & Save Season to 'Your 24-0'",
                type="primary",
                use_container_width=True,
            ):
                save_user_score(
                    user_id=st.session_state.user["id"],
                    team_name=res["team_name"],
                    driver1=res["d1_name"],
                    driver2=res["d2_name"],
                    car=res["car_name"],
                    principal=(
                        st.session_state.draft["p"].name
                        if st.session_state.draft["p"]
                        else "N/A"
                    ),
                    points=res["total_points"],
                    rank=res["c_pos"],
                    wins=res["wins"],
                    podiums=st.session_state.get("podiums_count", 0),
                    wdc_won=1 if won_wdc else 0,
                    wcc_won=1 if won_wcc else 0,
                    is_public=is_public_opt_in,
                )
                st.success("✅ Season record saved to career stats database!")

        if st.button("🔄 Reset & Start New Draft", use_container_width=True):
            st.session_state.draft = {"d1": None, "d2": None, "car": None, "p": None}
            st.session_state.available = drivers.copy()
            st.session_state.result = None
            st.session_state.rolled_year_d1 = None
            st.session_state.rolled_year_d2 = None
            st.session_state.rolled_year_car = None
            st.session_state.rolled_year_p = None
            st.session_state.rerolls_left = 1
            st.rerun()
