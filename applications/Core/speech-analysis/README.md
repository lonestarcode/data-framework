This Python script listens for spoken audio using a microphone, transcribes it into text, summarizes the transcription using OpenAI’s GPT-3.5 API, and displays both the transcription and summary. It’s designed to handle multiple audio inputs concurrently and ensures graceful shutdown when interrupted.

📝 Explanation of the Code

1. Setup and Imports
	•	Libraries Used:
	•	os: Access environment variables.
	•	openai: Communicates with the OpenAI API for text summarization.
	•	speech_recognition: Captures and processes audio input.
	•	dotenv: Loads environment variables from a .env file.
	•	ThreadPoolExecutor: Manages concurrent processing of tasks.
	•	threading: Handles the listening loop in a separate thread.
	•	time: Adds delays for rate-limiting and ensures smooth shutdowns.
	•	Environment Setup:
	•	The OpenAI API key is loaded from the .env file.
	•	Speech Recognition:
	•	Recognizer: Converts spoken audio into text.
	•	Global Variables:
	•	running: A flag to control the program’s main loop for graceful shutdown.

2. Core Functions

2.1 summarize_text(text)
	•	Sends the transcription to OpenAI’s GPT-3.5 API for summarization.
	•	Handles various API errors (rate limits, authentication issues, timeouts).
	•	Retries automatically after encountering a RateLimitError.

Example Input:
"This is a long explanation about machine learning and AI advancements."

Example Output:
"Machine learning and AI have seen significant advancements in recent years."

2.2 transcribe_audio(audio)
	•	Uses Google Speech Recognition to transcribe spoken audio into text.
	•	Handles errors like:
	•	UnknownValueError: Audio couldn’t be understood.
	•	RequestError: Issues with the speech recognition API.

Example Input:
Spoken words: “Hello, how are you?”

Example Output:
"Hello, how are you?"

2.3 process_audio(audio)
	•	Transcribes audio into text.
	•	Passes the transcription to summarize_text.
	•	Displays both the transcription and summary.

Example Workflow:
	1.	Audio is transcribed: "Artificial Intelligence is transforming the world."
	2.	Sent to OpenAI: Summarized to "AI is reshaping industries."

2.4 listen_and_process(source, executor)
	•	Continuously listens for audio input from the microphone.
	•	Processes audio using a ThreadPoolExecutor, allowing multiple audio tasks to run simultaneously.

Key Details:
	•	timeout=5: Waits 5 seconds for speech before retrying.
	•	phrase_time_limit=10: Limits each phrase to 10 seconds.

3. Main Function

3.1 Ambient Noise Adjustment
	•	Adjusts the microphone sensitivity to filter out background noise.

3.2 Threading for Listening
	•	listen_and_process runs in a separate thread to ensure the main program remains responsive.

3.3 Graceful Shutdown
	•	The program can be stopped with Ctrl+C.
	•	Ensures all pending audio tasks finish before exiting.

🛠️ How the Program Works Step-by-Step
	1.	Start Program:
	•	Adjusts for ambient noise.
	•	Begins listening for audio in a loop.
	2.	Audio Captured:
	•	User speaks into the microphone.
	•	Audio is sent to transcribe_audio.
	3.	Transcription:
	•	Audio is converted to text.
	•	Text is displayed in the console.
	4.	Summarization:
	•	Transcribed text is sent to OpenAI’s GPT API.
	•	Summary is generated and displayed.
	5.	Concurrency:
	•	Multiple audio inputs are processed in parallel via ThreadPoolExecutor.
	6.	Graceful Shutdown:
	•	Ctrl+C stops the program.
	•	Ensures all ongoing tasks are completed.

🎤 Sample Output

Adjusting for ambient noise...
Listening... (Press Ctrl+C to exit)

Listening for audio...
Transcription: Artificial Intelligence is shaping the future of technology.
Summarizing transcription...
Summary: AI is driving technological advancements across industries.

🚀 Key Features
	•	Real-Time Audio Processing: Processes audio input continuously without blocking the main program.
	•	Parallel Execution: Multiple audio tasks are handled concurrently using a thread pool.
	•	Error Handling: Robust error handling for both speech recognition and API calls.
	•	Graceful Shutdown: Stops smoothly on Ctrl+C.

🛡️ Error Handling Examples
	1.	Rate Limit Error: Waits and retries after 20 seconds.
	2.	Audio Not Understood: Informs the user.
	3.	API Connection Issues: Provides clear error messages.

📚 Dependencies

Ensure these libraries are installed:

pip install openai speechrecognition python-dotenv

Additionally:
	•	A .env file with OPENAI_API_KEY=<your_api_key>.

This program is an efficient, scalable tool for live audio transcription and summarization using OpenAI’s GPT API.