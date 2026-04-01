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

# Explicit placeholders to replace
TARGET_IP_PLACEHOLDERS  = ["<TARGET_IP>", "<SERVER_IP>", "<RHOST>", "<IP>", "<windows_ip>"]
ATTACKER_IP_PLACEHOLDERS = ["<OUR_IP>", "<LHOST>", "<ATTACKER_IP>", "<linux_ip>"]
DOMAIN_PLACEHOLDERS = [
    "<TARGET_DOMAIN>", "<DOMAIN>",
    "INLANEFREIGHT.LOCAL", "inlanefreight.local",
    "INLANEFREIGHT.COM",  "inlanefreight.com",
    "INLANEFREIGHT.HTB",  "inlanefreight.htb",
]

# Regex patterns for hardcoded HTB IPs found throughout the notes
_TARGET_IP_RE  = re.compile(r'\b(10\.129\.\d{1,3}\.\d{1,3}|10\.10\.10\.\d{1,3}|172\.16\.\d{1,3}\.\d{1,3})\b')
_ATTACKER_IP_RE = re.compile(r'\b10\.10\.1[45]\.\d{1,3}\b')

PAGE_SIZE = 30

# File Transfer filter — "-- off --" means show category view; any other = curated
TRANSFER_FILTERS: Dict[str, object] = {}  # retained for noise-keyword filtering only

# Headings to exclude from scraped "All" view (verification, encryption, meta)
_TRANSFER_NOISE_KEYWORDS = {
    "md5", "hash", "confirm", "check file", "encrypt", "decrypt",
    "introduction", "recap", "practice", "onwards", "section recap",
    "extra practice", "error", "pwnbox - check", "pwnbox check",
    "linux - confirm", "confirming", "verif",
}

# Windows victim-machine admin indicators only.
# We assume sudo on the attack box, so shell/bash blocks are never flagged.
_WIN_ADMIN_RE = re.compile(
    r'-Verb\s+RunAs'                                        # PS RunAs
    r'|Start-Process.{0,60}-Verb'                           # PS Start-Process elevated
    r'|net\s+(localgroup\s+administrators|user\s+\S+\s+/add)'  # group/user modification
    r'|sc\s+(config|create|start|stop)\s'                   # service control
    r'|reg\s+(add|save|delete)\s+HKL[ME]'                   # HKLM/HKME registry
    r'|schtasks.{0,80}/rl\s+highest'                        # scheduled task elevated
    r'|runas\s+/user:administrator'                         # explicit runas
    r'|Invoke-Mimikatz'                                     # mimikatz via PS
    r'|sekurlsa::|lsadump::|token::elevate'                 # mimikatz modules
    r'|Set-MpPreference'                                    # AV bypass (needs admin)
    r'|New-LocalUser|Add-LocalGroupMember'                  # local account management
    r'|Enable-PSRemoting'                                   # WinRM enable
    , re.IGNORECASE | re.MULTILINE,
)

# Only Windows-context langs are checked — shell/bash = attack box, no flag
_WIN_LANGS = {"powershell", "powershell-session", "cmd", "cmd-session"}

def needs_admin(code: str, lang: str) -> bool:
    if lang not in _WIN_LANGS:
        return False
    return bool(_WIN_ADMIN_RE.search(code))

# ── Curated file transfer command sets ────────────────────────────────────────
# Each method has a title, description, and a list of steps.
# Each step has: label, lang (for badge), display_lang (for st.code), code.
# Placeholders: <windows_ip> → target_ip,  <linux_ip> → attacker_ip

