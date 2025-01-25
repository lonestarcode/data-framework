This app is useful for understanding public sentiment and media engagement on a topic using data from Twitter.

This Flask application provides sentiment analysis and social engagement metrics for a given topic using Twitter data. Here’s how it works:
	1.	Fetches Tweets:
	•	Retrieves recent tweets containing the specified topic from verified Twitter accounts.
	•	Uses the Twitter API (requires a Bearer Token stored in an .env file).
	2.	Analyzes Sentiment:
	•	Processes each tweet’s text using TextBlob, a natural language processing library.
	•	Classifies the sentiment of tweets into positive, negative, or neutral categories.
	•	Returns the results as percentages.
	3.	Calculates Social Engagement:
	•	Provides a basic engagement metric by counting the number of tweets retrieved for the topic.
	4.	API Endpoint:
	•	GET /analyze?topic=<your_topic>
	•	Example: /analyze?topic=climate change
	•	Returns JSON data containing:
	•	Sentiment percentages (positive, negative, neutral).
	•	Media coverage (number of tweets).
	•	Social engagement (a proxy metric based on tweet count).
	5.	CORS Enabled:
	•	Cross-Origin Resource Sharing (CORS) is enabled, allowing the app to be accessed from web clients running on different origins.