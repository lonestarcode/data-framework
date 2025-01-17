import os
import openai
import speech_recognition as sr
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Load environment variables
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the recognizer
recognizer = sr.Recognizer()

# Global flag for graceful shutdown
running = True

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n{text}"}
            ],
            max_tokens=150,
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(20)
        return summarize_text(text)  # Retry
    except openai.error.APIError as e:
        print(f"OpenAI API error: {e}")
    except openai.error.Timeout:
        print("OpenAI API request timed out. Please try again later.")
    except openai.error.APIConnectionError:
        print("Failed to connect to OpenAI API. Please check your internet connection.")
    except openai.error.InvalidRequestError as e:
        print(f"Invalid request to OpenAI API: {e}")
    except openai.error.AuthenticationError:
        print("Authentication to OpenAI API failed. Please check your API key.")
    except openai.error.ServiceUnavailableError:
        print("OpenAI service is unavailable. Please try again later.")
    return None

def transcribe_audio(audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from the service; {e}")
    return None

def process_audio(audio):
    global running
    if not running:
        return
    transcription = transcribe_audio(audio)
    if transcription:
        print(f"Transcription: {transcription}")
        print("Summarizing transcription...")
        summary = summarize_text(transcription)
        if summary:
            print(f"Summary: {summary}")

def listen_and_process(source, executor):
    global running
    while running:
        try:
            print("\nListening for audio...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            executor.submit(process_audio, audio)
        except sr.WaitTimeoutError:
            print("Timeout; no speech detected.")

def main():
    global running
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Listening... (Press Ctrl+C to exit)")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            listener_thread = threading.Thread(target=listen_and_process, args=(source, executor))
            listener_thread.start()
            
            try:
                while running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down...")
                running = False
            finally:
                listener_thread.join()
                print("Waiting for pending tasks to complete...")
                executor.shutdown(wait=True)
                print("Cleanup complete. Exiting the program.")

if __name__ == "__main__":
    main()