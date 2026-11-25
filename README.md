# LinguaViva

**LinguaViva** is a Flask web application and REST API for translating **Cebuano** and **Filipino** into **Kagan (Kalagan)** and **Manobo**. It runs on Meta AI's `NLLB-200-Distilled-600M` model fine-tuned with a LoRA adapter (`nllb_final_best_model`).

## Supported Translation Directions

* `ceb_2kll` — Cebuano $\rightarrow$ Kagan (Kalagan)
* `tl_2kll` — Filipino $\rightarrow$ Kagan (Kalagan)
* `ceb_2mno` — Cebuano $\rightarrow$ Manobo
* `tl_2mno` — Filipino $\rightarrow$ Manobo

## Project Structure

```text
LinguaViva/
├── app.py                  # Flask server & translation API
├── nllb_final_best_model/  # LoRA adapter weights & tokenizer
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

2. **Set the base model in `app.py`:**
   Use Hugging Face Hub (recommended) or point to your local folder:
   ```python
   base_model_id = "facebook/nllb-200-distilled-600M"
   ```

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