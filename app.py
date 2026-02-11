from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    image_data = None

    if request.method == "POST":
        dream_text = request.form.get("prompt", "")

        # ---- TEXT ANALYSIS ----
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "developer",
                        "content": (
                            "You are a Jungian psychoanalyst. Interpret the dream using "
                            "Jung’s theories: archetypes, shadow, anima/animus, symbols, "
                            "collective unconscious, and individuation."
                        )
                    },
                    {"role": "user", "content": dream_text}
                ],
                temperature=1.0,
                max_output_tokens=300
            )

            if response.output:
                analysis = response.output[0].content[0].text

        except Exception as e:
            analysis = f"Text analysis failed: {e}"

        # ---- IMAGE GENERATION ----
        try:
            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=f"Dream visualization, surreal, symbolic, Jungian imagery: {dream_text}",
                size="256x256"
            )
            image_data = "data:image/png;base64," + img.data[0].b64_json
        except Exception:
            image_data = None  # skip image if generation fails

    return render_template("index.html", result=analysis, image=image_data)


if __name__ == "__main__":
    app.run(debug=True)