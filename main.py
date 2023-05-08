import openai
import pyttsx3
import speech_recognition as sr
import time

openai.api_key = "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"

engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            if text is not None:
                return text
            else:
                return ''
        except:
            print('Skipping unknown error')
            return ''


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Say 'Hey Gideon' to start recording your question ... ")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription is not None:
                    if transcription.lower() == "hey gideon":
                        filename = "input.wav"
                        Greet = "How can I help you today, sir?"
                        print(Greet)
                        speak_text(Greet)
                        while True:
                            with sr.Microphone() as source:
                                recognizer = sr.Recognizer()
                                source.pause_threshold = 1
                                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                with open(filename, "wb") as f:
                                    f.write(audio.get_wav_data())

                            text = transcribe_audio_to_text(filename)
                            if text.lower() == "thank you gideon" and transcription is not None:
                                print(f"You said: {text}")
                                Bye = "Have a nice day sir."
                                print(Bye)
                                speak_text(Bye)
                                break
                            else:
                                print(f"You said: {text}")
                                response = generate_response(text)
                                print(f"Gideon: {response}")
                                speak_text(response)
                                continuemsg = "Anything else sir?"
                                print(continuemsg)
                                speak_text(continuemsg)

            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            except Exception as e:
                print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()

