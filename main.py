import asyncio
import random
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os
import json

app = FastAPI(title="PhishShield AI - Enterprise Platform")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Richer Employee Dataset ---
DEPARTMENTS = ["Finance", "HR", "Engineering", "Sales", "Legal", "Marketing"]
FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ivan", "Julia",
               "Kevin", "Laura", "Mike", "Nina", "Oscar", "Priya", "Quinn", "Rachel", "Sam", "Tara",
               "Uma", "Victor", "Wendy", "Xander", "Yara", "Zack", "Aiden", "Bella", "Carlos", "Dana"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez",
              "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "White",
              "Harris", "Thompson", "Chen", "Park", "Patel", "Kim", "Singh", "Nguyen", "Lopez", "Gonzalez"]

EMPLOYEES = []
for i in range(1, 101):
    dept = random.choice(DEPARTMENTS)
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    EMPLOYEES.append({
        "id": f"EMP{i:03d}",
        "name": name,
        "email": f"{name.lower().replace(' ', '.')}@acmecorp.com",
        "department": dept,
        "risk_score": float(random.randint(10, 35)),
        "awareness_score": float(random.randint(65, 95)),
        "trainings_completed": random.randint(0, 5),
        "compromised": False,
        "reported": 0,
        "badge": "Defender" if random.random() > 0.7 else "Trainee"
    })

# --- AI Insights Rotator ---
AI_INSIGHTS = [
    "Finance department shows high susceptibility to urgency-based phishing vectors.",
    "Most users fail on spoofed internal domain names with visual typosquatting.",
    "Users respond poorly during high-pressure end-of-quarter simulations.",
    "HR is most vulnerable to authority-based attacks impersonating C-suite executives.",
    "Engineering team clicks rates spike on fake GitHub credential reset emails.",
    "Sales users are susceptible to fake invoice and payment portal scams.",
    "Legal department shows strong reporting behavior — 42% report rate this cycle.",
    "Predicted: Next campaign targeting Finance+Sales will achieve 38% click rate.",
    "Risk forecast: Urgency attacks will increase 22% in next 30 days based on trends.",
    "Recommended: Deploy mandatory training for 12 high-risk users immediately."
]

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
            "department_risk": {dept: self.calculate_dept_risk(dept) for dept in DEPARTMENTS}
        }
        self.remediation_tasks = []
        self.leaderboard = []
        self.attack_timeline = []
        self.current_insight_index = 0

    def calculate_dept_risk(self, dept: str) -> float:
        dept_emps = [e for e in EMPLOYEES if e["department"] == dept]
        if not dept_emps: return 0.0
        return sum(e["risk_score"] for e in dept_emps) / len(dept_emps)

    def update_overall_resilience(self):
        avg_risk = sum(e["risk_score"] for e in EMPLOYEES) / len(EMPLOYEES)
        self.analytics["overall_resilience"] = max(0.0, min(100.0, 100.0 - avg_risk))
        self.analytics["org_risk_score"] = round(avg_risk, 1)

    def get_next_insight(self):
        insight = AI_INSIGHTS[self.current_insight_index % len(AI_INSIGHTS)]
        self.current_insight_index += 1
        return insight

    def update_leaderboard(self):
        # Top reporters and highest awareness scores
        reporters = sorted(EMPLOYEES, key=lambda e: e["reported"], reverse=True)[:5]
        self.leaderboard = [{
            "name": e["name"],
            "dept": e["department"],
            "score": round(e["awareness_score"], 1),
            "reports": e["reported"],
            "badge": e["badge"]
        } for e in reporters]

state = SimulationState()
state.update_overall_resilience()

# --- Models ---
class CampaignGenRequest(BaseModel):
    department: str
    urgency: str
    psychological_vector: str

class AIGeneratedTemplate(BaseModel):
    subject_line: str
    body_content: str
    sophistication_index: int
    attack_type: str
    social_engineering_strategy: str

