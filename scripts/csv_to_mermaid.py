import csv
from datetime import datetime

CSV_PATH = "tasks.csv"
README_PATH = "README.md"
START_MARK = "<!-- GANTT:START -->"
END_MARK = "<!-- GANTT:END -->"

def ddays(start, end):
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    return f"{(e - s).days}d"

def status_token(status):
    status = (status or "").strip().lower()
    if status in ("done", "active", "crit"):
        return status + ", "
    return ""

def gen_mermaid(rows):
    lines = [
        "```mermaid",
        "gantt",
        "    title Roadmap Proyecto",
        "    dateFormat  YYYY-MM-DD",
        "    axisFormat  %d-%m",
        ""
    ]
    current_section = None
    ids = {}
    for i, r in enumerate(rows, start=1):
        ids[r["name"]] = f"id{i}"

    for r in rows:
        section = r["section"]
        if section != current_section:
            lines.append(f"    section {section}")
            current_section = section
        name = r["name"]
        start = r["start"]
        end = r["end"]
        depends = r.get("depends", "").strip()
        status = status_token(r.get("status"))
        task_id = ids[name]
        if depends:
            dep_id = ids.get(depends, "")
            line = f"    {name:<24} : {status}{task_id}, after {dep_id}, {ddays(start, end)}"
        else:
            line = f"    {name:<24} : {status}{task_id}, {start}, {ddays(start, end)}"
        lines.append(line)
    lines.append("```")
    return "\n".join(lines)

def replace_in_readme(gantt_text):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()
    start_i = readme.find(START_MARK)
    end_i = readme.find(END_MARK)
    if start_i == -1 or end_i == -1 or end_i < start_i:
        raise RuntimeError("No se encontraron los marcadores GANTT en README.md")
    new = readme[:start_i + len(START_MARK)] + "\n\n" + gantt_text + "\n\n" + readme[end_i:]
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new)

def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    gantt = gen_mermaid(rows)
    replace_in_readme(gantt)

if __name__ == "__main__":
    main()

"Agregar script CSV→Mermaid"
