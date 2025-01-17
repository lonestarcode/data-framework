
1. Develop a web scraper that scrapes news, articles, blogs, and social media posts from a pre-defined list at pre-defined intervals.
2. Implement robust data pre-processing and filtering system, so that NLP can be used to identify and filter our irrelevant content.
3. Generate summarizations for each news item using GPT-4o or Claude 3.5 (Should be model agnostic). Summarization must include source attribution, as well as the 3-5 most relevant keyword tags for each news item.
4. Create front end to display summaries and allow users to search, categorize, and view source links. Additional news outlets should be able to be added by the user in the front end.
5. Implement error-handling for the pipeline. Provide dashboard or logging system to monitor data flow, errors, metrics etc. Provide “downtvote” options for the user to hide poor results, with feedback given to the system automatically.

Technical Requirements
Languages: Python, JavaScript (if necessary for web components)
Frameworks/Libraries: Flask/Django for backend, React/Angular for frontend, NLP libraries like Hugging Face Transformers or spaCy.
Database: Use of a database (e.g., PostgreSQL or MongoDB) to store collected data and generated summaries.
Cloud Services: AWS for hosting and scalability.

Deliverables
Fully functional news collection and summarization pipeline.
Website to host the summaries with basic search and categorization.
Documentation for the entire system, including setup, usage, and maintenance instructions.
Source code repository with clear structure and comments.


