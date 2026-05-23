import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os
import json
import urllib.request

app = FastAPI(title="PhishShield AI - AI-Powered Human Firewall Intelligence Platform")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ═══════════════════════════════════════════════════════════
# RICH ORGANIZATIONAL DATASET — 150 EMPLOYEES, 6 DEPARTMENTS
# ═══════════════════════════════════════════════════════════
DEPARTMENTS = ["Finance", "HR", "Engineering", "Sales", "Legal", "Marketing"]
DEPT_HEADS = {
    "Finance": "Margaret Chen", "HR": "David Okafor", "Engineering": "Sarah Nakamura",
    "Sales": "James Rodriguez", "Legal": "Priya Sharma", "Marketing": "Elena Volkov"
}
FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ivan", "Julia",
    "Kevin", "Laura", "Mike", "Nina", "Oscar", "Priya", "Quinn", "Rachel", "Sam", "Tara",
    "Uma", "Victor", "Wendy", "Xander", "Yara", "Zack", "Aiden", "Bella", "Carlos", "Dana",
    "Erik", "Fatima", "Gavin", "Hana", "Igor", "Jade", "Kai", "Leila", "Marco", "Nadia",
    "Owen", "Paige", "Ravi", "Sofia", "Tyler", "Ursula", "Vince", "Wren", "Yasmin", "Zara"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez",
    "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "White",
    "Harris", "Thompson", "Chen", "Park", "Patel", "Kim", "Singh", "Nguyen", "Lopez", "Gonzalez",
    "Muller", "Sato", "Johansson", "Fernandez", "Ali", "Ivanov", "Okafor", "Nakamura"
]

EMPLOYEES = []
for i in range(1, 151):
    dept = DEPARTMENTS[i % len(DEPARTMENTS)]
    fn = FIRST_NAMES[i % len(FIRST_NAMES)]
    ln = LAST_NAMES[i % len(LAST_NAMES)]
    name = f"{fn} {ln}"
    EMPLOYEES.append({
        "id": f"EMP{i:04d}",
        "name": name,
        "email": f"{fn.lower()}.{ln.lower()}@acmecorp.com",
        "department": dept,
        "role": random.choice(["Analyst", "Manager", "Associate", "Director", "Specialist", "Coordinator"]),
        "risk_score": float(random.randint(5, 40)),
        "awareness_score": float(random.randint(55, 98)),
        "trainings_completed": random.randint(0, 8),
        "compromised": False,
        "reported": 0,
        "clicked_count": 0,
        "xp": random.randint(100, 500),
        "badge": random.choice(["Trainee", "Trainee", "Trainee", "Defender", "Vigilant"]),
        "streak_days": random.randint(0, 14),
        "last_simulation": None
    })

# ═══════════════════════════════════════════════════════════
# AI INSIGHTS ENGINE
# ═══════════════════════════════════════════════════════════
AI_INSIGHTS = [
    "🔬 Finance department shows 34% higher susceptibility to urgency-based phishing vectors than org average.",
    "🧠 Behavioral analysis: Users fail most on spoofed internal domains with visual typosquatting (e.g., acrnecorp.com).",
    "📊 Predictive model: End-of-quarter simulations will achieve 41% click rate due to deadline stress patterns.",
    "⚠️ HR division is critically vulnerable to authority-based attacks impersonating C-suite executives.",
    "🔍 Engineering team click rates spike 67% on fake GitHub/GitLab credential reset emails.",
    "💡 Sales users are highly susceptible to fake invoice and payment portal credential harvesting.",
    "✅ Legal department shows strongest reporting behavior — 48% report rate, highest in organization.",
    "🎯 Prediction: Next campaign targeting Finance+Sales with Fear vector will achieve 38% compromise rate.",
    "📈 Risk trajectory: Urgency-based attacks effectiveness increasing 22% per quarter based on trend analysis.",
    "🚨 URGENT: 14 employees exceed critical risk threshold (>75). Immediate mandatory training recommended.",
    "🛡️ Positive trend: Organization-wide awareness score improved 12% since last campaign cycle.",
    "🔒 Zero-trust validation: 23% of employees still enter credentials on first-visit external domains."
]

