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

        # ---- TEXT ANALYSIS ----
        try:
            response = client.chat.completions.create(
                model="gpt-4",
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
                max_tokens=400,
                temperature=0.7
            )

            analysis = response.choices[0].message.content

        except Exception as e:
            analysis = f"Text analysis failed: {e}"
            print(f"Text error: {e}")

        # ---- IMAGE GENERATION ----
        try:
            # Create a detailed prompt for better images
            image_prompt = f"Create a surreal, dreamlike, symbolic artistic representation of this dream in the style of Jungian psychology: {dream_text[:500]}. Dreamlike, symbolic, archetypal imagery with rich symbolism. Mystical, cosmic, constellation-like elements."
            
            # Try gpt-image-1 first, fall back to gpt-image-1-mini if it fails
            try:
                img_response = client.images.generate(
                    model="gpt-image-1",  # As required by assignment
                    prompt=image_prompt,
                    size="512x512",
                    n=1,
                    response_format="b64_json"
                )
            except Exception as e1:
                print(f"gpt-image-1 failed, trying gpt-image-1-mini: {e1}")
                #Try mini version?
                img_response = client.images.generate(
                    model="gpt-image-1-mini",  # Fallback as per assignment
                    prompt=image_prompt,
                    size="512x512",
                    n=1,
                    response_format="b64_json"
                )

            # Extract Base64 and convert for display
            image_base64 = img_response.data[0].b64_json
            image_data = f"data:image/png;base64,{image_base64}"

        except Exception as e:
            print(f"Image generation failed: {e}")
            # If gpt-image models don't work, fall back to dall-e-2 as last resort (chat api always sends error)
            try:
                print("Falling back to dall-e-2...")
                img_response = client.images.generate(
                    model="dall-e-2",
                    prompt=image_prompt,
                    size="512x512",
                    n=1,
                    response_format="b64_json"
                )
                image_base64 = img_response.data[0].b64_json
                image_data = f"data:image/png;base64,{image_base64}"
            except Exception as e2:
                print(f"All image generation failed: {e2}")
                image_data = None

    return render_template(
        "index.html",
        result=analysis,
        image=image_data,
        dream_text=dream_text
    )


if __name__ == "__main__":
    app.run(debug=True)