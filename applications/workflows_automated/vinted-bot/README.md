README: Vinted Bot

Overview

This Vinted Bot automates publishing items on Vinted at scheduled times. By default, it:
	1.	Logs into your Vinted account.
	2.	Navigates to your drafts page.
	3.	Publishes your first draft at the desired start time (e.g., 6:00 AM).
	4.	Waits until the item is actually live (using checks like the view count).
	5.	Once live, waits a user-defined interval (e.g., 30 or 60 minutes) before publishing the next draft.
	6.	Continues until all drafts have been published or the bot is stopped.

A web-based interface (Flask + Vanilla JS) allows you to configure the start time, interval, and monitor logs in real time.

Directory Structure

vinted-bot/
├── app.py
├── config/
│   └── config.yaml
├── requirements.txt
├── scripts/
│   └── main.py
├── static/
│   ├── app.js
│   └── styles.css
└── templates/
    └── index.html

	•	app.py: The Flask app providing a simple GUI and API endpoints.
	•	config/config.yaml: Stores credentials and default scheduling settings.
	•	requirements.txt: Lists the Python dependencies required to run the bot.
	•	scripts/main.py: Core Vinted bot logic (login, publishing, checks).
	•	static/: Frontend files – JS and CSS.
	•	templates/: HTML template (index.html) for the web-based GUI.

Prerequisites
	1.	Python 3.7+ installed.
	2.	Selenium WebDriver (e.g., ChromeDriver) installed and on your PATH if you’re using Selenium.
	•	Alternatively, if using Playwright, you’d install its dependencies instead.
	3.	(Optional) A virtual environment for clean dependency management.

Installation
	1.	Download or clone this repository (or unzip the vinted-bot folder).
	2.	In a terminal, navigate to the vinted-bot directory:

cd vinted-bot


	3.	(Optional but recommended) Create and activate a virtual environment:

# Create a venv
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate


	4.	Install dependencies:

pip install -r requirements.txt

Configuration

Open config/config.yaml to update:
	•	Username and Password for your Vinted account:

login:
  username: "YOUR_VINTED_USERNAME"
  password: "YOUR_VINTED_PASSWORD"


	•	Default scheduling:

schedule:
  start_time: "06:00"        # e.g., 6 AM
  interval_minutes: 60       # e.g., 60 minutes between live listings

intervals:
  check_live_interval_seconds: 30   # how often to poll for "live" status



These values can also be changed via the web interface at runtime.

Usage
	1.	Run the Flask server:

python app.py


	2.	Open a browser to http://127.0.0.1:5000.
	3.	Adjust the Start Time and Interval fields:
	•	Start Time: The exact time for publishing the first draft (HH:MM, 24-hour format).
	•	Interval (minutes): The delay after a listing goes live before publishing the next listing.
	4.	Click “Start Bot”:
	•	The bot will log in at the appropriate time and publish your first draft.
	•	It will wait for the listing to go live (based on view count or other checks) before starting the countdown for the next draft.
	5.	Check “Logs”:
	•	The bottom section updates every few seconds with messages about the bot’s progress.
	6.	Stop Bot:
	•	A “Stop Bot” button is provided but requires additional logic in main.py if you want to gracefully terminate an ongoing process.

Key Files
	1.	scripts/main.py:
	•	run_vinted_bot() orchestrates the steps:
	1.	Login
	2.	Publish first draft at the scheduled time
	3.	Check go-live status by polling the listing’s public URL
	4.	Wait the user-specified interval (in minutes)
	5.	Repeat until no more drafts (or process stopped)
	2.	app.py:
	•	Flask server routes:
	•	/start-bot: Launches the bot in a new thread.
	•	/stop-bot: Stub for stopping the bot (not fully implemented).
	•	/logs: Returns real-time bot logs as JSON.
	•	index() route serves templates/index.html.
	3.	Frontend (JS/CSS/HTML):
	•	static/app.js: Handles “Start Bot” & “Stop Bot” button clicks, fetches logs periodically.
	•	static/styles.css: Basic styling.
	•	templates/index.html: The layout for the control panel UI.

Troubleshooting
	•	Selenium Exceptions: If you see a WebDriver error, confirm you have the correct ChromeDriver (or other driver) installed.
	•	Login Failures: Double-check your username/password. Make sure the Vinted domain in login_to_vinted() is correct for your region.
	•	Draft Selectors: If Vinted changes how the “Publish” button or “view count” is displayed, update the XPath or CSS Selector in main.py.
	•	Schedule: If your start time is in the past, the bot will wait until the next day unless you’ve customized the logic.
	•	Stop Logic: By default, the bot can’t be interrupted mid-process unless you add manual checks in the code (e.g., a shared stop flag).

Extending the Bot
	•	Random Delays: Implement random intervals around the publish time to appear more human-like.
	•	GUI Enhancements: Add more fields or advanced scheduling (e.g., multiple times per day, day-of-week schedules).
	•	Logging: Integrate Python’s logging module or a framework like loguru for persistent logs.
	•	Deployment: Package in a Docker container or host on a cloud server for 24/7 operation.



The client’s primary goals and requirements can be summarized as follows:
	1.	Schedule Listings at Specific Times
	•	They want the first listing to go live at a particular start time (e.g., 6 AM).
	2.	Consecutive Listings Published at Intervals After Going Live
	•	Once the first listing goes live, the bot should wait a custom interval (e.g., 30 minutes or 1 hour) after confirmation of the listing being live before publishing the next.
	3.	Go-Live Detection
	•	Because Vinted has a verification period, the client wants the bot to check when the listing is actually live.
	•	The easiest proxy: wait until the item has at least one view—this typically means it’s publicly visible and out of the verification queue.
	4.	Batch of Drafts
	•	The client plans to draft all listings in advance.
	•	The bot’s only job is to publish them in sequence, enforcing the scheduled start time for the first listing and then the time gaps between subsequent ones.
	5.	Fully Automated
	•	The client wants the process to be hands-off: set it once (with a specified start time and intervals), and let the bot handle everything while they are offline.