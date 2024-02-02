import speech_recognition as sr
from gtts import gTTS
import os
import playsound
from openai import OpenAI

#Initialize the speech recognizer
recognizer = sr.Recognizer()

#Define a function to listen to the microphone for the wake word and commands to return the audio as text.

def listen():
    with sr.Microphone() as source:
        print("Listening for 'hola robot'...")
        while True:
            try:
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")

                    # Check for wake word
                    if "hey robot" in text:
                        print("Wake word detected! Listening for your command...")
                        audio = recognizer.listen(source)
                        text = recognizer.recognize_google(audio).lower()
                        return text
                except sr.UnknownValueError:
                    print("I did not understand that")
                except sr.RequestError:
                    print("Request Failed")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Could not request results")

#Define a function to get a response from OpenAI

# Cargar las variables de entorno desde el archivo .env
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI(
    # This is the default and can be omitted
    api_key = os.getenv("OPENAI_API_KEY"),
)


def get_chatgpt_response(text):
    # Prepare the prompt with the user's input text

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": "I want you to act as a english teacher for kids betwen 6 and 9 years old. I will talk to you whit de key frase 'hola eprof' and then you gona provide some lenguaje lessons, games or concepts, and it will be your job to explain them in easy-to-understand terms. This could include providing step-by-step instructions for solving a problem, demonstrating various techniques with visuals or suggesting online resources for further study. "},
                  {"role": "user", "content": text}]
    )
    return response.choices[0].message.content

#Define a function to verbalize the response
# Function to verbalize the response
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")

#Main Loop
def main():
    while True:
        # Listen for commands
        command = listen()
        if command:
            print("You said:", command)
            # Check for a quit command
            if 'quit' in command.lower() or 'exit' in command.lower():
                print("Exiting voice assistant...")
                break
            # Get ChatGPT response
            response = get_chatgpt_response(command)
            print("ChatGPT:", response)

            # Speak the response
            speak(response)

if __name__ == "__main__":
    main()

#Run the program. Program defaults to “Listening for ‘Hey Robot’. Once the wake up command is initiated, the voice assistant is ready to accept the commands. Next, plug in the microphone and you should be able to hear the response from OpenAI.