CURATED_TRANSFERS: Dict[str, List[Dict]] = {
    "🪟 Windows → Linux": [
        {
            "method": "Method 1 · SCP",
            "desc": "Standard secure copy. Requires SSH running on the Linux destination.",
            "steps": [
                {
                    "label": "🪟 Run from Windows",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "scp C:\\path\\to\\file.ext username@<linux_ip>:/path/to/destination/",
                },
            ],
        },
        {
            "method": "Method 2 · Python HTTP Server",
            "desc": "Fastest method when SSH creds aren't available. Python must be on the Windows machine.",
            "steps": [
                {
                    "label": "🪟 On Windows — host the file",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "cd C:\\path\\to\\folder\npython -m http.server 8000",
                },
                {
                    "label": "🐧 On Linux — download the file",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "wget http://<windows_ip>:8000/file.ext\n# or\ncurl -O http://<windows_ip>:8000/file.ext",
                },
            ],
        },
        {
            "method": "Method 3 · Netcat",
            "desc": "Raw socket transfer. No auth or encryption — requires nc on both machines.",
            "steps": [
                {
                    "label": "🐧 On Linux — listen to receive the file",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "nc -lnvp 4444 > file.ext",
                },
                {
                    "label": "🪟 On Windows — push the file",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "nc.exe <linux_ip> 4444 < C:\\path\\to\\file.ext",
                },
            ],
        },
        {
            "method": "Method 4 · SMB Share",
            "desc": "Pull from an existing Windows share using smbclient on Linux.",
            "steps": [
                {
                    "label": "🐧 Run from Linux",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": (
                        "smbclient //<windows_ip>/ShareName -U WindowsUsername\n"
                        "# At the smb:\\> prompt:\n"
                        "get file.ext"
                    ),
                },
            ],
        },
    ],
    "🐧 Linux → Windows": [
        {
            "method": "Method 1 · Impacket SMB Server  ★ CPTS Favourite",
            "desc": "Gold standard for AD labs. Windows uses built-in commands — nothing dropped on disk.",
            "steps": [
                {
                    "label": "🐧 On Linux — start the share",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "sudo impacket-smbserver shareName /path/to/linux/folder -smb2support",
                },
                {
                    "label": "🪟 On Windows — copy the file",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "copy \\\\<linux_ip>\\shareName\\file.ext C:\\path\\to\\destination\\file.ext",
                },
            ],
        },
        {
            "method": "Method 2 · Python HTTP Server + PowerShell / Certutil",
            "desc": "Use when SMB (port 445) is firewalled. HTTP (80/8000) is usually allowed.",
            "steps": [
                {
                    "label": "🐧 On Linux — host the file",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "cd /path/to/linux/folder\npython3 -m http.server 8000",
                },
                {
                    "label": "🪟 On Windows — download with PowerShell",
                    "lang": "powershell",
                    "display_lang": "powershell",
                    "code": 'Invoke-WebRequest -Uri "http://<linux_ip>:8000/file.ext" -OutFile "C:\\path\\to\\file.ext"',
                },
                {
                    "label": "🪟 On Windows — download with Certutil (LOLBAS)",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "certutil.exe -urlcache -split -f http://<linux_ip>:8000/file.ext C:\\path\\to\\file.ext",
                },
            ],
        },
        {
            "method": "Method 3 · SCP",
            "desc": "Push directly from Linux if the Windows target has OpenSSH installed (Win10/11, Server 2019+).",
            "steps": [
                {
                    "label": "🐧 Run from Linux",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "scp /path/to/linux/file.ext windows_user@<windows_ip>:C:/path/to/destination/",
                },
            ],
        },
        {
            "method": "Method 4 · Netcat",
            "desc": "Raw socket transfer. Requires nc.exe present on the Windows target.",
            "steps": [
                {
                    "label": "🪟 On Windows — listen to receive the file",
                    "lang": "cmd",
                    "display_lang": "shell",
                    "code": "nc.exe -lnvp 4444 > file.ext",
                },
                {
                    "label": "🐧 On Linux — push the file",
                    "lang": "bash",
                    "display_lang": "bash",
                    "code": "nc <windows_ip> 4444 < /path/to/linux/file.ext",
                },
            ],
        },
    ],
}


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
def apply_substitutions(
    code: str, target_ip: str, attacker_ip: str, target_domain: str
) -> str:
    if target_ip:
        for ph in TARGET_IP_PLACEHOLDERS:
            code = code.replace(ph, target_ip)
        code = _TARGET_IP_RE.sub(target_ip, code)
    if attacker_ip:
        for ph in ATTACKER_IP_PLACEHOLDERS:
            code = code.replace(ph, attacker_ip)
        code = _ATTACKER_IP_RE.sub(attacker_ip, code)
    if target_domain:
        for ph in DOMAIN_PLACEHOLDERS:
            code = code.replace(ph, target_domain)
    return code


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Base & background ── */
    html, body, .stApp {
        background-color: #0d1117 !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    }

    /* Scanline overlay for terminal feel */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 65, 0.015) 2px,
            rgba(0, 255, 65, 0.015) 4px
        );
        pointer-events: none;
        z-index: 0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #1a3a2a !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Protect Streamlit's built-in UI icons from the font override */
    .material-symbols-rounded, .stIcon {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: #3fb950 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.05em;
        text-shadow: 0 0 10px #3fb95066;
    }

    /* ── Clean Sidebar Menu (hides native radio circles) ── */
    [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    [data-testid="stRadio"] label {
        padding: 8px 12px !important;
        border-radius: 4px;
        margin-bottom: 2px !important;
        background: transparent;
        transition: all 0.2s;
        cursor: pointer;
        position: relative;
    }
    [data-testid="stRadio"] label:hover {
        background: #1a3a2a44 !important;
    }
    [data-testid="stRadio"] label p {
        font-size: 0.85rem !important;
        color: #8b949e !important;
        margin: 0 !important;
    }
    [data-testid="stRadio"] label[aria-checked="true"] {
        background: #1a3a2a !important;
        border-left: 3px solid #3fb950 !important;
        border-radius: 0 4px 4px 0 !important;
    }
    [data-testid="stRadio"] label[aria-checked="true"] p {
        color: #3fb950 !important;
        font-weight: 600 !important;
    }

    /* Sidebar inputs */
    [data-testid="stSidebar"] input {
        background-color: #0d1117 !important;
        border: 1px solid #1a3a2a !important;
        color: #58a6ff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        border-radius: 4px !important;
    }
    [data-testid="stSidebar"] input:focus {
        border-color: #3fb950 !important;
        box-shadow: 0 0 0 1px #3fb95044 !important;
    }
    [data-testid="stSidebar"] input::placeholder {
        color: #3d4450 !important;
    }
    [data-testid="stSidebar"] label {
        color: #8b949e !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Selectbox */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #0d1117 !important;
        border: 1px solid #1a3a2a !important;
        color: #58a6ff !important;
        font-size: 0.8rem !important;
    }

    /* ── Main area ── */
    .main .block-container {
        padding-top: 1.5rem !important;
        max-width: 1400px;
    }

    /* Page header */
    h1, h2 {
        font-family: 'JetBrains Mono', monospace !important;
        color: #e6edf3 !important;
    }

    /* ── Command cards ── */
    .ttp-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-left: 3px solid #3fb950;
        border-radius: 6px;
        padding: 12px 16px 4px 16px;
        margin-bottom: 14px;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .ttp-card:hover {
        border-left-color: #58a6ff;
        box-shadow: 0 0 12px #3fb95022;
    }

    .ttp-breadcrumb {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #3d4450;
        margin-bottom: 4px;
        letter-spacing: 0.03em;
    }

    .ttp-heading {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        font-weight: 600;
        color: #58a6ff;
        margin-bottom: 6px;
    }
    .ttp-heading::before {
        content: '❯ ';
        color: #3fb950;
        font-weight: 400;
    }

    .ttp-badge {
        display: inline-block;
        background: #0d1117;
        color: #3fb950;
        border: 1px solid #1a3a2a;
        border-radius: 3px;
        padding: 0px 6px;
        font-size: 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 8px;
        vertical-align: middle;
        letter-spacing: 0.05em;
    }

    /* ── Code blocks ── */
    [data-testid="stCode"] {
        border: 1px solid #1a3a2a !important;
        border-radius: 4px !important;
        background: #010409 !important;
    }
    [data-testid="stCode"] code {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 0.78rem !important;
        color: #e6edf3 !important;
    }

    /* ── Metric (command count) ── */
    [data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #1a3a2a;
        border-radius: 6px;
        padding: 8px 12px !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #3fb950 !important;
        font-size: 1.6rem !important;
        text-shadow: 0 0 8px #3fb95066;
    }

    /* ── Pagination buttons ── */
    [data-testid="baseButton-secondary"] {
        background-color: #161b22 !important;
        border: 1px solid #1a3a2a !important;
        color: #3fb950 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        border-radius: 4px !important;
    }
    [data-testid="baseButton-secondary"]:hover {
        background-color: #1a3a2a !important;
        border-color: #3fb950 !important;
    }
    [data-testid="baseButton-secondary"]:disabled {
        opacity: 0.25 !important;
    }

    /* ── Info / empty state ── */
    [data-testid="stAlert"] {
        background-color: #161b22 !important;
        border: 1px solid #1a3a2a !important;
        border-radius: 6px !important;
        color: #8b949e !important;
        font-size: 0.82rem !important;
    }

    .ttp-admin-badge {
        display: inline-block;
        background: transparent;
        color: #d29922;
        border: 1px solid #d2992244;
        border-radius: 3px;
        padding: 0px 5px;
        font-size: 0.62rem;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 6px;
        vertical-align: middle;
        letter-spacing: 0.06em;
    }
    .ttp-method-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        font-weight: 600;
        color: #3fb950;
        margin: 18px 0 2px 0;
        letter-spacing: 0.03em;
    }
    .ttp-method-title::before { content: '// '; color: #3d4450; }
    .ttp-method-desc {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #8b949e;
        margin-bottom: 10px;
    }
    .ttp-step-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.73rem;
        color: #58a6ff;
        margin-bottom: 3px;
        margin-top: 8px;
    }
    .ttp-step-label::before { content: '❯ '; color: #3fb950; }

    /* Inactive nav — plain text non-buttons */
    .nav-inactive-btn button {
        background: transparent !important;
        border: none !important;
        color: #3d4450 !important;
        padding: 3px 4px !important;
        font-size: 0.82rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-align: left !important;
        box-shadow: none !important;
        width: 100%;
    }
    .nav-inactive-btn button:hover {
        color: #8b949e !important;
        background: transparent !important;
    }
    /* Switch-mode back link */
    .nav-switch button {
        background: transparent !important;
        border: none !important;
        color: #3fb95055 !important;
        font-size: 0.68rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        padding: 0 2px !important;
        letter-spacing: 0.06em;
        box-shadow: none !important;
    }
    .nav-switch button:hover {
        color: #3fb950 !important;
        background: transparent !important;
    }

    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #1a3a2a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3fb950; }

    /* Inject "// FILE TRANSFERS" cleanly above the 6th nav item */
    [data-testid="stRadio"] > div > label:nth-child(6) {
        margin-top: 35px !important;
    }
    [data-testid="stRadio"] > div > label:nth-child(6)::before {
        content: "// FILE TRANSFERS";
        position: absolute;
        top: -24px;
        left: 0;
        color: #3fb950;
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        font-weight: 600;
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session state ─────────────────────────────────────────────────────────────
_CAT_KEYS  = list(CATEGORY_MODULES.keys())
_TF_KEYS   = list(CURATED_TRANSFERS.keys())
_NAV_OPTIONS = _CAT_KEYS + _TF_KEYS

if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = _CAT_KEYS[0]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<h1 style="font-size:1.1rem;letter-spacing:0.05em;color:#3fb950;">'
        'TTP DASHBOARD</h1>'
        '<p style="font-size:0.68rem;color:#3d4450;margin-top:-10px;letter-spacing:0.08em;">'
        'CPTS // COMMAND BROWSER</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Navigation (categories + file transfers in one radio) ─────────────────
    st.markdown(
        '<p style="font-size:0.7rem;color:#3fb950;letter-spacing:0.1em;margin-bottom:6px;">'
        '// NAVIGATE</p>',
        unsafe_allow_html=True,
    )

    def _on_nav_change():
        val = st.session_state.get("_nav_radio")
        if val:
            st.session_state["nav_selection"] = val

    nav_selection = st.radio(
        "Navigate",
        options=_NAV_OPTIONS,
        index=_NAV_OPTIONS.index(st.session_state["nav_selection"]),
        key="_nav_radio",
        on_change=_on_nav_change,
        label_visibility="collapsed",
    )
    st.session_state["nav_selection"] = nav_selection

    st.divider()

    # ── Target settings ───────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:0.7rem;color:#3fb950;letter-spacing:0.1em;margin-bottom:8px;">'
        '// TARGET SETTINGS</p>',
        unsafe_allow_html=True,
    )
    target_ip = st.text_input(
        "Target IP",
        placeholder="10.129.x.x / 172.16.x.x",
        help="Replaces <TARGET_IP>, <RHOST>, <windows_ip>, and hardcoded HTB target IPs",
    )
    attacker_ip = st.text_input(
        "Attacker IP",
        placeholder="10.10.14.x",
        help="Replaces <OUR_IP>, <LHOST>, <linux_ip>, and hardcoded HTB attacker IPs",
    )
    target_domain = st.text_input(
        "Target Domain",
        placeholder="domain.local",
        help="Replaces <TARGET_DOMAIN> and INLANEFREIGHT.LOCAL/COM/HTB",
    )

    st.divider()

    # ── Search ────────────────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:0.7rem;color:#3fb950;letter-spacing:0.1em;margin-bottom:8px;">'
        '// SEARCH</p>',
        unsafe_allow_html=True,
    )
    search_query = st.text_input(
        "Search",
        placeholder="nmap, hashcat, sqlmap…",
        label_visibility="collapsed",
    )


