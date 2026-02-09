from flask import Flask, render_template, request
import os
import base64
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
        dream_text = request.form["prompt"]

        try:
            # ---- TEXT ANALYSIS (Jungian) ----
            response = client.responses.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "developer",
                        "content": (
                            "You are a Jungian psychoanalyst. "
                            "Interpret the dream according to Jung’s symbols, archetypes, "
                            "shadow, anima/animus, and individuation. "
                            "Explain the meaning clearly and helpfully."
                        )
                    },
                    {"role": "user", "content": dream_text}
                ],
                temperature=1.1,
                max_output_tokens=700
            )

            analysis = response.output[0].content[0].text

            # ---- IMAGE GENERATION ----
            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=f"Dream visualization, surreal, symbolic, Jungian imagery: {dream_text}",
                n=1,
                size="256x256"
            )

            image_bytes = base64.b64decode(img.data[0].b64_json)
            image_data = "data:image/png;base64," + img.data[0].b64_json

        except Exception as e:
            analysis = f"Error occurred: {e}"

    return render_template("index.html", result=analysis, image=image_data)


if __name__ == "__main__":
    app.run(debug=True)