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

app = FastAPI(title="Phish Shield AI Simulation Engine")
templates = Jinja2Templates(directory="templates")

# --- In-Memory State ---
DEPARTMENTS = ["Finance", "HR", "Engineering", "Sales"]

EMPLOYEES = []
for i in range(1, 101):
    dept = random.choice(DEPARTMENTS)
    EMPLOYEES.append({
        "id": f"EMP{i:03d}",
        "name": f"User {i}",
        "department": dept,
        "risk_score": float(random.randint(10, 30)), # Start lower for better demo progression
        "compromised": False
    })

class SimulationState:
    def __init__(self):
        self.active_campaign = None
        self.telemetry_stream = []
        self.analytics = {
            "overall_resilience": 100.0,
            "total_sent": 0,
            "total_clicks": 0,
            "total_credentials": 0,
            "total_reported": 0,
            "department_risk": {dept: self.calculate_dept_risk(dept) for dept in DEPARTMENTS}
        }
        self.remediation_tasks = []

    def calculate_dept_risk(self, dept: str) -> float:
        dept_emps = [e for e in EMPLOYEES if e["department"] == dept]
        if not dept_emps: return 0.0
        return sum(e["risk_score"] for e in dept_emps) / len(dept_emps)

    def update_overall_resilience(self):
        avg_risk = sum(e["risk_score"] for e in EMPLOYEES) / len(EMPLOYEES)
        # Resilience is inverse of risk. If risk is 0, resilience is 100. If risk is 100, resilience is 0.
        self.analytics["overall_resilience"] = max(0.0, min(100.0, 100.0 - avg_risk))

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

class LaunchRequest(BaseModel):
    department: str
    psychological_vector: str

# --- Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/v1/campaigns/generate", response_model=AIGeneratedTemplate)
async def generate_campaign(req: CampaignGenRequest):
    templates_db = {
        "Fear": {
            "subject": f"URGENT: {req.department} Security Audit Failure",
            "body": f"Attention {req.department} Team,\n\nOur automated intrusion detection system has flagged multiple unauthorized access attempts originating from your department's subnet. To prevent immediate suspension of your corporate credentials, you must authenticate and review the audit logs.\n\nClick here to verify your identity."
        },
        "Greed": {
            "subject": f"CONFIDENTIAL: Q3 {req.department} Profit Sharing Payout",
            "body": f"Hello,\n\nThe executive board has approved an off-cycle profit-sharing distribution exclusively for the {req.department} division. To confirm your direct deposit details and claim your allocation before the end of the business day, please access the portal below.\n\nAccess Compensation Portal."
        },
        "Urgency": {
            "subject": f"ACTION REQUIRED: Mandatory {req.department} OS Patch",
            "body": f"All {req.department} personnel: A critical zero-day vulnerability affecting our internal network has been disclosed. You are required to install the attached emergency security patch immediately. Systems not patched within 1 hour will be forcibly disconnected from the VPN.\n\nDownload Patch Executable."
        },
        "Authority": {
            "subject": f"CEO DIRECTIVE: {req.department} Strategic Reorganization",
            "body": f"Team,\n\nPlease review the attached highly confidential brief regarding the upcoming structural reorganization within the {req.department} division. This document is restricted to internal personnel only and requires your immediate acknowledgment.\n\n- The Executive Team"
        }
    }
    
    selected = templates_db.get(req.psychological_vector, templates_db["Fear"])
    # Algorithmic sophistication scoring based on urgency level
    si_map = {"Low": 4, "Medium": 7, "Critical": 9}
    sophistication = si_map.get(req.urgency, 5)
    
    return AIGeneratedTemplate(
        subject_line=selected["subject"],
        body_content=selected["body"],
        sophistication_index=sophistication
    )

async def simulation_engine_loop(department: str, vector: str):
    targets = [e for e in EMPLOYEES if e["department"] == department] if department != "All" else EMPLOYEES
    state.analytics["total_sent"] += len(targets)
    
    for emp in targets:
        # 1. State Mutation: Delivered
        state.telemetry_stream.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "user": emp["name"],
            "dept": emp["department"],
            "action": "Delivered",
            "status": "info"
        })
        await asyncio.sleep(random.uniform(0.5, 1.2))
        
        chance = random.random()
        base_click_prob = 0.2 + (emp["risk_score"] / 200.0)
        
        if chance < base_click_prob:
            # 2. State Mutation: Clicked Link
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"],
                "dept": emp["department"],
                "action": "Clicked Link",
                "status": "warning"
            })
            state.analytics["total_clicks"] += 1
            # Behavioral Risk Scoring Algorithm: +45.0 for clicking
            emp["risk_score"] = min(100.0, emp["risk_score"] + 45.0)
            
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            if random.random() < 0.6:
                # 3. State Mutation: Credentials Entered
                state.telemetry_stream.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"],
                    "dept": emp["department"],
                    "action": "Credentials Entered",
                    "status": "danger"
                })
                state.analytics["total_credentials"] += 1
                # Behavioral Risk Scoring Algorithm: +55.0 for credentials
                emp["risk_score"] = min(100.0, emp["risk_score"] + 55.0)
                emp["compromised"] = True
                
                # Dynamic Remediation Router
                task_map = {
                    "Fear": "Defeating Intimidation Scams",
                    "Greed": "Identifying Too-Good-To-Be-True Lures",
                    "Urgency": "Defeating Urgency Tactics",
                    "Authority": "Verifying Executive Directives"
                }
                
                state.remediation_tasks.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "user": emp["name"],
                    "dept": emp["department"],
                    "module": task_map.get(vector, "General Phishing Awareness"),
                    "status": "Assigned"
                })
                
        elif chance > 0.7:
            # 4. State Mutation: Reported to Security
            state.telemetry_stream.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": emp["name"],
                "dept": emp["department"],
                "action": "Reported to Security",
                "status": "success"
            })
            state.analytics["total_reported"] += 1
            # Mitigation Reward: -30.0 for reporting
            emp["risk_score"] = max(0.0, emp["risk_score"] - 30.0)

        # Recalculate metrics
        state.analytics["department_risk"][emp["department"]] = state.calculate_dept_risk(emp["department"])
        state.update_overall_resilience()
        
        if len(state.telemetry_stream) > 100:
            state.telemetry_stream = state.telemetry_stream[:100]
        if len(state.remediation_tasks) > 50:
            state.remediation_tasks = state.remediation_tasks[:50]

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
