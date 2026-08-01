import re
import json
from datetime import datetime

# -------------------------
# Secret masking
# -------------------------

def sanitize_alert(alert_json):
    text = json.dumps(alert_json)

    # Mask passwords
    text = re.sub(
        r'(?i)(password|passwd|secret)\s*[:=]\s*"?[^",}]+',
        r'\1: **',
        text
    )

    # Mask API keys
    text = re.sub(
        r'(?i)(api[_-]?key)\s*[:=]\s*"?[^",}]+',
        r'\1: **',
        text
    )

    # Mask tokens
    text = re.sub(
        r'(?i)(token)\s*[:=]\s*"?[^",}]+',
        r'\1: **',
        text
    )

    return json.loads(text)


# -------------------------
# Prompt logging
# -------------------------

def log_prompt(prompt):

    with open("logs/prompts.log", "a") as f:

        f.write("\n=============================\n")
        f.write(str(datetime.now()))
        f.write("\n")
        f.write(prompt)
        f.write("\n")


# -------------------------
# Response logging
# -------------------------

def log_response(response):

    with open("logs/responses.log", "a") as f:

        f.write("\n=============================\n")
        f.write(str(datetime.now()))
        f.write("\n")
        f.write(response)
        f.write("\n")


# -------------------------
# Human Review Banner
# -------------------------

DISCLAIMER = """

==================================================

This AI-generated analysis is advisory only.

No automated actions have been performed.

All recommendations must be reviewed and approved by a human SOC analyst before implementation.

==================================================

"""
