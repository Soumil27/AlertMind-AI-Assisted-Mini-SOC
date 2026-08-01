import sys
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from prompts import SYSTEM_PROMPT
from guardrails import sanitize_alert, log_prompt, log_response, DISCLAIMER

load_dotenv()

# Check command-line argument
if len(sys.argv) != 2:
    print("Usage: python app.py <alert_json_file>")
    sys.exit(1)

alert_file = sys.argv[1]

# Load alert JSON
with open(alert_file, "r") as file:
    alert = json.load(file)
alert = sanitize_alert(alert)

source = alert["_source"]

rule = source["rule"]
agent = source["agent"]

event = source["data"]["win"]["eventdata"]

user_alert = f"""
Rule ID: {rule['id']}
Description: {rule['description']}
Agent: {agent['name']}
Timestamp: {source['timestamp']}
MITRE ID: {', '.join(rule['mitre']['id'])}
MITRE Technique: {', '.join(rule['mitre']['technique'])}
MITRE Tactic: {', '.join(rule['mitre']['tactic'])}
Command: {event.get('commandLine', 'N/A')}
Parent Process: {event.get('parentImage', 'N/A')}
User: {event.get('user', 'N/A')}
"""

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)
log_prompt(f"Alert File: {alert_file}\n\n{user_alert}")

response = llm.invoke([
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=user_alert)
])
log_response(response.content)

print("\n==========================================")
print("      AlertMind AI Assistant")
print("==========================================\n")

print(response.content)
print(DISCLAIMER)