# ═══════════════════════════════════════════════════════════
# AI CHATBOT KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════
CHATBOT_RESPONSES = {
    "phishing": "Phishing is a social engineering attack where attackers send fraudulent communications (usually emails) designed to trick recipients into revealing sensitive information like passwords, credit card numbers, or corporate credentials.\n\n**Key indicators:**\n• Urgent or threatening language\n• Suspicious sender domains (typosquatting)\n• Requests for credentials or financial info\n• Mismatched URLs (hover to check)\n• Generic greetings instead of your name\n\n**Defense:** Always verify sender identity independently. Never click links in unexpected emails. Report suspicious emails to your IT Security team.",

    "spear": "Spear phishing is a targeted form of phishing where attackers research specific individuals or organizations to craft highly personalized attacks.\n\n**How it differs from regular phishing:**\n• Uses your real name, role, and department\n• References real projects or colleagues\n• Mimics internal communication style\n• Often impersonates executives (BEC)\n\n**Why it's dangerous:** Success rates are 3-5x higher than mass phishing because the personalization bypasses our natural skepticism.\n\n**Defense:** Verify unusual requests through a separate channel (phone call, in-person). Be especially cautious of requests involving money transfers or credential sharing.",

    "bec": "Business Email Compromise (BEC) is a sophisticated scam targeting organizations that conduct wire transfers or have suppliers abroad.\n\n**Common BEC scenarios:**\n• CEO Fraud — Impersonating executives requesting urgent transfers\n• Invoice Fraud — Fake invoices from compromised vendor accounts\n• Attorney Impersonation — Legal pressure for confidential transfers\n• Data Theft — HR targeting for W-2/employee PII\n\n**Impact:** FBI reports BEC caused $2.7 billion in losses in 2023 alone.\n\n**Defense:** Implement dual-authorization for financial transactions. Verify any change in payment details via phone. Train employees to question urgency.",

    "password": "Strong password practices are your first line of defense:\n\n**Best practices:**\n• Use 16+ characters with mixed case, numbers, symbols\n• Never reuse passwords across services\n• Use a password manager (1Password, Bitwarden)\n• Enable MFA/2FA everywhere possible\n• Never share passwords via email or chat\n\n**Common attack methods:**\n• Credential stuffing (reused passwords from breaches)\n• Brute force attacks\n• Phishing for credentials\n• Keylogger malware\n\n**If compromised:** Change immediately, enable MFA, check for unauthorized access, report to IT Security.",

    "report": "If you suspect a phishing email:\n\n**Immediate steps:**\n1. DO NOT click any links or download attachments\n2. DO NOT reply to the email\n3. DO NOT forward it to colleagues\n4. Report it to your IT Security team\n5. Use the 'Report Phishing' button in your email client\n\n**What happens after reporting:**\n• Security team analyzes the email headers and payload\n• Malicious domains are blocklisted\n• Similar emails are quarantined org-wide\n• Threat intelligence is updated\n\n**You're rewarded:** In PhishShield AI, reporting earns XP and contributes to your Defender badge!",

    "social": "Social engineering exploits human psychology rather than technical vulnerabilities.\n\n**Common tactics:**\n• **Authority** — Impersonating executives or IT\n• **Urgency** — Creating artificial time pressure\n• **Fear** — Threatening account suspension or legal action\n• **Greed** — Promising rewards or financial gains\n• **Curiosity** — Enticing with interesting content\n• **Helpfulness** — Exploiting desire to assist\n\n**Defense framework (STOP):**\n• **S**top — Pause before acting\n• **T**hink — Is this expected? Does it make sense?\n• **O**bserve — Check sender, URLs, attachments\n• **P**rotect — Report and verify independently",

    "mfa": "Multi-Factor Authentication (MFA) adds layers beyond passwords:\n\n**Factor types:**\n• Something you know (password)\n• Something you have (phone, hardware key)\n• Something you are (biometrics)\n\n**MFA methods ranked by security:**\n1. 🥇 Hardware keys (YubiKey, Titan)\n2. 🥈 Authenticator apps (Google Auth, Authy)\n3. 🥉 Push notifications\n4. ⚠️ SMS codes (vulnerable to SIM swapping)\n\n**Even with MFA:** Advanced phishing can capture MFA tokens in real-time (adversary-in-the-middle). Always verify the legitimacy of login pages.",

    "default": "I'm PhishShield AI's security assistant. I can help with:\n\n🔹 **Phishing** — What it is and how to spot it\n🔹 **Spear Phishing** — Targeted attacks\n🔹 **BEC** — Business Email Compromise\n🔹 **Passwords** — Best practices\n🔹 **Reporting** — How to report threats\n🔹 **Social Engineering** — Psychological tactics\n🔹 **MFA** — Multi-factor authentication\n\nType any topic or question to learn more!"
}

