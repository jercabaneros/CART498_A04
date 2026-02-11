from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store last image filename globally (simple + safe for free tier)
LAST_IMAGE_PATH = "static/generated.png"

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    image_url = None

    if request.method == "POST":
        dream_text = request.form["prompt"]

        try:
            # ---- TEXT ANALYSIS ----
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
                temperature=1.1,
                max_output_tokens=700
            )

            analysis = response.output[0].content[0].text

            # ---- IMAGE GENERATION ----
            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=f"Dream visualization: {dream_text}",
                size="auto"
            )

            # Decode base64 → write to a file instead of keeping in RAM
            img_bytes = base64.b64decode(img.data[0].b64_json)

            # Ensure static folder exists
            os.makedirs("static", exist_ok=True)

            with open(LAST_IMAGE_PATH, "wb") as f:
                f.write(img_bytes)

            image_url = "/image"  # route below

        except Exception as e:
            analysis = f"Error occurred: {e}"

    return render_template("index.html", result=analysis, image_url=image_url)


@app.route("/image")
def serve_image():
    return send_file(LAST_IMAGE_PATH, mimetype="image/png")


if __name__ == "__main__":
    app.run()