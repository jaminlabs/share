#!/usr/bin/env python3
"""Does the PC you already own match a $3,499 "personal AI computer"? (jamin labs EP20, Oct 24, 2026)

    python3 spec_check.py

Reads your NVIDIA GPU (nvidia-smi), RAM, CPU threads and free disk, and prints them next to the spec Ghost publishes
for its Core box (ghost.ai, read Oct 24, 2026). No install, no internet, nothing is sent anywhere. Linux or Windows
with an NVIDIA driver; on a Mac there is no nvidia-smi, so only RAM/CPU/disk are shown.
"""
import os
import shutil
import subprocess

CORE = {  # ghost.ai spec callouts, read 2026-10-24
    "GPU": "NVIDIA RTX PRO 4000 Blackwell SFF Edition",
    "VRAM (GB)": 24,
    "GPU power (W)": 70,  # NVIDIA product page: max power consumption 70 W
    "RAM (GB)": 64,
    "CPU threads": 12,  # AMD Ryzen 5 9600X, 6 cores / 12 threads
    "Disk (TB)": 1,
}


def gpu():
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    out = subprocess.run([exe, "--query-gpu=name,memory.total,power.limit", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True).stdout.strip().splitlines()
    if not out:
        return None
    name, mem, power = [x.strip() for x in out[0].split(",")]
    return {"GPU": name, "VRAM (GB)": round(float(mem) / 1024), "GPU power (W)": round(float(power))}


def ram_gb():
    try:
        with open("/proc/meminfo") as f:
            kb = int(next(line for line in f if line.startswith("MemTotal")).split()[1])
        return round(kb / 1024 / 1024)
    except (OSError, StopIteration, ValueError):
        return None


def main():
    mine = gpu() or {"GPU": "no NVIDIA GPU found"}
    mine["RAM (GB)"] = ram_gb()
    mine["CPU threads"] = os.cpu_count()
    mine["Disk (TB)"] = round(shutil.disk_usage(os.path.expanduser("~")).total / 1e12, 1)
    print(f"{'':16}{'Ghost Core':>44}{'your PC':>44}")
    for k, v in CORE.items():
        print(f"{k:16}{str(v):>44}{str(mine.get(k, '?')):>44}")
    vram = mine.get("VRAM (GB)") or 0
    print()
    if vram >= 24:
        print("24 GB of VRAM or more: a 27B model in 4-bit fits on your card (mine ran Qwen3.8-27B AWQ 4-bit on 24 GB).")
    elif vram >= 16:
        print("16-23 GB of VRAM: a 27B model in 4-bit is usually too tight; look at smaller models first.")
    else:
        print("Under 16 GB of VRAM: small models only, or a hosted API.")


if __name__ == "__main__":
    main()