# ── Main content ──────────────────────────────────────────────────────────────
nav_selection     = st.session_state.get("nav_selection", _CAT_KEYS[0])
is_transfer_view  = nav_selection in _TF_KEYS
selected_category = nav_selection if not is_transfer_view else _CAT_KEYS[0]
transfer_filter   = nav_selection if is_transfer_view else _TF_KEYS[0]

all_commands = load_all_commands()
commands = all_commands[selected_category]

# For scraped category view — strip noise headings in Post-Exploitation
if not is_transfer_view and selected_category == "🏴 Post-Exploitation":
    commands = [
        c for c in commands
        if not any(kw in c["heading"].lower() for kw in _TRANSFER_NOISE_KEYWORDS)
    ]

# Apply text search filter (only for scraped view)
if not is_transfer_view and search_query:
    q = search_query.lower()
    commands = [
        c for c in commands
        if q in c["code"].lower()
        or q in c["heading"].lower()
        or q in c["file"].lower()
        or q in c["module"].lower()
    ]

# ── Header bar ────────────────────────────────────────────────────────────────
col_title, col_count = st.columns([5, 1])
with col_title:
    title = transfer_filter if is_transfer_view else selected_category
    st.markdown(
        f'<h2 style="font-family:\'JetBrains Mono\',monospace;color:#e6edf3;">'
        f'{title}</h2>',
        unsafe_allow_html=True,
    )
