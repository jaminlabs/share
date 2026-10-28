# Before you buy a $3,499 AI box, check the PC you already own (Oct 24, 2026)

Ghost raised an $11M seed round led by Andreessen Horowitz to sell **Core**, a $3,499 "personal AI computer" that runs
models on the box itself ([TechCrunch, Oct 5, 2026](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/),
[ghost.ai](https://ghost.ai)). Its spec sheet looks a lot like a gaming PC with a 24 GB NVIDIA card. Mine is one.

Takes 1 minute: run [`spec_check.py`](spec_check.py) and see where your PC lands next to Core's published spec.

```sh
python3 spec_check.py
```

No install, no internet, nothing is sent anywhere. It reads `nvidia-smi`, RAM, CPU threads and disk size.

## My result (Oct 24, 2026)

| | Ghost Core (ghost.ai) | My Linux PC |
|---|---|---|
| GPU | NVIDIA RTX PRO 4000 Blackwell SFF | NVIDIA GeForce RTX 3090 Ti |
| VRAM | 24 GB GDDR7 ECC | 24 GB GDDR6X |
| Memory bandwidth | 432 GB/s | 1008 GB/s |
| GPU power | 70 W | 450 W |
| CPU | Ryzen 5 9600X (6 cores) | Ryzen 9 3900X (12 cores) |
| RAM / disk | 64 GB DDR5 / 1 TB | 64 GB / 2 TB |
| Models | Qwen 3.8-Next, Qwen 3.8-27B, Gemma 4-31B, Muse-Glimmer-30B | Qwen3.8-27B (4-bit), ran Oct 12 |

Where Core wins, honestly: a 70 W card is far quieter and cheaper to run 24/7 than my 450 W one (my 3090 Ti ran at
448 W and the fans got loud enough that I switched the local model off). Ghost also says Core comes with "its own
software layer, browser, and filing system", always-on memory and an agent firewall. I haven't used one; Batch 1 is
scheduled to ship Oct 31.

Where my old PC wins: same 24 GB of VRAM, more than twice the memory bandwidth (memory bandwidth is what mostly sets tokens per
second for a local model), and it was already on my desk.

## How I ran Qwen 27B on it (Oct 12, 2026)

I used vLLM, which gives you an OpenAI-compatible endpoint on your own machine (Ghost says Core offers an endpoint
compatible with the OpenAI Responses API, the same idea):

```sh
# Linux, NVIDIA driver installed
uv venv && uv pip install vllm
hf download <a Qwen3.8-27B AWQ 4-bit repo> --local-dir models/Qwen3.8-27B-AWQ-INT4
export VLLM_USE_FLASHINFER_SAMPLER=0   # my PC has no CUDA compiler for FlashInfer's sampler
vllm serve models/Qwen3.8-27B-AWQ-INT4 --served-model-name qwen38-27b \
  --host 127.0.0.1 --port 8000 --max-model-len 8192 --gpu-memory-utilization 0.90
# then point any OpenAI-compatible app at http://127.0.0.1:8000/v1
```

Ollama (https://ollama.com) is the popular one-command route; I did not use it here.

## What the founder says

"You can run models on existing hardware, but it's a terrible experience on many levels." — Zain Javaid, Ghost CEO,
to TechCrunch. The hardware part is a spec sheet you can compare yourself. The experience part is the software, and
that's what the $3,499 is really for. You decide.

Sources: [TechCrunch](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) ·
[ghost.ai](https://ghost.ai) and [ghost.ai/support](https://ghost.ai/support) (read Oct 24, 2026) ·
[NVIDIA RTX PRO 4000 Blackwell SFF](https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-4000-sff/) ·
[NVIDIA Ada whitepaper (RTX 3090 Ti: 1008 GB/s)](https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf)