QUIZ_BANK = [
    {
        "question": "You receive an email from 'security-alert@corp-audit-internal.com' with the subject 'URGENT: Account suspended in 15 min'. What do you do?",
        "options": [
            "A. Click the link immediately",
            "B. Forward to warn colleagues",
            "C. Report to IT Security & verify domain",
            "D. Delete and ignore"
        ],
        "correct": 2,
        "explanation": "Always report suspicious emails to IT Security and verify the domain independently. The domain 'corp-audit-internal.com' is not your company's domain."
    },
    {
        "question": "CEO emails you: 'Transfer $12,000 to vendor account ASAP.' Sender: ceo@acmecorp-directive.com. What do you do?",
        "options": [
            "A. Transfer immediately — it's the CEO",
            "B. Reply asking for confirmation",
            "C. Call the CEO directly on their known phone number to verify",
            "D. Forward to your manager"
        ],
        "correct": 2,
        "explanation": "Always verify financial requests through a separate, trusted communication channel. The domain 'acmecorp-directive.com' is a lookalike domain, not the real company domain."
    },
    {
        "question": "You receive a text: 'Your package delivery failed. Click here to reschedule.' You aren't expecting a package. What do you do?",
        "options": [
            "A. Click to check — it might be a surprise gift",
            "B. Delete the message immediately",
            "C. Go to the delivery company's official website directly",
            "D. Reply STOP to unsubscribe"
        ],
        "correct": 2,
        "explanation": "Never click links in unexpected texts. Go directly to the delivery company's official website or app to check status. This is a classic smishing (SMS phishing) attack."
    },
    {
        "question": "A pop-up says: 'Your computer is infected! Call Microsoft Support at 1-800-XXX.' What do you do?",
        "options": [
            "A. Call the number immediately",
            "B. Close the browser and run your antivirus",
            "C. Download the suggested cleanup tool",
            "D. Give them remote access to fix it"
        ],
        "correct": 1,
        "explanation": "This is a tech support scam. Microsoft will never show pop-ups with phone numbers. Close the browser (use Task Manager if needed) and run a legitimate antivirus scan."
    },
    {
        "question": "A colleague's email asks you to review an attached 'Q4_Report.xlsm' file. The email seems slightly off. What do you do?",
        "options": [
            "A. Open it — it's from a colleague",
            "B. Enable macros when prompted to view the report",
            "C. Contact your colleague through another channel to verify they sent it",
            "D. Save it to your desktop for later"
        ],
        "correct": 2,
        "explanation": "Files ending in .xlsm contain macros that can execute malicious code. Always verify unexpected attachments through a separate channel. The colleague's account may have been compromised."
    }
]

# ═══════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════
class SimulationState:
    def __init__(self):
        self.active_campaign = None
        self.telemetry_stream = []
        self.analytics = {
            "overall_resilience": 100.0,
            "org_risk_score": 0.0,
            "total_sent": 0,
            "total_clicks": 0,
            "total_credentials": 0,
            "total_reported": 0,
            "campaigns_run": 0,
            "department_risk": {dept: self._calc_dept_risk(dept) for dept in DEPARTMENTS},
            "total_employees": len(EMPLOYEES),
            "vulnerable_count": 0,
            "avg_awareness": 0.0
        }
        self.remediation_tasks = []
        self.leaderboard = []
        self.attack_timeline = []
        self.campaign_history = []
        self.current_insight_index = 0
        self.demo_running = False
        self._update_computed()

    def _calc_dept_risk(self, dept: str) -> float:
        emps = [e for e in EMPLOYEES if e["department"] == dept]
        return sum(e["risk_score"] for e in emps) / len(emps) if emps else 0.0

    def _update_computed(self):
        avg_risk = sum(e["risk_score"] for e in EMPLOYEES) / len(EMPLOYEES)
        self.analytics["overall_resilience"] = max(0.0, min(100.0, 100.0 - avg_risk))
        self.analytics["org_risk_score"] = round(avg_risk, 1)
        self.analytics["vulnerable_count"] = sum(1 for e in EMPLOYEES if e["risk_score"] > 50)
        self.analytics["avg_awareness"] = round(sum(e["awareness_score"] for e in EMPLOYEES) / len(EMPLOYEES), 1)
        for dept in DEPARTMENTS:
            self.analytics["department_risk"][dept] = round(self._calc_dept_risk(dept), 1)

    def get_next_insight(self):
        insight = AI_INSIGHTS[self.current_insight_index % len(AI_INSIGHTS)]
        self.current_insight_index += 1
        return insight

    def update_leaderboard(self):
        ranked = sorted(EMPLOYEES, key=lambda e: (e["reported"], e["awareness_score"], e["xp"]), reverse=True)[:10]
        self.leaderboard = [{
            "rank": i + 1,
            "name": e["name"],
            "dept": e["department"],
            "role": e["role"],
            "score": round(e["awareness_score"], 1),
            "reports": e["reported"],
            "xp": e["xp"],
            "badge": e["badge"],
            "streak": e["streak_days"]
        } for i, e in enumerate(ranked)]

state = SimulationState()

# ═══════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════
class CampaignGenRequest(BaseModel):
    department: str
    urgency: str
    psychological_vector: str

class PhishingDNA(BaseModel):
    fear: int
    urgency: int
    authority: int
    greed: int

class AIGeneratedTemplate(BaseModel):
    subject_line: str
    body_content: str
    sophistication_index: int
    attack_type: str
    social_engineering_strategy: str
    dna: Optional[PhishingDNA] = None

class LaunchRequest(BaseModel):
    department: str
    psychological_vector: str

class EmailScanRequest(BaseModel):
    sender_address: str
    domain_age_days: int
    spf_alignment: str
    urgency_keywords_count: int
    contains_malicious_redirection_link: bool

class ChatMessage(BaseModel):
    message: str