with col_count:
    if is_transfer_view:
        st.metric("METHODS", len(CURATED_TRANSFERS.get(transfer_filter, [])))
    else:
        st.metric("COMMANDS", len(commands))

# ── Curated file transfer view ────────────────────────────────────────────────
if is_transfer_view:
    methods = CURATED_TRANSFERS.get(transfer_filter, [])
    if not methods:
        st.info("No curated commands for this direction.")
        st.stop()

    for method in methods:
        st.markdown(
            f'<div class="ttp-method-title">{method["method"]}</div>'
            f'<div class="ttp-method-desc">{method["desc"]}</div>',
            unsafe_allow_html=True,
        )
        for step in method["steps"]:
            code = apply_substitutions(step["code"], target_ip, attacker_ip, target_domain)
            admin_badge = (
                '<span class="ttp-admin-badge">&#9881; ELEVATED</span>'
                if needs_admin(code, step["lang"]) else ""
            )
            st.markdown(
                f'<div class="ttp-step-label">{step["label"]}'
                f'  <span class="ttp-badge">{step["lang"]}</span>'
                f'{admin_badge}</div>',
                unsafe_allow_html=True,
            )
            st.code(code, language=step["display_lang"])
        st.markdown('<hr class="ttp-divider">', unsafe_allow_html=True)
    st.stop()