class LaunchRequest(BaseModel):
    department: str
    psychological_vector: str

class EmailScanRequest(BaseModel):
    sender_address: str
    domain_age_days: int
    spf_alignment: str
    urgency_keywords_count: int
    contains_malicious_redirection_link: bool

# --- Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/v1/campaigns/generate", response_model=AIGeneratedTemplate)
async def generate_campaign(req: CampaignGenRequest):
    templates_db = {
        "Fear": {
            "subject": f"⚠️ URGENT: {req.department} Security Audit — Immediate Action Required",
            "body": f"""Dear {req.department} Team Member,

Our automated intrusion detection system has flagged multiple unauthorized access attempts originating from your department's subnet at 02:14 AM UTC.

To prevent immediate suspension of your corporate credentials and potential data breach, you must authenticate and complete an emergency identity verification.

⚠️  This access window expires in: 00:14:32

[VERIFY IDENTITY NOW] → https://corp-security-audit.internal-it.com/verify

Your cooperation is mandatory per SOC Protocol 7-B.

— IT Security Operations Center""",
            "attack_type": "Fake Security Alert",
            "strategy": "Creates fear of account suspension and data breach. Employs a countdown timer to manufacture urgency. Uses official-sounding internal domain to appear legitimate."
        },
        "Greed": {
            "subject": f"🎉 CONFIDENTIAL: Q3 {req.department} Profit Sharing Payout — Action Required",
            "body": f"""Hello,

The Executive Board has approved an off-cycle profit-sharing distribution exclusively for top performers in the {req.department} division.

Your allocation: $4,200 — Direct Deposit Available

To confirm your banking details before the 5 PM cutoff, please access the secure compensation portal below. This offer is not transferable.

[CLAIM YOUR ALLOCATION] → https://hr-payroll-portal.acmecorp-benefits.net/claim

Note: Unclaimed funds will be redistributed by EOD.

Best,
Payroll & Compensation Team""",
            "attack_type": "Fake Payroll Portal",
            "strategy": "Exploits greed and FOMO with a fake financial reward. Creates artificial scarcity with a hard deadline. Requests sensitive banking information under the guise of a legitimate benefit."
        },
        "Urgency": {
            "subject": f"🔴 CRITICAL: Mandatory {req.department} Endpoint Security Patch — Deploy NOW",
            "body": f"""All {req.department} Personnel — IMMEDIATE ACTION REQUIRED

A critical zero-day vulnerability (CVE-2024-8821) affecting our endpoint systems has been publicly disclosed. Threat actors are actively exploiting this vulnerability in the wild.

You are required to install the emergency security patch immediately.
Systems not patched within 60 minutes will be forcibly disconnected from VPN.

[DOWNLOAD EMERGENCY PATCH] → https://patch-deploy.it-helpdesk-internal.com/CVE-2024-8821

Severity: CRITICAL | Affected: All Windows endpoints | Deadline: 60 minutes

— CISO Office""",
            "attack_type": "Fake Software Patch",
            "strategy": "Exploits fear of being disconnected from work systems. References a realistic CVE number for credibility. Tight 60-minute deadline bypasses rational thinking."
        },
        "Authority": {
            "subject": f"Re: {req.department} — Strategic Reorganization Brief [CONFIDENTIAL]",
            "body": f"""[This message was sent from the CEO's mobile device]

{req.department} Team,

Please review the attached highly confidential document regarding the upcoming structural reorganization affecting your division. This has not been publicly announced.

Given the sensitivity, please do NOT forward this email. Access the document using your corporate SSO credentials.

[VIEW CONFIDENTIAL BRIEF] → https://sharepoint-docs.acmecorp-internal.net/brief/reorg

Your acknowledgment is required by COB today.

— Michael Chen, Chief Executive Officer""",
            "attack_type": "CEO Impersonation (BEC)",
            "strategy": "Business Email Compromise impersonating C-suite. Leverages authority and confidentiality to prevent the target from verifying with colleagues. Requests SSO credential entry."
        }
    }

    selected = templates_db.get(req.psychological_vector, templates_db["Fear"])
    si_map = {"Low": 4, "Medium": 7, "Critical": 9}
    sophistication = si_map.get(req.urgency, 5)

    return AIGeneratedTemplate(
        subject_line=selected["subject"],
        body_content=selected["body"],
        sophistication_index=sophistication,
        attack_type=selected["attack_type"],
        social_engineering_strategy=selected["strategy"]
    )

