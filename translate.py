# Languages: German, Spanish, French, Italian,
# Korean, Dutch, Russian, English, Portuguese (Portugal),
# Portuguese (Brazilian), Spanish (Latin America), Chinese (Simplified),
# Chinese (Traditional), Czech, Ukrainian, Hindi, Icelandic, Japanese,
# Polish, Swedish, Hungarian, Romanian, Danish, Norwegian (Nynorsk),
# Norwegian (Bokmål), Finnish

languages = {"German", "Spanish", "French", "Italian", "Korean",
             "Dutch", "Russian", "English", "Portuguese (Portugal)", 
             "Portuguese (Brazilian)", "Spanish (Latin America)", 
             "Chinese (Simplified)", "Chinese (Traditional)", "Czech", 
             "Ukrainian", "Hindi", "Icelandic", "Japanese", "Polish", 
             "Swedish", "Hungarian", "Romanian", "Danish", "Norwegian (Nynorsk)", 
             "Norwegian (Bokmål)", "Finnish"}

from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

pipe = pipeline(
    "text-generation", 
    model="Unbabel/Tower-Plus-2B",
    device_map="auto")

@app.route("/translate", methods=["POST"])
def main():
    source_language = request.json["source_language"]
    target_language = request.json["target_language"]

    if source_language not in languages:
        return jsonify({"error": "Invalid source language"}), 400

    if target_language not in languages:
        return jsonify({"error": "Invalid target language"}), 400

    print(f"Translating {source_language} to {target_language}")

    source_content = request.json["source_content"]
        
    content_prompt = (
        f"Translate the following {source_language} source text to {target_language}:\n"
        f"{source_language}: {source_content}\n"
        f"{target_language}: "
    )

    messages = [{"role": "user", "content": content_prompt}]
    _ = pipe.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    outputs = pipe(messages, max_new_tokens=256, do_sample=False)
    content = outputs[0]["generated_text"][-1]["content"]

    return jsonify({"target_content": content}), 200