# ═══════════════════════════════════════════════════════════
# PAGE ROUTES
# ═══════════════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse)
async def serve_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# ═══════════════════════════════════════════════════════════
# AI CAMPAIGN GENERATOR
# ═══════════════════════════════════════════════════════════
PHISHING_TEMPLATES = {
    "Fear": {
        "subject": "⚠️ URGENT: {dept} Security Audit — Immediate Action Required",
        "body": """Dear {dept} Team Member,

Our automated intrusion detection system has flagged multiple unauthorized access attempts originating from your department's subnet at 02:14 AM UTC today.

Affected systems: Active Directory, VPN Gateway, SharePoint
Threat Level: CRITICAL
Estimated accounts at risk: 47

To prevent immediate suspension of your corporate credentials and potential data breach exposure, you must authenticate and complete an emergency identity verification within the next 15 minutes.

⚠️  Verification window expires in: 00:14:32

[VERIFY IDENTITY NOW] → https://corp-security-audit.internal-it.com/verify?token=a8f3d

Your cooperation is mandatory per SOC Protocol 7-B. Failure to verify will result in automatic credential revocation.

This message was generated by the IT Security Operations Center.
Do not reply to this email. Reference: INC-2024-8847

— IT Security Operations Center
   PhishShield AI Simulation""",
        "attack_type": "Fake Security Alert",
        "strategy": "Creates fear of account suspension and data breach. Employs a countdown timer to manufacture extreme urgency. Uses official-sounding internal domain and incident reference number for credibility. Multiple authority signals (SOC Protocol, auto-generated notice) bypass rational verification."
    },
    "Greed": {
        "subject": "🎉 CONFIDENTIAL: Q3 {dept} Performance Bonus — Claim Before 5 PM",
        "body": """Hello,

The Executive Compensation Committee has approved an off-cycle performance bonus exclusively for top-performing members of the {dept} division based on Q3 results.

Your individual allocation: $4,200.00 — Direct Deposit Available

This bonus is in addition to your standard compensation and reflects your department's exceptional contribution to company revenue targets.

To confirm your banking details and receive the direct deposit before the 5:00 PM EST processing cutoff today, please access the secure compensation portal below:

[CLAIM YOUR BONUS] → https://hr-payroll-portal.acmecorp-benefits.net/claim?ref=Q3-{dept}

⚠️ Important: Unclaimed allocations will be redistributed to other departments by end of business day. This offer is non-transferable and confidential.

Best regards,
Payroll & Compensation Team
AcmeCorp Human Resources
   PhishShield AI Simulation""",
        "attack_type": "Fake Payroll Portal",
        "strategy": "Exploits greed and FOMO with a believable financial reward tied to real department performance. Creates artificial scarcity with a hard EOD deadline. Requests sensitive banking information under the guise of a legitimate compensation process. 'Confidential' label prevents victims from verifying with colleagues."
    },
    "Urgency": {
        "subject": "🔴 CRITICAL: Mandatory {dept} Endpoint Security Patch — Deploy Within 60 Minutes",
        "body": """ALL {dept} PERSONNEL — IMMEDIATE ACTION REQUIRED

A critical zero-day vulnerability (CVE-2024-8821) affecting Microsoft Windows endpoint systems has been publicly disclosed by CISA. Our threat intelligence indicates active exploitation by APT groups targeting organizations in our sector.

Vulnerability Details:
• CVE: CVE-2024-8821 (CVSS 9.8 — Critical)
• Attack Vector: Remote Code Execution via network
• Affected: All Windows 10/11 endpoints
• Status: Active exploitation in the wild

You are required to install the emergency security patch immediately by clicking the link below. Systems not patched within 60 minutes will be forcibly disconnected from the corporate VPN to protect the network.

[DOWNLOAD EMERGENCY PATCH] → https://patch-deploy.it-helpdesk-internal.com/CVE-2024-8821

Deadline: 60 minutes from receipt | Enforced by: Network Security Team

— Office of the Chief Information Security Officer
   PhishShield AI Simulation""",
        "attack_type": "Fake Software Patch",
        "strategy": "Exploits fear of losing network access and being unable to work. References a realistic CVE number and CISA advisory for credibility. CVSS score adds technical authority. Tight 60-minute deadline with VPN disconnection threat bypasses rational verification. Technical details make non-technical users trust the legitimacy."
    },
    "Authority": {
        "subject": "Re: {dept} — Strategic Reorganization Brief [HIGHLY CONFIDENTIAL]",
        "body": """[Sent from mobile — excuse brevity]

{dept} Team,

I need you to urgently review the attached document regarding the upcoming structural reorganization that will affect your division. The board approved this last night and we're announcing internally on Monday.

This is HIGHLY CONFIDENTIAL — please do NOT forward this email or discuss with anyone outside your direct team until the official announcement.

Access the document using your corporate SSO credentials:
[VIEW CONFIDENTIAL REORGANIZATION BRIEF] → https://sharepoint-docs.acmecorp-internal.net/exec/reorg-brief

I need your written acknowledgment by COB today. If I don't hear back, I'll assume you're aligned with the proposed changes to your department.

Thanks,
Michael Chen
Chief Executive Officer
AcmeCorp Inc.

Sent from my iPhone
   PhishShield AI Simulation""",
        "attack_type": "CEO Impersonation (BEC)",
        "strategy": "Classic Business Email Compromise impersonating the CEO. Leverages authority, urgency, and confidentiality to prevent the target from verifying with colleagues. 'Sent from iPhone' explains brief/informal tone. Implied threat ('I'll assume you're aligned') creates pressure to act. Requests SSO credential entry on a fake SharePoint portal."
    }
}