async def simulation_engine_loop(department: str, vector: str):
    state.analytics["campaigns_run"] += 1
    targets = [e for e in EMPLOYEES if e["department"] == department] if department != "All" else EMPLOYEES
    state.analytics["total_sent"] += len(targets)

    state.attack_timeline.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": f"Campaign deployed to {len(targets)} targets in {department}",
        "type": "launch"
    })

    for emp in targets:
        state.telemetry_stream.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "user": emp["name"],
            "dept": emp["department"],
            "action": "Email Delivered",
            "status": "info"
        })
        await asyncio.sleep(random.uniform(0.3, 0.8))

        chance = random.random()
        base_click_prob = 0.2 + (emp["risk_score"] / 200.0)

        if chance < base_click_prob:
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"],
                "dept": emp["department"],
                "action": "Link Clicked ⚡",
                "status": "warning"
            })
            state.analytics["total_clicks"] += 1
            emp["risk_score"] = min(100.0, emp["risk_score"] + 45.0)
            emp["awareness_score"] = max(0.0, emp["awareness_score"] - 15.0)

            state.attack_timeline.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "event": f"{emp['name']} clicked phishing link",
                "type": "click"
            })

            await asyncio.sleep(random.uniform(0.3, 1.0))

            if random.random() < 0.6:
                state.telemetry_stream.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"],
                    "dept": emp["department"],
                    "action": "Credentials Entered 🔓",
                    "status": "danger"
                })
                state.analytics["total_credentials"] += 1
                emp["risk_score"] = min(100.0, emp["risk_score"] + 55.0)
                emp["awareness_score"] = max(0.0, emp["awareness_score"] - 25.0)
                emp["compromised"] = True

                task_map = {
                    "Fear": "Defeating Intimidation Scams",
                    "Greed": "Identifying Too-Good-To-Be-True Lures",
                    "Urgency": "Resisting High-Pressure Tactics",
                    "Authority": "Verifying Executive Directives (BEC)"
                }

                state.remediation_tasks.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"],
                    "dept": emp["department"],
                    "module": task_map.get(vector, "General Phishing Awareness"),
                    "status": "Assigned",
                    "priority": "HIGH"
                })

                state.attack_timeline.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "event": f"⚠️ Credentials compromised: {emp['name']}",
                    "type": "compromise"
                })

        elif chance > 0.7:
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"],
                "dept": emp["department"],
                "action": "Reported to Security ✅",
                "status": "success"
            })
            state.analytics["total_reported"] += 1
            emp["risk_score"] = max(0.0, emp["risk_score"] - 30.0)
            emp["awareness_score"] = min(100.0, emp["awareness_score"] + 10.0)
            emp["reported"] += 1
            if emp["reported"] >= 2:
                emp["badge"] = "Defender"

        state.analytics["department_risk"][emp["department"]] = state.calculate_dept_risk(emp["department"])
        state.update_overall_resilience()
        state.update_leaderboard()

        if len(state.telemetry_stream) > 100:
            state.telemetry_stream = state.telemetry_stream[:100]
        if len(state.remediation_tasks) > 50:
            state.remediation_tasks = state.remediation_tasks[:50]
        if len(state.attack_timeline) > 30:
            state.attack_timeline = state.attack_timeline[:30]

@app.post("/api/v1/campaigns/launch")
async def launch_simulation(req: LaunchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulation_engine_loop, req.department, req.psychological_vector)
    return {"status": "Simulation Pipeline Triggered"}

