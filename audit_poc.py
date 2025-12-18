#!/Users/edwinhouben/Development/Github/.venv/bin/python
import os
import shutil
import subprocess
import json
import logging
from datetime import datetime
from collections import Counter

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ApexHunter")

TEMP_DIR = "audit_workspace"
REPORT_NAME = "SECURITY_AUDIT_REPORT.md"
# Zorg dat je de push unblocked hebt op GitHub zoals besproken
DEMO_TARGETS = ["https://github.com/houbbie/vulnerable-app-demo"]

class ApexHunter:
    def __init__(self):
        self._setup_env()

    def _setup_env(self):
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR, exist_ok=True)
        logger.info("Apex Hunter Engine Ready.")

    def get_severity(self, detector):
        high = ['aws', 'azure', 'gcp', 'ssh', 'postgresql', 'privatekey', 'database']
        medium = ['stripe', 'slack', 'github', 'twilio', 'api-key']
        name = detector.lower()
        if any(k in name for k in high): return "CRITICAL"
        if any(k in name for k in medium): return "HIGH"
        return "MEDIUM"
    
    def verify_dummy_keys(self, detector_name, secret_value):
        """Simuleert actieve verificatie voor de demo-doeleinden."""
        demo_keys = ['AKIAV7B', 'sk_test_', 'xoxb-']
        if any(k in secret_value for k in demo_keys):
            return "✅ SUCCESS (ACTIVE)"
        return "❓ UNVERIFIED"

    def run_deep_scan(self, repo_url):
        logger.info(f"Initiating Deep Scan: {repo_url}")
        try:
            cmd = ["trufflehog", "git", repo_url, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            findings = [json.loads(l) for l in result.stdout.splitlines() if l.strip()]
            return findings
        except Exception as e:
            logger.error(f"Scan gefaald: {e}")
            return []

    def export_to_markdown(self, repo_url, findings):
        stats = Counter([self.get_severity(f.get('detector_name', '')) for f in findings])
        
        with open(REPORT_NAME, "w", encoding="utf-8") as md:
            md.write(f"# 🛡️ Apex Hunter: Security Audit & Response Rapport\n\n")
            md.write(f"| Kenmerk | Details |\n| :--- | :--- |\n")
            md.write(f"| **Repository** | {repo_url} |\n")
            md.write(f"| **Audit Datum** | {datetime.now().strftime('%d-%m-%Y %H:%M')} |\n")
            md.write(f"| **Status** | {'🔴 KRITIEK GEVAAR' if stats['CRITICAL'] > 0 else '🟢 VEILIG'} |\n\n")

            md.write(f"## 📊 Risico Scoreboard\n")
            for level in ['CRITICAL', 'HIGH', 'MEDIUM']:
                count = stats.get(level, 0)
                emoji = "🔴" if level == "CRITICAL" else "🟠" if level == "HIGH" else "🟡"
                md.write(f"- **{level}**: {emoji} {count} bevinding(en)\n")
            md.write("\n")

            md.write(f"## 🔍 Gedetailleerde Bevindingen\n")
            # Kolom 'Validatie' toegevoegd voor de demo klap op de vuurpijl
            md.write(f"| Service | Ernst | Validatie | Branch | Bestandspad |\n| :--- | :--- | :--- | :--- | :--- |\n")
            
            seen = set()
            for f in findings:
                meta = f.get('SourceMetadata', {}).get('Data', {}).get('Git', {})
                det = f.get('detector_name', 'Unknown')
                raw = f.get('Raw', '')
                br = meta.get('branch', 'N/A')
                path = meta.get('file', 'Git History')
                key = f"{det}:{br}:{path}"
                
                if key not in seen:
                    sev = self.get_severity(det)
                    # Hier roepen we je verificatie-simulatie aan
                    v_status = self.verify_dummy_keys(det, raw)
                    md.write(f"| {det} | {sev} | {v_status} | {br} | `{path}` |\n")
                    seen.add(key)
                if len(seen) >= 20: break

            md.write(f"\n## 🛠️ Incident Response Playbook\n")
            md.write(f"### Fase 1: Containment (Direct)\n")
            md.write(f"- [ ] **Revoke:** Trek de sleutel in bij de provider.\n")
            md.write(f"- [ ] **Notify:** Informeer het Security Team.\n")

        logger.info(f"Rapport gegenereerd: {REPORT_NAME}")

if __name__ == "__main__":
    hunter = ApexHunter()
    for repo in DEMO_TARGETS:
        results = hunter.run_deep_scan(repo)
        hunter.export_to_markdown(repo, results)
        print(f"\n✅ Audit voltooid. Check {REPORT_NAME} voor de resultaten.")