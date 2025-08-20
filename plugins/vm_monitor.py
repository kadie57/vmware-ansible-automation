#!/usr/bin/env python3

import time
import re
import requests

LOG_FILE = "/var/log/vcenter803.log"
WEBHOOK_URL = "http://localhost:5000/events"

# Regex để bắt đường dẫn file .vmx và trích tên máy ảo
VM_NAME_REGEX = re.compile(r"Created VM.*?([\w\-/]+\.vmx)")

def extract_vm_name(line):
    match = VM_NAME_REGEX.search(line)
    if match:
        # Trích tên máy ảo từ đường dẫn file .vmx
        vmx_path = match.group(1)
        vm_name = vmx_path.split("/")[-1].replace(".vmx", "")
        return vm_name
    return None

def send_webhook(vm_name):
    data = {
	"event": "VM_CREATED",
	"details": {
		"vm_name": vm_name
	}
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"✅ Đã gửi webhook: {data}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi gửi webhook: {e}")

def monitor_log():
    print(f"🔍 Đang theo dõi {LOG_FILE}...")
    with open(LOG_FILE, "r") as f:
        # Nhảy tới cuối file
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if "Created VM" in line:
                vm_name = extract_vm_name(line)
                if vm_name:
                    send_webhook(vm_name)
                else:
                    print(f"⚠️ Không trích xuất được tên máy ảo từ dòng: {line.strip()}")

if __name__ == "__main__":
    monitor_log()
