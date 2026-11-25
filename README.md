# LinguaViva

**LinguaViva** is a Flask web application and REST API for translating **Cebuano** and **Filipino** into **Kagan (Kalagan)** and **Manobo**. It runs on Meta AI's `NLLB-200-Distilled-600M` model (`nllb-base-model`) fine-tuned with a LoRA adapter (`nllb_final_best_model`).

## Supported Translation Directions

* `ceb_2kll` — Cebuano $\rightarrow$ Kagan (Kalagan)
* `tl_2kll` — Filipino $\rightarrow$ Kagan (Kalagan)
* `ceb_2mno` — Cebuano $\rightarrow$ Manobo
* `tl_2mno` — Filipino $\rightarrow$ Manobo

## Project Structure

```text
LinguaViva/
├── app.py                  # Flask server & translation API
├── nllb-base-model/        # Local NLLB-200-Distilled-600M base model
├── nllb_final_best_model/  # Fine-tuned LoRA adapter weights & tokenizer
├── templates/              # HTML pages (index, translate, about)
└── static/                 # CSS & JS assets
```

## Quick Start

1. **Clone and set up environment:**

   ```bash
   git clone https://github.com/arvinlauron/LinguaViva.git
   cd LinguaViva
   python3 -m venv .venv
   source .venv/bin/activate
   pip install flask torch transformers peft sentencepiece accelerate
   ```

2. **Ensure model directories are in place:**
   * Place the base model in `./nllb-base-model` (or switch `base_model_id` in `app.py` to `"facebook/nllb-200-distilled-600M"` to download automatically from Hugging Face).
   * Place the fine-tuned LoRA adapter in `./nllb_final_best_model`.

3. **Run the server:**

   ```bash
   python app.py
   ```

   Open `http://localhost:8080` in your browser.

## API Usage

**`POST /translate`**

Request:

```json
{
  "text": "Masakiton ka.",
  "direction": "ceb_2kll"
}
```

Response:

```json
{
  "translation": "Masakiton kaw."
}
```

> **Note:** LinguaViva is an experimental translation tool and should not replace certified human translators for medical, legal, or official use.