# ── Scraped notes view ────────────────────────────────────────────────────────
if not commands:
    st.info("No commands match — try a different search or filter.")
    st.stop()

# Pagination setup
total_pages = max(1, (len(commands) - 1) // PAGE_SIZE + 1)

if "page" not in st.session_state:
    st.session_state.page = 0

page_key = f"{selected_category}|{search_query}|{transfer_filter}"
if st.session_state.get("_last_page_key") != page_key:
    st.session_state.page = 0
    st.session_state["_last_page_key"] = page_key

page = st.session_state.page
page_commands = commands[page * PAGE_SIZE: (page + 1) * PAGE_SIZE]

# Render cards
for cmd in page_commands:
    code = apply_substitutions(cmd["code"], target_ip, attacker_ip, target_domain)
    admin_badge = (
        '<span class="ttp-admin-badge">&#9881; ELEVATED</span>'
        if needs_admin(code, cmd["lang"]) else ""
    )
    st.markdown(
        f'<div class="ttp-card">'
        f'<div class="ttp-breadcrumb">{cmd["module"]} › {cmd["file"]}</div>'
        f'<div class="ttp-heading">{cmd["heading"]}'
        f'<span class="ttp-badge">{cmd["lang"]}</span>'
        f'{admin_badge}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.code(code, language=cmd["display_lang"])

# Pagination controls
if total_pages > 1:
    st.markdown("<br>", unsafe_allow_html=True)
    p_col1, p_col2, p_col3 = st.columns([1, 3, 1])
    with p_col1:
        if st.button("◀ PREV", disabled=(page == 0), use_container_width=True):
            st.session_state.page -= 1
            st.rerun()
    with p_col2:
        st.markdown(
            f'<p style="text-align:center;font-size:0.72rem;color:#3d4450;'
            f'font-family:monospace;padding-top:8px;">'
            f'PAGE {page + 1} / {total_pages} &nbsp;·&nbsp; {len(commands)} results</p>',
            unsafe_allow_html=True,
        )
    with p_col3:
        if st.button("NEXT ▶", disabled=(page >= total_pages - 1), use_container_width=True):
            st.session_state.page += 1
            st.rerun()
