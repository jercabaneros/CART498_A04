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
    dream_text = ""

    if request.method == "POST":
        dream_text = request.form.get("prompt", "")

        # ---- TEXT ANALYSIS (FIXED) ----
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # FIXED: Correct model name
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Jungian psychoanalyst. Interpret the dream using "
                            "Jung's theories: archetypes, shadow, anima/animus, symbols, "
                            "the collective unconscious, and individuation. "
                            "Provide a thoughtful interpretation in 200-300 words."
                        )
                    },
                    {"role": "user", "content": dream_text}
                ],
                max_tokens=400,  # FIXED: Correct parameter name
                temperature=0.7
            )

            # FIXED: Correct way to extract text
            analysis = response.choices[0].message.content

        except Exception as e:
            analysis = f"Text analysis failed: {e}"
            print(f"Text error: {e}")

        # ---- IMAGE GENERATION (FIXED) ----
        try:
            # Create a more detailed prompt for better images
            image_prompt = f"Create a surreal, dreamlike, symbolic artistic representation of this dream in the style of Jungian psychology: {dream_text[:500]}. Dreamlike, symbolic, archetypal imagery with rich symbolism. Mystical, cosmic, constellation-like elements."
            
            img_response = client.images.generate(
                model="dall-e-2",  # ChANGED from dall-e-3 (gpt-image-1 may not be available) to dall-e-2
                prompt=image_prompt,
                size="512x512",  # Better quality
                quality="standard",
                n=1,
                response_format="b64_json"  # Get base64 directly
            )

            # FIXED: Extract Base64 correctly
            image_base64 = img_response.data[0].b64_json
            image_data = f"data:image/png;base64,{image_base64}"

        except Exception as e:
            print(f"Image generation failed: {e}")
            image_data = None

    return render_template(
        "index.html",
        result=analysis,
        image=image_data,
        dream_text=dream_text
    )


if __name__ == "__main__":
    app.run(debug=True)