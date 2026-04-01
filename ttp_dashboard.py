"""
TTP Dashboard — Streamlit app for browsing CPTS study notes.

Run with:
    streamlit run ttp_dashboard.py
"""

import re
from pathlib import Path
from typing import Dict, List

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TTP Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent

CATEGORY_MODULES: Dict[str, List[str]] = {
    "🔍 Recon": [
        "Footprinting",
        "Information Gathering - Web Edition",
        "Network Enumeration with NMAP",
        "Getting Started",
        "Penetration Testing Process",
        "Vulnerability Assessment",
        "AEN",
        "Using Web Proxies",
    ],
    "🚪 Initial Access": [
        "Attacking Common Services",
        "Login Brute Forcing",
        "Password Attacks",
    ],
    "💥 Exploitation": [
        "Using the Metasploit Framework",
        "Shells and Payloads",
        "SQL Injection",
        "SQLMap",
        "File Upload Attacks",
        "File Inclusion",
        "Attacking Web Applications with Ffuf",
        "Web Attacks",
        "XSS",
        "Command Injections",
        "Attacking Common Applications",
    ],
    "🏴 Post-Exploitation": [
        "File Transfers",
        "Linux Priv Esc",
        "Windows Priv Esc",
        "Documentation and Reporting",
    ],
    "↔️ Lateral Movement": [
        "Active Directory Enumeration & Attacks",
        "Pivoting, Tunneling, and Port Forwarding",
    ],
}

# Only parse code blocks tagged with command-relevant languages
COMMAND_LANGS = {
    "shell-session", "shell", "bash",
    "powershell-session", "powershell",
    "cmd-session", "cmd",
    "sql", "python", "",
}

# Map fenced-block language tags → Prism/Streamlit language IDs
LANG_DISPLAY: Dict[str, str] = {
    "shell-session": "bash",
    "powershell-session": "powershell",
    "cmd-session": "shell",
    "cmd": "shell",
    "": "bash",
}

# Explicit placeholders to replace (in priority order)
IP_PLACEHOLDERS = [
    "<TARGET_IP>", "<SERVER_IP>", "<OUR_IP>",
    "<RHOST>", "<LHOST>", "<IP>",
]
DOMAIN_PLACEHOLDERS = [
    "<TARGET_DOMAIN>", "<DOMAIN>",
    "INLANEFREIGHT.LOCAL", "inlanefreight.local",
    "INLANEFREIGHT.COM",  "inlanefreight.com",
    "INLANEFREIGHT.HTB",  "inlanefreight.htb",
]

PAGE_SIZE = 30


# ── Parsing (cached) ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner="📂 Loading notes…")
def load_all_commands() -> Dict[str, List[Dict]]:
    result: Dict[str, List[Dict]] = {cat: [] for cat in CATEGORY_MODULES}

    for category, modules in CATEGORY_MODULES.items():
        for module in modules:
            module_path = REPO_ROOT / module
            if not module_path.exists():
                continue
            for md_file in sorted(module_path.rglob("*.md")):
                _extract_blocks(md_file, module, category, result)

    return result


