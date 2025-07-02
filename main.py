import speech_recognition as sr
import os
import win32com.client
import webbrowser
import subprocess, sys
import datetime
from google import genai
from google.genai import types
from config import GEMINI_API_KEY
import Gemini


# todo : make sure that jarvis says only the required portion of text and does not print it unnecessarily
chatStr = ""


def chat(query):
    global chatStr
    # chatStr += f"Rasaal: {query}\n Jarvis: "
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    # gemini-2.5-pro-exp-03-25
    # gemini-2.0-flash-lite
    # gemini-2.5-flash-preview-04-17
    # gemini-2.0-flash
    model = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=query),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text",
        system_instruction=[
            types.Part.from_text(text="""Give outputs in about 100 words.
            Do not use '*' symbol in output.
            Give output in form of plain text only."""),
        ],
    )
    try:
        for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            # print(chunk.text, end="")
            say(chunk.text)
    except Exception as e:
        print("Error occurred during content generation : ", e)
        chatStr += "\nError during content generation."
    say(chatStr)

    return chatStr


def generate(prompt):
    text = f"Gemini response for prompt {prompt} \n*******************************\n\n"

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
    model = "gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                system_instruction=[
                    types.Part.from_text(text="""Give outputs in about 100 words.
        Do not use '*' symbol in output.
        Give output in form of plain text only."""),
                ],
    )
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            # print(chunk.text, end="")
            text += chunk.text
    except Exception as e:
        print("Error occurred during content generation : ", e)
        text += "\nError during content generation."

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")
    prompt_suffix: str = '-'.join(prompt.split('intelligence')[1:]).strip()
    filename: str = f"{prompt_suffix}.txt"
    filepath = os.path.join("Gemini", filename)
    with open(filepath, "w") as f:
        f.write(text)


speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text):
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language = "en-in")
            print(f"User Said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred, Sorry from Jarvis"


if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Hello, I am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: add more websites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["instagram", "https://www.instagram.com"], ["linkedin", "https://www.linkedin.com"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Ma'am...")
                webbrowser.open(site[1])

        # todo: debug why the following code is not functional and rectify it + add more apps to it
        apps = [["excel", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Excel.lnk"],
                ["onenote", "onenote.exe"]]

        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"opening {app[0]} Ma'am")
                subprocess.run([app[1]])

        # todo: add more songs to the songs list

        songs = [["Royalty", "C:/Users/rasaa/Downloads/audio.mp3"]]
        for song in songs:
            if f"play {song[0]}".lower() in query.lower():
                try:
                    os.system(f"start {song[1]}")
                except Exception as e:
                    say("Can't play audio, Sorry from Jarvis")

        if "the time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Ma'am the time is {strfTime}")

        elif "artificial intelligence".lower() in query.lower():
            generate(query)

        elif "Jarvis Quit".lower() in query.lower():
            say("Quitting Jarvis, Have a good day Ma'am")
            exit()

        elif "Jarvis reset chat".lower() in query.lower():
            chatStr = ""

        else:
            chat(query)