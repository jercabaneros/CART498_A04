from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    image_data = None
    dream_text = ""

    if request.method == "POST":
        dream_text = request.form.get("prompt", "")

        # ---- TEXT ANALYSIS ----
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Jungian psychoanalyst. Interpret the dream using "
                            "Jung’s theories: archetypes, shadow, anima/animus, symbols, "
                            "the collective unconscious, and individuation."
                        )
                    },
                    {"role": "user", "content": dream_text}
                ],
                max_output_tokens=300,
                temperature=0.9
            )

            # EXTRACT TEXT SAFELY
            analysis = response.output_text

        except Exception as e:
            analysis = f"Text analysis failed: {e}"

        # ---- IMAGE GENERATION ----
        try:
            img = client.images.generate(
                model="gpt-image-1",     # FIXED MODEL (valid)
                prompt=f"Surreal symbolic Jungian dream imagery: {dream_text}",
                size="256x256"           # Render-friendly
            )

            # Extract Base64
            image_base64 = img.data[0].b64_json
            image_data = f"data:image/png;base64,{image_base64}"

        except Exception as e:
            print("Image generation failed:", e)
            image_data = None

    return render_template(
        "index.html",
        result=analysis,
        image=image_data,
        dream_text=dream_text
    )


if __name__ == "__main__":
    app.run(debug=True)