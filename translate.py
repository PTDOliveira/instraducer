from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)

languages = {
    "German", "Spanish", "French", "Italian", "Korean", "Dutch", "Russian",
    "English", "Portuguese (Portugal)", "Portuguese (Brazilian)",
    "Spanish (Latin America)", "Chinese (Simplified)",
    "Chinese (Traditional)", "Czech", "Ukrainian", "Hindi", "Icelandic",
    "Japanese", "Polish", "Swedish", "Hungarian", "Romanian", "Danish",
    "Norwegian (Nynorsk)", "Norwegian (Bokmål)", "Finnish"
}

print("🔄 Loading model… this can take a while!")

pipe = pipeline(
    "text-generation",
    model="Unbabel/Tower-Plus-2B",
    device_map="auto"
)

@app.route("/translate", methods=["POST"])
def main():
    data = request.json

    source_language = data.get("source_language")
    target_language = data.get("target_language")
    source_content = data.get("source_content")

    if source_language not in languages:
        return jsonify({"error": "Invalid source language"}), 400

    if target_language not in languages:
        return jsonify({"error": "Invalid target language"}), 400

    prompt = (
        f"Translate the following {source_language} text to {target_language}:\n"
        f"{source_language}: {source_content}\n"
        f"{target_language}: "
    )

    messages = [{"role": "user", "content": prompt}]
    outputs = pipe(messages, max_new_tokens=256, do_sample=False)
    translated_text = outputs[0]["generated_text"][-1]["content"]

    return jsonify({"target_content": translated_text}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
