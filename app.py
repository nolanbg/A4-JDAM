from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


# Jungian system prompt
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


@app.route("/", methods=["GET", "POST"])
def index():

    interpretation = None
    image_path = None

    if request.method == "POST":

        dream_text = request.form["dream"]

        try:
            # ---------------------------
            # TEXT INTERPRETATION
            # ---------------------------

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


            # ---------------------------
            # IMAGE GENERATION
            # ---------------------------

            image_prompt = f"""
            Create a surreal, symbolic dreamlike illustration
            inspired by this dream and its Jungian meaning:

            {dream_text}

            Style: painterly, mystical, atmospheric,
            symbolic, psychological, soft lighting
            """

            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024"
            )

            # Decode base64 image
            image_base64 = image_response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            image = Image.open(BytesIO(image_bytes))

            # Save image
            filename = f"{uuid.uuid4()}.png"
            image_path = f"static/{filename}"

            image.save(image_path)


        except Exception as e:
            interpretation = f"Error: {str(e)}"


    return render_template(
        "index.html",
        interpretation=interpretation,
        image_path=image_path
    )


if __name__ == "__main__":
    app.run(debug=True)