def _extract_blocks(
    md_file: Path,
    module: str,
    category: str,
    result: Dict[str, List[Dict]],
) -> None:
    try:
        text = md_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    lines = text.splitlines()
    current_heading = md_file.stem

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track nearest heading for context
        if re.match(r"^#{1,4}\s", line):
            current_heading = line.lstrip("#").strip()
            i += 1
            continue

        fence = re.match(r"^```(\S*)", line)
        if fence:
            lang = fence.group(1).lower()
            i += 1
            code_lines: List[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1

            code = "\n".join(code_lines).strip()

            if code and len(code) > 5 and lang in COMMAND_LANGS:
                result[category].append(
                    {
                        "module": module,
                        "file": md_file.stem,
                        "path": str(md_file.relative_to(REPO_ROOT)),
                        "heading": current_heading,
                        "lang": lang,
                        "display_lang": LANG_DISPLAY.get(lang, lang),
                        "code": code,
                    }
                )
        i += 1


# ── Substitution ──────────────────────────────────────────────────────────────
def apply_substitutions(code: str, target_ip: str, target_domain: str) -> str:
    if target_ip:
        for ph in IP_PLACEHOLDERS:
            code = code.replace(ph, target_ip)
    if target_domain:
        for ph in DOMAIN_PLACEHOLDERS:
            code = code.replace(ph, target_domain)
    return code


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Sidebar nav radio looks like a menu */
    div[data-testid="stRadio"] label {
        font-size: 0.95rem;
        padding: 4px 0;
    }
    .ttp-breadcrumb {
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 2px;
    }
    .ttp-heading {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .ttp-badge {
        display: inline-block;
        background: #2d2d3a;
        color: #a6e3a1;
        border-radius: 4px;
        padding: 1px 7px;
        font-size: 0.7rem;
        font-family: monospace;
        margin-left: 6px;
        vertical-align: middle;
    }
    hr.ttp-divider {
        margin: 6px 0 14px 0;
        border-color: #2a2a3a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎯 TTP Dashboard")
    st.caption("CPTS Study Notes — Command Browser")
    st.markdown("---")

    selected_category = st.radio(
        "Category",
        options=list(CATEGORY_MODULES.keys()),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### 🎯 Target Settings")
    target_ip = st.text_input(
        "Target IP",
        placeholder="e.g. 10.10.10.10",
        help="Replaces: <TARGET_IP>, <SERVER_IP>, <RHOST>, …",
    )
    target_domain = st.text_input(
        "Target Domain",
        placeholder="e.g. domain.local",
        help="Replaces: <TARGET_DOMAIN>, INLANEFREIGHT.LOCAL, …",
    )

    st.markdown("---")
    st.markdown("#### 🔎 Search")
    search_query = st.text_input(
        "Filter commands",
        placeholder="nmap, hashcat, sqlmap…",
        label_visibility="collapsed",
    )


# ── Main content ──────────────────────────────────────────────────────────────
all_commands = load_all_commands()
commands = all_commands[selected_category]

# Filter
if search_query:
    q = search_query.lower()
    commands = [
        c for c in commands
        if q in c["code"].lower()
        or q in c["heading"].lower()
        or q in c["file"].lower()
        or q in c["module"].lower()
    ]

# Header
col_title, col_count = st.columns([5, 1])
with col_title:
    st.header(selected_category)
with col_count:
    st.metric("Commands", len(commands))

if not commands:
    st.info("No commands match your search. Try different keywords.")
    st.stop()

# Pagination
total_pages = max(1, (len(commands) - 1) // PAGE_SIZE + 1)

if "page" not in st.session_state:
    st.session_state.page = 0

# Reset page on category/search change
page_key = f"{selected_category}|{search_query}"
if st.session_state.get("_last_page_key") != page_key:
    st.session_state.page = 0
    st.session_state["_last_page_key"] = page_key

page = st.session_state.page
start = page * PAGE_SIZE
page_commands = commands[start: start + PAGE_SIZE]

# Render cards
for cmd in page_commands:
    code = apply_substitutions(cmd["code"], target_ip, target_domain)

    st.markdown(
        f'<div class="ttp-breadcrumb">📁 {cmd["module"]} › {cmd["file"]}</div>'
        f'<div class="ttp-heading">{cmd["heading"]}'
        f'  <span class="ttp-badge">{cmd["lang"]}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )
    st.code(code, language=cmd["display_lang"])
    st.markdown('<hr class="ttp-divider">', unsafe_allow_html=True)

# Pagination controls
if total_pages > 1:
    p_col1, p_col2, p_col3 = st.columns([1, 2, 1])
    with p_col1:
        if st.button("← Prev", disabled=(page == 0)):
            st.session_state.page -= 1
            st.rerun()
    with p_col2:
        st.caption(f"Page {page + 1} of {total_pages}  ({len(commands)} results)")
    with p_col3:
        if st.button("Next →", disabled=(page >= total_pages - 1)):
            st.session_state.page += 1
            st.rerun()
