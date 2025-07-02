import base64
from google import genai
from google.genai import types
from config import GEMINI_API_KEY  # Ensure this file contains GEMINI_API_KEY = "your-api-key"

def generate():
    # Initialize the client with the API key
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
    # Specify the model and the content
    model = "gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="Hello, what is the formula for area of a triangle "),
            ],
        ),
    ]
    # Configuration for the response
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    # Stream and print the generated content
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")


if __name__ == "__main__":
    generate()