@app.post("/api/v1/campaigns/generate", response_model=AIGeneratedTemplate)
async def generate_campaign(req: CampaignGenRequest):
    template = PHISHING_TEMPLATES.get(req.psychological_vector, PHISHING_TEMPLATES["Fear"])
    si_map = {"Low": 4, "Medium": 7, "Critical": 9}
    
    dna_map = {
        "Fear": {"fear": 85, "urgency": 70, "authority": 40, "greed": 10},
        "Greed": {"fear": 10, "urgency": 60, "authority": 20, "greed": 95},
        "Urgency": {"fear": 30, "urgency": 90, "authority": 50, "greed": 20},
        "Authority": {"fear": 40, "urgency": 60, "authority": 95, "greed": 5}
    }
    dna_vals = dna_map.get(req.psychological_vector, {"fear": 50, "urgency": 50, "authority": 50, "greed": 50})
    
    return AIGeneratedTemplate(
        subject_line=template["subject"].replace("{dept}", req.department),
        body_content=template["body"].replace("{dept}", req.department),
        sophistication_index=si_map.get(req.urgency, 5),
        attack_type=template["attack_type"],
        social_engineering_strategy=template["strategy"],
        dna=PhishingDNA(**dna_vals)
    )

# ═══════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════
async def simulation_engine_loop(department: str, vector: str):
    state.analytics["campaigns_run"] += 1
    targets = [e for e in EMPLOYEES if e["department"] == department] if department != "All" else EMPLOYEES
    state.analytics["total_sent"] += len(targets)

    campaign_record = {
        "id": f"CAMP-{state.analytics['campaigns_run']:04d}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "department": department,
        "vector": vector,
        "targets": len(targets),
        "clicks": 0,
        "credentials": 0,
        "reported": 0,
        "status": "RUNNING"
    }
    state.campaign_history.insert(0, campaign_record)

    state.attack_timeline.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": f"🚀 Campaign {campaign_record['id']} deployed to {len(targets)} targets in {department}",
        "type": "launch", "severity": "info"
    })

    for emp in targets:
        state.telemetry_stream.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "user": emp["name"], "dept": emp["department"],
            "action": "📧 Email Delivered", "status": "info"
        })
        await asyncio.sleep(random.uniform(0.2, 0.6))

        chance = random.random()
        click_prob = 0.15 + (emp["risk_score"] / 250.0)

        if chance < click_prob:
            # User clicked
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"], "dept": emp["department"],
                "action": "⚡ Link Clicked", "status": "warning"
            })
            state.analytics["total_clicks"] += 1
            campaign_record["clicks"] += 1
            emp["risk_score"] = min(100.0, emp["risk_score"] + 35.0)
            emp["awareness_score"] = max(0.0, emp["awareness_score"] - 12.0)
            emp["clicked_count"] += 1
            emp["streak_days"] = 0

            state.attack_timeline.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "event": f"⚡ {emp['name']} ({emp['department']}) clicked phishing link",
                "type": "click", "severity": "warning"
            })

            await asyncio.sleep(random.uniform(0.2, 0.8))

            if random.random() < 0.55:
                # Credentials compromised
                state.telemetry_stream.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"], "dept": emp["department"],
                    "action": "🔓 Credentials Compromised", "status": "danger"
                })
                state.analytics["total_credentials"] += 1
                campaign_record["credentials"] += 1
                emp["risk_score"] = min(100.0, emp["risk_score"] + 45.0)
                emp["awareness_score"] = max(0.0, emp["awareness_score"] - 20.0)
                emp["compromised"] = True
                emp["xp"] = max(0, emp["xp"] - 50)

                remediation_map = {
                    "Fear": "Defeating Intimidation & Fear Tactics",
                    "Greed": "Identifying Too-Good-To-Be-True Lures",
                    "Urgency": "Resisting High-Pressure Deadlines",
                    "Authority": "Verifying Executive Directives (BEC)"
                }
                state.remediation_tasks.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"], "dept": emp["department"],
                    "module": remediation_map.get(vector, "General Phishing Awareness"),
                    "status": "AUTO-ASSIGNED", "priority": "CRITICAL"
                })
                state.attack_timeline.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "event": f"🚨 BREACH: {emp['name']} credentials compromised via {vector} vector",
                    "type": "compromise", "severity": "critical"
                })

        elif chance > 0.65:
            # User reported
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"], "dept": emp["department"],
                "action": "🛡️ Reported to Security", "status": "success"
            })
            state.analytics["total_reported"] += 1
            campaign_record["reported"] += 1
            emp["risk_score"] = max(0.0, emp["risk_score"] - 25.0)
            emp["awareness_score"] = min(100.0, emp["awareness_score"] + 8.0)
            emp["reported"] += 1
            emp["xp"] += 75
            emp["streak_days"] += 1
            if emp["reported"] >= 3:
                emp["badge"] = "Defender"
            if emp["reported"] >= 6:
                emp["badge"] = "Hunter"
            if emp["reported"] >= 10:
                emp["badge"] = "Guardian"

        emp["last_simulation"] = datetime.now().strftime("%H:%M:%S")
        state._update_computed()
        state.update_leaderboard()

        # Trim buffers
        if len(state.telemetry_stream) > 150:
            state.telemetry_stream = state.telemetry_stream[:150]
        if len(state.remediation_tasks) > 80:
            state.remediation_tasks = state.remediation_tasks[:80]
        if len(state.attack_timeline) > 50:
            state.attack_timeline = state.attack_timeline[:50]

    campaign_record["status"] = "COMPLETED"

