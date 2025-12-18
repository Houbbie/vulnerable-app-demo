#!/usr/bin/env python3
import os
import subprocess
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ApexHunter")

REPORT_NAME = "SECURITY_AUDIT_REPORT.md"
# VERVANG DIT door jouw GitHub URL
GITHUB_REPO = "https://github.com/houbbie/vulnerable-app-demo"

class ApexHunter:
    def run_remote_scan(self, repo_url):
        logger.info(f"🚀 Verbinding maken met GitHub: {repo_url}")
        
        # We scannen de REMOTE repository direct via de 'git' module van TruffleHog
        # --no-verification is nodig omdat onze demo-keys niet 'echt' bestaan bij AWS
        cmd = ["trufflehog", "git", repo_url, "--json", "--no-verification"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            findings = []
            
            if result.stdout:
                for line in result.stdout.splitlines():
                    if line.strip():
                        findings.append(json.loads(line))
            
            if not findings and result.stderr:
                logger.warning(f"Scan melding: {result.stderr}")
                
            return findings
        except Exception as e:
            logger.error(f"Fout tijdens remote scan: {e}")
            return []

    def export_to_markdown(self, repo_url, findings):
        with open(REPORT_NAME, "w", encoding="utf-8") as md:
            md.write(f"# 🛡️ Apex Hunter: Remote Audit Rapport\n\n")
            md.write(f"| Kenmerk | Details |\n| :--- | :--- |\n")
            md.write(f"| **Target URL** | {repo_url} |\n")
            md.write(f"| **Datum** | {datetime.now().strftime('%d-%m-%Y %H:%M')} |\n")
            md.write(f"| **Status** | {'🔴 KRITIEK GEVAAR' if findings else '🟢 VEILIG'} |\n\n")
            
            md.write("## 🔍 Gevonden Geheimen in Historie\n")
            md.write("| Service | Ernst | Branch | Bestand |\n| :--- | :--- | :--- | :--- |\n")
            
            seen = set()
            for f in findings:
                det = f.get('detector_name', 'Unknown')
                meta = f.get('SourceMetadata', {}).get('Data', {}).get('Git', {})
                branch = meta.get('branch', 'N/A')
                path = meta.get('file', 'Git History')
                
                key = f"{det}:{branch}:{path}"
                if key not in seen:
                    md.write(f"| {det} | CRITICAL | {branch} | `{path}` |\n")
                    seen.add(key)
        
        logger.info(f"✅ Rapport gegenereerd: {REPORT_NAME}")

if __name__ == "__main__":
    hunter = ApexHunter()
    results = hunter.run_remote_scan(GITHUB_REPO)
    hunter.export_to_markdown(GITHUB_REPO, results)
    print(f"Audit voltooid. Bevindingen: {len(results)}")