# Is your RTX 30 card running tensor math at half rate? (Oct 23, 2026)

GeForce RTX 30 cards run FP16/BF16 tensor math with FP32 accumulate at half the rate of NVIDIA's pro cards on the same
chip. The open-source Linux kernel module [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) lifts that limit
on GA102 and GA104 cards (RTX 3090, 3090 Ti, 3080, 3080 Ti, 3070, 3070 Ti, 3060 Ti).

**Linux only.** It is a kernel module that runs before the NVIDIA driver loads. Nothing here works on Windows or macOS.

## 1. Check your card in 10 seconds (no install)

You need Python with PyTorch (CUDA build) and `nvidia-smi`. Run [`quickcheck.py`](quickcheck.py):

```sh
python quickcheck.py
```

It runs BF16 matrix multiplies and divides TFLOPS by the GPU clock, so power-limit throttling cancels out:

| Result | Meaning |
|---|---|
| about 0.042 TFLOPS per MHz | locked (half rate), the normal GeForce state |
| about 0.082 TFLOPS per MHz | unlocked |

The 0.042 / 0.082 values were measured on an RTX 3090 Ti. On a 3080 or 3070 the per-MHz number is lower (fewer tensor
cores), but unlocking roughly doubles it the same way.

## 2. My numbers (RTX 3090 Ti, 450 W limit, driver 615.78.08, Oct 23, 2026)

| | Before | After | |
|---|---:|---:|---:|
| BF16 matmul (8192³, TFLOPS) | 81.2 | 124.7 | 1.54× |
| FP16 matmul (TFLOPS) | 78.8 | 114.4 | 1.45× |
| TF32 matmul (TFLOPS) | 40.8 | 70.7 | 1.73× |
| FP32 matmul (TFLOPS) | 27.5 | 27.7 | no change |
| BF16 per clock (TFLOPS per MHz) | 0.042 | 0.082 | 1.95× |
| ComfyUI, Qwen-Image 1024², 20 steps (s per image) | 27.6 | 19.6 | 1.41× |

Per clock it is about 2×. In absolute speed the card stays inside the same 450 W power limit, so the clock drops when
the tensor cores work harder. That's why the real gains were 1.4–1.7×, not 2×. The ComfyUI images came out
pixel-identical before and after.

## 3. Install (read the repo first)

Follow the [repo README](https://github.com/Zagitta/gpu-unlock): `make install`, then add `gpu_unlock.targets=all` to
your kernel command line the way your bootloader expects, then **fully power off** and turn the PC back on (a plain
reboot may not reset the card). After boot, check:

```sh
journalctl -k -b | grep gpu_unlock     # expect: gpu_unlock: unlocked
python quickcheck.py                    # expect: about 2x the TFLOPS per MHz
```

How I did it: I gave Claude Code the repo link and these rules, and it did everything except the one step that needed
my password:

- Read the README and the open issues first.
- Log every command and result to a file.
- Show me any `sudo` command before running it.
- Stop and report if something is unexpected (unsupported card, build failure, missing kernel option). Don't work around it.
- Never reboot, shut down or touch BIOS settings. I do the final power-off myself.
- Never edit generated boot files (on Limine: change `/etc/default/limine` and run `limine-update`, not `limine.conf`).
- Measure a baseline before installing so you can compare.

Things to know before you do this:

- Take a filesystem snapshot first, or know how to boot without the kernel option.
- One user's Limine system stopped booting after an AI edited its boot config (repo issue #7). Don't let anything edit
  generated boot files.
- After suspend/resume the unlock may be gone. Check with `quickcheck.py`, and fully power off and on if it is.
- The module adds an out-of-tree kernel taint. The repo was about a month old when I installed it.

Sources: [gpu-unlock README and issues](https://github.com/Zagitta/gpu-unlock) (commit 258f38a); NVIDIA Ampere GA102
whitepaper v2.1, Table 9 (RTX 3090: 71 TFLOPS FP16/BF16 tensor with FP32 accumulate vs 142 with FP16 accumulate) and
Table 3 (RTX A6000, same chip: 154.8 for both).