@app.post("/api/v1/campaigns/launch")
async def launch_simulation(req: LaunchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulation_engine_loop, req.department, req.psychological_vector)
    return {"status": "Simulation Pipeline Triggered", "campaign_id": f"CAMP-{state.analytics['campaigns_run'] + 1:04d}"}

# ═══════════════════════════════════════════════════════════
# DEMO MODE — AUTO-RUN FOR HACKATHON JUDGES
# ═══════════════════════════════════════════════════════════
async def demo_mode_runner():
    state.demo_running = True
    vectors = ["Fear", "Authority", "Urgency", "Greed"]
    for v in vectors:
        dept = random.choice(DEPARTMENTS)
        await simulation_engine_loop(dept, v)
        await asyncio.sleep(1)
    state.demo_running = False

@app.post("/api/v1/demo/start")
async def start_demo_mode(background_tasks: BackgroundTasks):
    if state.demo_running:
        return {"status": "Demo already running"}
    background_tasks.add_task(demo_mode_runner)
    return {"status": "Demo Mode Activated — Sit back and watch the chaos"}

# ═══════════════════════════════════════════════════════════
# DATA ENDPOINTS
# ═══════════════════════════════════════════════════════════
@app.get("/api/v1/telemetry/stream")
async def get_telemetry():
    return state.telemetry_stream[:80]

@app.get("/api/v1/analytics/metrics")
async def get_metrics():
    return state.analytics

@app.get("/api/v1/remediation/queue")
async def get_remediation():
    return state.remediation_tasks[:30]

@app.get("/api/v1/leaderboard")
async def get_leaderboard():
    return state.leaderboard

@app.get("/api/v1/attack-timeline")
async def get_timeline():
    return state.attack_timeline[:30]

@app.get("/api/v1/insights/next")
async def get_insight():
    return {"insight": state.get_next_insight()}

@app.get("/api/v1/employees/top-risk")
async def get_top_risk():
    top = sorted(EMPLOYEES, key=lambda e: e["risk_score"], reverse=True)[:10]
    return [{"name": e["name"], "dept": e["department"], "role": e["role"],
             "risk": round(e["risk_score"], 1), "email": e["email"],
             "badge": e["badge"]} for e in top]

@app.get("/api/v1/employees/directory")
async def get_employee_directory():
    return [{
        "id": e["id"], "name": e["name"], "email": e["email"],
        "department": e["department"], "role": e["role"],
        "risk_score": round(e["risk_score"], 1),
        "awareness_score": round(e["awareness_score"], 1),
        "badge": e["badge"], "xp": e["xp"],
        "compromised": e["compromised"]
    } for e in EMPLOYEES]

@app.get("/api/v1/campaigns/history")
async def get_campaign_history():
    return state.campaign_history[:20]

@app.get("/api/v1/analytics/dept-comparison")
async def get_dept_comparison():
    result = []
    for dept in DEPARTMENTS:
        emps = [e for e in EMPLOYEES if e["department"] == dept]
        result.append({
            "department": dept,
            "head": DEPT_HEADS[dept],
            "employee_count": len(emps),
            "avg_risk": round(sum(e["risk_score"] for e in emps) / len(emps), 1),
            "avg_awareness": round(sum(e["awareness_score"] for e in emps) / len(emps), 1),
            "compromised_count": sum(1 for e in emps if e["compromised"]),
            "total_reports": sum(e["reported"] for e in emps),
            "total_xp": sum(e["xp"] for e in emps)
        })
    return result

# ═══════════════════════════════════════════════════════════
# AI CHATBOT
# ═══════════════════════════════════════════════════════════
# Helper to fetch reply from Gemini API if GEMINI_API_KEY is configured
async def get_gemini_reply(user_message: str) -> Optional[str]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    system_instruction = (
        "You are PhishShield AI's security assistant, a premium cyber-psychology and security awareness chatbot. "
        "Help the user understand social engineering, phishing (spear phishing, BEC, vishing, smishing), password security, "
        "MFA, and incident reporting. "
        "Keep your responses concise, highly informative, formatted in clean Markdown, and use bullet points and cyber emojis where appropriate."
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": system_instruction}
            ]
        }
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        loop = asyncio.get_event_loop()
        def do_request():
            with urllib.request.urlopen(req, timeout=8) as response:
                return response.read().decode("utf-8")
        res_data = await loop.run_in_executor(None, do_request)
        res_json = json.loads(res_data)
        reply = res_json['candidates'][0]['content']['parts'][0]['text']
        return reply
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

