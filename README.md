<div align="center">

# 🛡️ PriVi-Shell: Developed by: PriViSecurity**

![PriVi-Shell Dashboard](PriViShell.PNG)

</div>

Advanced Multi-Platform Reverse Shell Generator with AMSI Bypass.

# ⚡ PriViShell v1.0 [STEALTH]
### Multi-Platform Reverse Shell Generator with AMSI Bypass
**Developed by [Prince Ubebe](https://github.com/YOUR_GITHUB_USERNAME) | PriViSecurity**



**PriViShell** is a tactical Python-based framework designed for Pentesters and CTF players. It generates high-stability reverse shell payloads for multiple operating systems, including an **Elite Stealth Mode** for bypassing modern Windows security controls.

## 🚀 Key Features
- **Fileless Execution:** Payloads are designed to run in memory, minimizing disk footprint.
- **AMSI Bypass (Stealth Mode):** Utilizes `amsiInitFailed` reflection to temporarily blind Windows Defender during shell execution.
- **Cross-Platform Support:** - **Linux:** Base64-encoded Bash TCP shells.
  - **Python:** Stable PTY spawn shells for interactive sessions.
  - **Windows:** UTF-16LE Encoded PowerShell shells.
- **Input Validation:** Robust error checking for IP/Hostname and Port ranges to prevent broken payloads.
- **Flexible Output:** Copy directly from the terminal or export to `.ps1`, `.sh`, or `.py` files.

## 🛠️ Installation
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/PriViShell.git](https://github.com/YOUR_USERNAME/PriViShell.git)
   cd PriViShell
