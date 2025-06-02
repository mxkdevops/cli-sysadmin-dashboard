import subprocess
import datetime
import os

# Define tasks and associated shell commands
tasks = {
    "Check CPU Usage": "top -bn1 | grep 'Cpu(s)'",
    "Check Uptime": "uptime",
    "Check Disk Usage": "df -h /",
    "Check SSH Status": "systemctl is-active ssh",
    "Check UFW Firewall": "sudo ufw status",
    "Check Users Logged In": "who"
}

task_status = {task: "Pending" for task in tasks}
task_output = {}

# Helper: Run a shell command and return result
def run_command(task, cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        task_status[task] = "✔️"
        task_output[task] = output.strip()
        return output.strip()
    except subprocess.CalledProcessError as e:
        task_status[task] = "❌"
        task_output[task] = e.output.strip()
        return e.output.strip()

# Menu UI
def show_menu():
    os.system("clear" if os.name == "posix" else "cls")
    print("🛠️  SysAdmin Daily Terminal Dashboard")
    print("=" * 40)
    for i, task in enumerate(tasks.keys(), start=1):
        status = task_status[task]
        print(f"{i}. {task} [{status}]")
    print(f"{len(tasks)+1}. Run ALL Tasks")
    print(f"{len(tasks)+2}. Export Daily Report")
    print(f"{len(tasks)+3}. Exit")
    print("=" * 40)

def export_report():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_report_{date_str}.txt"
    with open(filename, "w") as f:
        f.write(f"SysAdmin Report - {date_str}\n")
        f.write("=" * 50 + "\n\n")
        for task, output in task_output.items():
            f.write(f"{task} [{task_status[task]}]\n")
            f.write(output + "\n\n")
    print(f"\n✅ Report exported to {filename}")
    input("Press Enter to continue...")

def run_all_tasks():
    for task, cmd in tasks.items():
        print(f"\n🔄 Running: {task}")
        output = run_command(task, cmd)
        print(output)
    input("\n✅ All tasks completed. Press Enter to continue...")

def run_dashboard():
    while True:
        show_menu()
        try:
            choice = int(input("Select a task number: "))
            if 1 <= choice <= len(tasks):
                task = list(tasks.keys())[choice - 1]
                print(f"\n🔄 Running: {task}")
                output = run_command(task, tasks[task])
                print(output)
                input("\nPress Enter to continue...")
            elif choice == len(tasks) + 1:
                run_all_tasks()
            elif choice == len(tasks) + 2:
                export_report()
            elif choice == len(tasks) + 3:
                print("👋 Exiting dashboard. Goodbye!")
                break
            else:
                print("❌ Invalid option.")
        except ValueError:
            print("❌ Please enter a valid number.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    run_dashboard()
