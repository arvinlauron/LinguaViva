from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

app = Flask(__name__)

# ==========================================
# 1. LOAD MODEL & TOKENIZER
# ==========================================
#base_model_id = "facebook/nllb-200-distilled-600M"
base_model_id = "./nllb-base-model"
adapter_path = "./nllb_final_best_model"

print("Loading Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(adapter_path)

print("Loading Base Model and LoRA Adapter (This may take a moment)...")
base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_id)
model = PeftModel.from_pretrained(base_model, adapter_path)

# Move to GPU if available
# Move to GPU if available
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

model.to(device)
model.eval()
print(f"Model successfully loaded on {device.upper()}!")

# ==========================================
# 2. APP ROUTES (PAGES)
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate_page")
def translate_page():
    return render_template("translate.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ==========================================
# 3. TRANSLATION API
# ==========================================
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    direction = data.get("direction", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    prompts = {
        "ceb_2kll": "Translate Cebuano to Kagan: ",
        "tl_2kll": "Translate Filipino to Kagan: ",
        "ceb_2mno": "Translate Cebuano to Manobo: ",
        "tl_2mno": "Translate Filipino to Manobo: "
    }
    
    prompt_text = prompts.get(direction, "") + text

    if direction in ["ceb_2kll", "ceb_2mno"]:
        tokenizer.src_lang = "ceb_Latn"
    else:
        tokenizer.src_lang = "tgl_Latn"

    forced_bos_token_id = tokenizer.convert_tokens_to_ids("ceb_Latn")

    inputs = tokenizer(prompt_text, return_tensors="pt", max_length=256, truncation=True).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=256,
            num_beams=8,
            length_penalty=1.0,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return jsonify({"translation": translated_text})

import os

if __name__ == '__main__':
    # Get port from environment variable, default to 8080 if not set
    port = int(os.environ.get("PORT", 8080))
    # Bind to 0.0.0.0 so it is publicly accessible inside the container
    app.run(host="0.0.0.0", port=port)