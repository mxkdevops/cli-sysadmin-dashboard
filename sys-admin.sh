#!/bin/bash

LOG_DIR="$HOME/sysadmin_logs"
mkdir -p "$LOG_DIR"
TODAY_LOG="$LOG_DIR/$(date +%F).log"

declare -A TASKS
TASKS=(
  ["Check Uptime"]="uptime"
  ["Disk Usage"]="df -h"
  ["Memory Usage"]="free -m"
  ["Top 5 CPU Processes"]="ps aux --sort=-%cpu | head -n 6"
  ["Check Open Ports"]="ss -tuln"
  ["Failed SSH Logins"]="grep 'Failed password' /var/log/auth.log | tail -n 5"
  ["Firewall Status"]="sudo ufw status"
  ["Running Services"]="systemctl list-units --type=service --state=running"
  ["Pending Updates"]="apt list --upgradable"
  ["System Logs"]="tail -n 10 /var/log/syslog"
)

# Create an indexed array of task names for easier selection
TASK_NAMES=("${!TASKS[@]}")

function show_menu() {
  echo -e "\n🧰 SYSTEM ADMIN DASHBOARD - $(date)\n"
  for i in "${!TASK_NAMES[@]}"; do
    echo "[$((i+1))] ${TASK_NAMES[$i]}"
  done
  echo "[0] Exit"
}

function run_task() {
  local task_name="$1"
  echo -e "\n🔹 Running: $task_name"
  echo "=== $task_name ===" >> "$TODAY_LOG"
  eval "${TASKS[$task_name]}" | tee -a "$TODAY_LOG"
  echo "======================" >> "$TODAY_LOG"
}

while true; do
  show_menu
  echo -n $'\nChoose a task number to run: '
  read choice
  if [[ "$choice" == "0" ]]; then
    echo "👋 Exiting..."
    break
  elif [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#TASK_NAMES[@]} )); then
    task_name="${TASK_NAMES[$((choice-1))]}"
    run_task "$task_name"
  else
    echo "❌ Invalid choice."
  fi
done
