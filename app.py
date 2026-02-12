from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import io

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store image in memory
generated_image_bytes = None

JUNG_PROMPT = """
You are a Jungian dream analyst.
Interpret dreams using Carl Jung's psychological theories.
Focus on archetypes, shadow, symbols, and individuation.
Write clearly and meaningfully.
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global generated_image_bytes

    analysis = None
    dream_text = None
    image_ready = False

    if request.method == "POST":
        dream_text = request.form.get("prompt", "")

        # ---- TEXT ANALYSIS ----
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "system", "content": JUNG_PROMPT},
                    {"role": "user", "content": dream_text}
                ],
                temperature=0.9,
                max_output_tokens=300
            )

            analysis = response.output_text

        except Exception as e:
            analysis = f"Text analysis failed: {e}"

        # ---- IMAGE GENERATION ----
        try:
            image_response = client.images.generate(
                model="gpt-image-1-mini",
                prompt=f"Surreal symbolic Jungian dream visualization: {dream_text}",
                size="256x256"
            )

            b64 = image_response.data[0].b64_json
            generated_image_bytes = base64.b64decode(b64)
            image_ready = True

        except Exception:
            image_ready = False

    return render_template(
        "index.html",
        result=analysis,
        dream_text=dream_text,
        image_ready=image_ready
    )

@app.route("/image")
def image():
    global generated_image_bytes

    if generated_image_bytes is None:
        return "No image available", 404

    return send_file(
        io.BytesIO(generated_image_bytes),
        mimetype="image/png"
    )

if __name__ == "__main__":
    app.run(debug=True)