@app.post("/api/v1/chatbot/message")
async def chatbot_reply(msg: ChatMessage):
    query = msg.message.lower().strip()
    
    # Try calling Gemini first
    gemini_reply = await get_gemini_reply(msg.message)
    if gemini_reply:
        return {"reply": gemini_reply}
        
    # Match keywords to responses
    if any(k in query for k in ["phish", "what is phish", "identify"]):
        return {"reply": CHATBOT_RESPONSES["phishing"]}
    elif any(k in query for k in ["spear", "targeted", "personalized"]):
        return {"reply": CHATBOT_RESPONSES["spear"]}
    elif any(k in query for k in ["bec", "business email", "ceo fraud", "wire"]):
        return {"reply": CHATBOT_RESPONSES["bec"]}
    elif any(k in query for k in ["password", "credential", "strong pass"]):
        return {"reply": CHATBOT_RESPONSES["password"]}
    elif any(k in query for k in ["report", "suspicious", "flag"]):
        return {"reply": CHATBOT_RESPONSES["report"]}
    elif any(k in query for k in ["social engineer", "manipulation", "tactic", "psychology"]):
        return {"reply": CHATBOT_RESPONSES["social"]}
    elif any(k in query for k in ["mfa", "2fa", "multi-factor", "authenticat"]):
        return {"reply": CHATBOT_RESPONSES["mfa"]}
    elif any(k in query for k in ["vishing", "voice", "phone call", "smishing", "sms"]):
        return {"reply": "📞 **Vishing & Smishing:**\n\nVishing (voice phishing) uses phone calls to trick victims. Smishing uses SMS text messages.\n\n**Common vishing tactics:**\n• Fake bank fraud alerts\n• IRS/tax scam calls\n• Tech support impersonation\n• Fake prize winnings\n\n**Common smishing tactics:**\n• Package delivery notifications\n• Bank account alerts\n• Prize/lottery messages\n\n**Defense:** Never give personal info over unsolicited calls. Hang up and call the organization directly using their official number."}
    elif any(k in query for k in ["ransomware", "ransom", "encrypt", "malware"]):
        return {"reply": "🔒 **Ransomware:**\n\nRansomware is malware that encrypts your files and demands payment for the decryption key.\n\n**How it spreads:**\n• Phishing email attachments (.exe, .zip, .docm)\n• Drive-by downloads from compromised sites\n• RDP brute-force attacks\n• Supply chain compromises\n\n**Prevention:**\n• Regular offline backups (3-2-1 rule)\n• Patch systems promptly\n• Disable macros in Office docs\n• Use endpoint detection (EDR)\n• Network segmentation\n\n**If infected:** Isolate the machine immediately. Do NOT pay the ransom. Contact your security team and law enforcement."}
    elif any(k in query for k in ["zero-day", "zero day", "0day", "exploit", "vulnerability"]):
        return {"reply": "💀 **Zero-Day Exploits:**\n\nA zero-day is a software vulnerability unknown to the vendor, giving them 'zero days' to fix it before exploitation.\n\n**Why they matter:**\n• No patch exists yet\n• Traditional antivirus can't detect them\n• Often sold on dark web for $50K-$2.5M\n• Used in advanced persistent threats (APTs)\n\n**Protection strategies:**\n• Behavior-based detection (EDR/XDR)\n• Network anomaly monitoring\n• Application sandboxing\n• Principle of least privilege\n• Regular security assessments"}
    elif any(k in query for k in ["spoofing", "spoof", "impersonat", "fake domain"]):
        return {"reply": "🎭 **Email Spoofing:**\n\nSpoofing forges the 'From' address to make emails appear from trusted senders.\n\n**Types of spoofing:**\n• Display name spoofing (easiest)\n• Domain spoofing (blocked by SPF/DKIM)\n• Lookalike domains (acmecorp vs acrnecorp)\n• Reply-to manipulation\n\n**Detection:**\n• Check full email headers\n• Verify SPF, DKIM, and DMARC records\n• Hover over sender address\n• Look for typosquatting in domains\n\n**Prevention:** Implement DMARC with 'reject' policy. Train employees to inspect sender details."}
    elif any(k in query for k in ["whaling", "executive", "cxo", "ceo"]):
        return {"reply": "🐋 **Whaling Attacks:**\n\nWhaling targets C-suite executives and senior leaders with highly personalized attacks.\n\n**Why executives are targeted:**\n• Authority to approve large transfers\n• Access to sensitive strategic data\n• Often bypass security controls\n• Public profiles make research easy\n\n**Common whaling scenarios:**\n• Fake legal subpoenas\n• Board meeting document lures\n• M&A-related urgent requests\n• Tax filing fraud\n\n**Defense:** Implement out-of-band verification for all financial requests. Limit executive email metadata exposure."}
    elif any(k in query for k in ["train", "aware", "learn", "education"]):
        return {"reply": "📚 **Security Awareness Training:**\n\nEffective training programs reduce phishing click rates by up to 75%.\n\n**Best practices:**\n• Regular simulated phishing campaigns\n• Bite-sized micro-learning modules\n• Role-specific training content\n• Gamification (badges, leaderboards)\n• Immediate feedback on failures\n• Positive reinforcement, not punishment\n\n**PhishShield AI approach:** We use adaptive AI to customize training based on each employee's specific vulnerabilities, ensuring the most relevant content is delivered at the right time."}
    elif any(k in query for k in ["help", "what can", "how do", "explain"]):
        return {"reply": CHATBOT_RESPONSES["default"]}
    else:
        return {"reply": CHATBOT_RESPONSES["default"]}

