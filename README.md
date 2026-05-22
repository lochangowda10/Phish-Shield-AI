# Phish Shield AI

**Phish Shield AI** is an Adaptive AI Cyber Defense & Human Risk Analytics Platform. It is built as a complete, fully operational prototype designed for cybersecurity hackathon demonstrations (e.g., Track 4: AI-Driven Phishing Attack Simulation and Cyber Awareness Training Platform).

## Overview

This platform simulates an enterprise phishing attack and awareness training environment without needing to send real emails. It features a complete frontend Security Operations Center (SOC) dashboard and a deterministic backend simulation engine. 

### Core Features

1. **Workspace Command Center**: A dark-mode, elite SOC-style dashboard built with Tailwind CSS and dynamic Chart.js animations.
2. **Configuration Matrix**: Allows administrators to set a Target Department, Psychological Vector (Fear, Greed, Urgency, Authority), and Urgency Level.
3. **Heuristic Engine Output**: Simulates an LLM to dynamically generate highly contextual phishing payloads and assigns a "Sophistication Index" (SI) based on the inputs.
4. **Live Infiltration Telemetry Log**: Streams live simulated interaction state mutations for 100 seeded corporate employees across 4 departments as they interact with the simulated email:
   - `Delivered` -> `Clicked Link` -> `Credentials Entered` -> `Reported to Security`
5. **Human Risk Radar Dashboard**: Visualizes the organization's resilience, live click rates, and dynamic departmental risk scores.
6. **Remediation Hub Queue**: Automatically catches compromised employees (those who click or enter credentials) and dispatches targeted micro-learning training modules based on the specific psychological vector they failed against.

## Technical Architecture

* **Backend Engine**: Python `FastAPI` (single-file architecture in `main.py`).
  * Asynchronous simulation loop running in the background.
  * Deterministic risk scoring algorithm (e.g., +45 risk for clicking, -30 for reporting).
* **Frontend UI**: Standard HTML5 (`templates/index.html`), vanilla JavaScript for live 1-second polling, Tailwind CSS via CDN, and Chart.js.
* **State Management**: Built-in mock in-memory database seeded with 100 users. No external database setup is required to run the demo.

## Getting Started

### Prerequisites
* Python 3.8+
* `pip` package manager

### Installation & Execution

1. Clone the repository:
   ```bash
   git clone https://github.com/lochangowda10/Phish-Shield-AI.git
   cd Phish-Shield-AI
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Simulation Engine:
   ```bash
   python -m uvicorn main:app --reload
   ```

4. Open your web browser and navigate to:
   **http://localhost:8000**

## Running the Demo

1. Open the dashboard in your browser.
2. In the **Configuration Matrix** on the left, select a Target Department, Psychological Vector, and Urgency Level.
3. Click **"GENERATE AI PAYLOAD"** to see the system write a targeted phishing email.
4. Click **"EXECUTE SIMULATION"**.
5. Watch the **Live Infiltration Telemetry Log** on the right populate with employee actions.
6. Observe the **Human Risk Radar Dashboard** in the center dynamically adjust the company's risk profile based on employee behavior.
7. Note how compromised users are automatically assigned to the **Remediation Hub Queue** at the bottom.
