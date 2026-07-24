# Unit 1 — AI/ML Lab Programs (Standalone Scripts)

Each `.py` file is a **complete, self-contained program**. Just run it directly:

```bash
python 07_sentiment_analysis_pipeline.py
```

## How each script works
1. Every script starts with an `ensure()` helper that checks if a required package
   (matplotlib, pandas, numpy, scikit-learn, torch, transformers) is installed.
   If it's missing, it auto-installs it via `pip install`.
2. Programs 7–20 use Hugging Face's `transformers` library. On first run, they
   automatically **download the pretrained model/tokenizer** from the
   Hugging Face Hub (needs internet). The download is cached locally
   (usually under `~/.cache/huggingface`), so every future run of that
   same program is fully offline and fast.
3. Programs 1–6 need no internet at all — only local computation.

## Programs and what they download from Hugging Face

| File | Downloads from Hugging Face | Size (approx) |
|---|---|---|
| 01–06 | None (local only) | — |
| 07 | distilbert-base-uncased-finetuned-sst-2-english | ~260 MB |
| 08 | bert-base-uncased tokenizer | few MB |
| 09 | gpt2 | ~500 MB |
| 10 | distilbert-base-uncased-finetuned-sst-2-english | ~260 MB |
| 11 | bert-base-uncased tokenizer | few MB |
| 12 | bert-base-uncased (full model) | ~440 MB |
| 13 | gpt2 | ~500 MB |
| 14 | distilbert-base-cased-distilled-squad | ~260 MB |
| 15 | bert-base-uncased tokenizer | few MB |
| 16 | bert-base-uncased + gpt2 tokenizers | few MB |
| 17 | bert-base-uncased (full model) | ~440 MB |
| 18 | bert-base-uncased (full model) | ~440 MB |
| 19 | gpt2 | ~500 MB |
| 20 | gpt2 | ~500 MB |

Models are shared across scripts — e.g. `bert-base-uncased` downloads once and
is reused by programs 8, 11, 12, 15, 16, 17, 18. Same for `gpt2` across
9, 13, 16, 19, 20. Total one-time download if you run everything: roughly 1.5–2 GB.

## Recommended run order
Run 1–6 first (instant, offline). Then run 7 or 9 first for the transformer
programs — this triggers the two biggest downloads (DistilBERT-SST2 and
GPT-2) that later scripts reuse from cache.

## Environment notes
- Works in plain Python 3.8+, Jupyter, Google Colab, or VS Code.
- On Termux/mobile: `torch` + `transformers` installs are heavy — Colab is
  easier for programs 6–20 specifically. Programs 1–5 run fine on Termux.
- GPU (if available): add `device=0` inside any `pipeline(...)` call to use CUDA.
