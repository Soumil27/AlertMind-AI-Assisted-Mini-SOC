import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from prompts import SYSTEM_PROMPT

load_dotenv()

# -----------------------------
# Load Wazuh JSON Alert
# -----------------------------
with open("alerts/powershell.json", "r") as file:
    alert = json.load(file)

# Wazuh stores the alert inside "_source"
source = alert["_source"]

# -----------------------------
# Extract fields
# -----------------------------
rule = source["rule"]
agent = source["agent"]

rule_id = rule["id"]
description = rule["description"]

mitre = rule["mitre"]

mitre_id = ", ".join(mitre["id"])
mitre_technique = ", ".join(mitre["technique"])
mitre_tactic = ", ".join(mitre["tactic"])

timestamp = source["timestamp"]
agent_name = agent["name"]

# Optional process details
event = source["data"]["win"]["eventdata"]

command = event.get("commandLine", "N/A")
parent_process = event.get("parentImage", "N/A")
user = event.get("user", "N/A")

# -----------------------------
# Build alert for LLM
# -----------------------------
user_alert = f"""
Rule ID: {rule_id}

Description:
{description}

Agent:
{agent_name}

Timestamp:
{timestamp}

MITRE ID:
{mitre_id}

MITRE Technique:
{mitre_technique}

MITRE Tactic:
{mitre_tactic}

Executed Command:
{command}

Parent Process:
{parent_process}

User:
{user}
"""

# -----------------------------
# LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

response = llm.invoke([
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=user_alert)
])

print("\n==========================================")
print("      AlertMind AI Assistant")
print("==========================================\n")

print(response.content)
