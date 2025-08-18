# src/logger.py
import os
from datetime import datetime

base_path = "logs"
if not os.path.exists(base_path):
    os.makedirs(base_path)

log_file = os.path.join(base_path, "log.md")
log_title_format = "# %Y-%m-%d"


def ensure_date_header():
    today = datetime.now().strftime(log_title_format)
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(today + "\n\n")
    else:
        with open(log_file, "r+", encoding="utf-8") as f:
            content = f.read()
            if today not in content:
                f.write("\n" + today + "\n\n")


def append_log(lines):
    from datetime import datetime

    ensure_date_header()
    md_text = "\n".join(f"- {line.strip()}" for line in lines if line.strip())
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"**{datetime.now():%I:%M %p}**\n{md_text}\n\n")