@app.get("/api/v1/quiz/question")
async def get_quiz_question(index: int = 0):
    q = QUIZ_BANK[index % len(QUIZ_BANK)]
    return q

@app.get("/api/v1/debug/env")
async def debug_env():
    key = os.environ.get("GEMINI_API_KEY", "")
    api_test_result = "not_run"
    api_error = None
    if key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": "Hello"}]}]
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = response.read().decode("utf-8")
                res_json = json.loads(res_data)
                api_test_result = "success"
        except Exception as e:
            api_test_result = "failed"
            api_error = str(e)
            if hasattr(e, 'read'):
                try:
                    api_error += f" | Response: {e.read().decode('utf-8')}"
                except:
                    pass
    return {
        "gemini_api_key_configured": len(key) > 0,
        "key_length": len(key),
        "key_prefix": key[:4] if len(key) > 4 else "",
        "api_test_result": api_test_result,
        "api_error": api_error
    }


# ═══════════════════════════════════════════════════════════
# DEFENSIVE INBOX GUARDIAN
# ═══════════════════════════════════════════════════════════
class DefenseState:
    def __init__(self):
        self.monitored_stream = []
        try:
            with open(os.path.join(BASE_DIR, "synthetic_dataset.json"), "r") as f:
                self.dataset = json.load(f)
        except Exception:
            self.dataset = []
        self.dataset_index = 0
        self.stats = {"safe": 0, "suspicious": 0, "critical": 0}

defense_state = DefenseState()

@app.post("/api/v1/defense/scan")
async def scan_email(req: EmailScanRequest):
    classification = "SAFE"
    reasoning = "Domain is established, SPF records align, and no urgent/malicious traits detected."
    if req.domain_age_days < 30 and req.urgency_keywords_count > 3:
        classification = "HIGH_RISK_SPAM"
        reasoning = f"CRITICAL: Domain newly registered ({req.domain_age_days} days). Combined with {req.urgency_keywords_count} urgency keywords — high-confidence phishing vector."
    elif req.contains_malicious_redirection_link or req.spf_alignment == "FAIL":
        classification = "SUSPICIOUS"
        reasoning = f"WARNING: SPF Alignment: {req.spf_alignment}. Malicious redirect detected: {req.contains_malicious_redirection_link}."
    return {"classification": classification, "reasoning": reasoning,
            "structural_score": random.randint(8, 35) if classification != "SAFE" else random.randint(78, 100)}

@app.get("/api/v1/defense/stream")
async def get_defense_stream():
    if defense_state.dataset:
        entry = defense_state.dataset[defense_state.dataset_index % len(defense_state.dataset)]
        defense_state.dataset_index += 1
        req = EmailScanRequest(**entry)
        classification = "SAFE"
        reasoning = "Domain established. SPF aligned. No anomalies."
        if req.domain_age_days < 30 and req.urgency_keywords_count > 3:
            classification = "HIGH_RISK_SPAM"
            reasoning = f"CRITICAL: Domain age {req.domain_age_days}d + {req.urgency_keywords_count} urgency keywords. Zero-day phishing vector."
            defense_state.stats["critical"] += 1
        elif req.contains_malicious_redirection_link or req.spf_alignment == "FAIL":
            classification = "SUSPICIOUS"
            reasoning = f"WARNING: SPF={req.spf_alignment}. Malicious redirect={req.contains_malicious_redirection_link}."
            defense_state.stats["suspicious"] += 1
        else:
            defense_state.stats["safe"] += 1

        defense_state.monitored_stream.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "sender": entry["sender_address"],
            "subject": entry.get("subject", "No Subject"),
            "domain_age": entry["domain_age_days"],
            "structural_score": entry.get("structural_score", random.randint(20, 95)),
            "classification": classification,
            "reasoning": reasoning
        })
        if len(defense_state.monitored_stream) > 25:
            defense_state.monitored_stream = defense_state.monitored_stream[:25]

    return defense_state.monitored_stream

@app.get("/api/v1/defense/stats")
async def get_defense_stats():
    return defense_state.stats

# ═══════════════════════════════════════════════════════════
# AUTHENTICATION (Demo)
# ═══════════════════════════════════════════════════════════
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/auth/login")
async def login(req: LoginRequest):
    valid_creds = {
        "admin": "phishshield2024",
        "security": "defender123",
        "demo": "demo"
    }
    if req.username in valid_creds and req.password == valid_creds[req.username]:
        role_map = {"admin": "Super Admin", "security": "Security Team", "demo": "Demo User"}
        return {"success": True, "role": role_map.get(req.username, "Employee"), "token": "PS-AI-TOKEN-2024"}
    return {"success": False, "error": "Invalid credentials"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
