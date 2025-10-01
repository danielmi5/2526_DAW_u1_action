import subprocess, datetime


def run_tests():
    try:
        subprocess.check_call(["pytest", "-q"])
        return "✅ Tests correctos"
    except subprocess.CalledProcessError:
        return "❌ Tests fallidos"

def update_readme(status: str):
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == "<!-- Historial de los tests -->":
            new_lines.pop()
            time = datetime.datetime.now()
            new_lines.append(f"- {status}| {time.strftime('%d/%m/%Y')} - {time.strftime('%H:%M')}\n<!-- Historial de los tests -->\n")


    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    status = run_tests()
    update_readme(status)
