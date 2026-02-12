from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64
import uuid

# ----------------------------------
# Load environment variables
# ----------------------------------

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


# ----------------------------------
# Jungian System Prompt
# ----------------------------------

JUNGIAN_PROMPT = """
You are a Jungian psychoanalyst specializing in dream interpretation.

Analyze dreams using:
- Archetypes (Shadow, Anima/Animus, Self, Hero, Wise Old Man, etc.)
- Symbols
- Collective unconscious
- Emotional patterns
- Personal growth themes

Provide thoughtful, reflective interpretations.
Avoid medical diagnoses.
Speak clearly and empathetically.
"""


# ----------------------------------
# Main Route
# ----------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    interpretation = None
    image_path = None
    error_message = None

    if request.method == "POST":

        dream_text = request.form.get("dream", "").strip()

        if not dream_text:
            error_message = "Please enter a dream."
            return render_template(
                "index.html",
                interpretation=interpretation,
                image_path=image_path,
                error=error_message
            )

        try:
            # ----------------------------------
            # TEXT INTERPRETATION
            # ----------------------------------

            text_response = openai.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "system",
                        "content": JUNGIAN_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"Interpret this dream:\n{dream_text}"
                    }
                ],
                temperature=0.9,
                max_output_tokens=400
            )

            interpretation = text_response.output_text


            # ----------------------------------
            # IMAGE GENERATION (SAFE)
            # ----------------------------------

            image_prompt = f"""
            Create a surreal, symbolic, dreamlike illustration
            inspired by this dream and its Jungian meaning:

            {dream_text}

            Style: painterly, mystical, atmospheric,
            psychological, soft lighting
            """

            try:

                image_response = openai.images.generate(
                    model="gpt-image-1-mini",
                    prompt=image_prompt,
                    size="1024x1024"   # Lower memory
                )

                image_base64 = image_response.data[0].b64_json

                filename = f"{uuid.uuid4()}.png"
                image_path = f"static/{filename}"

                with open(image_path, "wb") as f:
                    f.write(base64.b64decode(image_base64))


            except Exception as img_error:

                # Log but don't crash
                print("Image generation failed:", img_error)
                image_path = None


        except Exception as e:

            print("Main error:", e)
            error_message = "Something went wrong. Please try again."



    return render_template(
        "index.html",
        interpretation=interpretation,
        image_path=image_path,
        error=error_message
    )


# ----------------------------------
# Run App
# ----------------------------------

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
