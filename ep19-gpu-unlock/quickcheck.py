"""Is my RTX 30 card's BF16 tensor rate unlocked right now? About 10 seconds.

Runs 8192^3 BF16 matrix multiplies (FP32 accumulation) and divides TFLOPS by the SM clock, which cancels out
power-limit throttling. On an RTX 3090 Ti: about 0.042 TFLOPS per MHz locked, about 0.082 unlocked.
Other GA102/GA104 cards have fewer tensor cores, so compare against your own "before" number.

Needs: PyTorch with CUDA, nvidia-smi on PATH.   Usage: python quickcheck.py [gpu index]
"""
import statistics
import subprocess
import sys
import time

import torch

gpu = int(sys.argv[1]) if len(sys.argv) > 1 else 0
torch.cuda.set_device(gpu)
torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
n, iters = 8192, 40
a = torch.randn(n, n, device="cuda", dtype=torch.bfloat16)
b = torch.randn(n, n, device="cuda", dtype=torch.bfloat16)
c = torch.empty_like(a)

deadline = time.monotonic() + 3  # warm up so the clock settles
while time.monotonic() < deadline:
    torch.matmul(a, b, out=c)
    torch.cuda.synchronize()

rates, clocks = [], []
for _ in range(3):
    start, end = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
    start.record()
    for _ in range(iters):
        torch.matmul(a, b, out=c)
    end.record()
    clock = subprocess.run(["nvidia-smi", "-i", str(gpu), "--query-gpu=clocks.sm", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True).stdout.strip()
    end.synchronize()
    rates.append(2 * n ** 3 * iters / (start.elapsed_time(end) / 1000) / 1e12)
    clocks.append(float(clock))

tflops, mhz = statistics.median(rates), statistics.median(clocks)
print(f"{torch.cuda.get_device_name(gpu)}: BF16 {tflops:.1f} TFLOPS at {mhz:.0f} MHz = {tflops / mhz:.4f} TFLOPS per MHz")
print("RTX 3090 Ti reference: ~0.042 locked, ~0.082 unlocked. Other cards: compare before vs after on your own card.")
