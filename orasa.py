#!/usr/bin/env python3
import argparse
from modules.recon import Recon
from modules.scanner import PortScanner
from modules.report import Report
from colorama import Fore, Style

banner = f"""
{Fore.CYAN}
                                                 
                                                 
  /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$$  /$$$$$$ 
 /$$__  $$ /$$__  $$|____  $$ /$$_____/ |____  $$
| $$  \ $$| $$  \__/ /$$$$$$$|  $$$$$$   /$$$$$$$
| $$  | $$| $$      /$$__  $$ \____  $$ /$$__  $$
|  $$$$$$/| $$     |  $$$$$$$ /$$$$$$$/|  $$$$$$$
 \______/ |__/      \_______/|_______/  \_______/
                                                 
                                                 
                                                 
{Style.RESET_ALL}

{Fore.MAGENTA}      Offensive Recon & Attack Surface Analyzer{Style.RESET_ALL}
{Fore.YELLOW}      Developed by: Abdelilah Elkhaoudari{Style.RESET_ALL}
{Fore.GREEN}      Phone: +212613301426{Style.RESET_ALL}
{Fore.BLUE}      Email: elkhaoudariabdelilah@gmail.com{Style.RESET_ALL}
"""

print(banner)



def main():
    parser = argparse.ArgumentParser(
        prog='orasa',
        description='Offensive Security Recon & Attack Surface Analyzer'
    )

    parser.add_argument('-d', '--domain', required=True, help='Target domain (example.com)')
    parser.add_argument('--full-scan', action='store_true', help='Run recon + port scan + reporting')
    parser.add_argument('-p', '--ports', default='1-1024', help='Port range (1-1024 or 22,80,443)')
    parser.add_argument('-o', '--output', default='results.json', help='JSON output file')

    args = parser.parse_args()

    # Reconnaissance
    recon = Recon(args.domain)
    print(f"[+] Starting recon on {args.domain}")
    recon.run_basic()

    # Port scanning
    if args.full_scan:
        print("[+] Starting port scan...")
        scanner = PortScanner(args.domain, args.ports)
        scanner.run()
        recon.merge_ports(scanner.results)

    # Reporting
    report = Report(recon.get_results())
    report.to_json(args.output)
    report.to_html('report.html')

    print(f"\n[✓] Scan completed!")
    print(f"[✓] JSON report saved to: {args.output}")
    print(f"[✓] HTML report saved to: report.html")

if __name__ == '__main__':
    main()