@app.get("/api/v1/telemetry/stream")
async def get_telemetry_stream():
    return state.telemetry_stream

@app.get("/api/v1/analytics/metrics")
async def get_analytics_metrics():
    return state.analytics

@app.get("/api/v1/remediation/queue")
async def get_remediation_queue():
    return state.remediation_tasks

@app.get("/api/v1/leaderboard")
async def get_leaderboard():
    return state.leaderboard

@app.get("/api/v1/attack-timeline")
async def get_attack_timeline():
    return state.attack_timeline

@app.get("/api/v1/insights/next")
async def get_next_insight():
    return {"insight": state.get_next_insight()}

@app.get("/api/v1/employees/top-risk")
async def get_top_risk_employees():
    top = sorted(EMPLOYEES, key=lambda e: e["risk_score"], reverse=True)[:8]
    return [{"name": e["name"], "dept": e["department"],
             "risk": round(e["risk_score"], 1), "email": e["email"]} for e in top]

# --- Defensive Inbox Guardian ---
class DefenseState:
    def __init__(self):
        self.monitored_stream = []
        try:
            with open(os.path.join(BASE_DIR, "synthetic_dataset.json"), "r") as f:
                self.dataset = json.load(f)
        except Exception:
            self.dataset = []
        self.dataset_index = 0

defense_state = DefenseState()

@app.post("/api/v1/defense/scan")
async def scan_email(req: EmailScanRequest):
    classification = "SAFE"
    reasoning = "Domain is established, SPF records align, and no urgent/malicious traits detected."

    if req.domain_age_days < 30 and req.urgency_keywords_count > 3:
        classification = "HIGH_RISK_SPAM"
        reasoning = f"CRITICAL: Domain is newly registered ({req.domain_age_days} days old) combined with high-urgency language ({req.urgency_keywords_count} keywords). Likely a zero-day phishing attack."
    elif req.contains_malicious_redirection_link or req.spf_alignment == "FAIL":
        classification = "SUSPICIOUS"
        reasoning = f"WARNING: Structural anomalies detected. SPF Alignment: {req.spf_alignment}. Malicious Redirect: {req.contains_malicious_redirection_link}."

    return {
        "classification": classification,
        "reasoning": reasoning,
        "structural_score": random.randint(10, 40) if classification != "SAFE" else random.randint(80, 100)
    }

@app.get("/api/v1/defense/stream")
async def get_defense_stream():
    if defense_state.dataset:
        new_email = defense_state.dataset[defense_state.dataset_index % len(defense_state.dataset)]
        defense_state.dataset_index += 1

        scan_req = EmailScanRequest(**new_email)
        classification = "SAFE"
        reasoning = "Domain is established, SPF records align, and no urgent/malicious traits detected."

        if scan_req.domain_age_days < 30 and scan_req.urgency_keywords_count > 3:
            classification = "HIGH_RISK_SPAM"
            reasoning = f"CRITICAL: Domain newly registered ({scan_req.domain_age_days} days old) + {scan_req.urgency_keywords_count} urgency keywords. Zero-day phishing vector detected."
        elif scan_req.contains_malicious_redirection_link or scan_req.spf_alignment == "FAIL":
            classification = "SUSPICIOUS"
            reasoning = f"WARNING: SPF Alignment: {scan_req.spf_alignment}. Malicious redirection link: {scan_req.contains_malicious_redirection_link}."

        event = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "sender": new_email["sender_address"],
            "subject": new_email["subject"],
            "domain_age": new_email["domain_age_days"],
            "structural_score": new_email["structural_score"],
            "classification": classification,
            "reasoning": reasoning
        }

        defense_state.monitored_stream.insert(0, event)
        if len(defense_state.monitored_stream) > 20:
            defense_state.monitored_stream = defense_state.monitored_stream[:20]

    return defense_state.monitored_stream

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
