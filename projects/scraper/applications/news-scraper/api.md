
```markdown:scraper/docs/api.md
# API Documentation

## Authentication
All authenticated endpoints require a Bearer token in the Authorization header:
```bash
Authorization: Bearer <token>
```

## Endpoints

### Summaries

#### GET /api/summaries
Retrieves paginated list of article summaries.

**Query Parameters:**
- `category` (optional): Filter by source category
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10)

**Response:**
```json
{
    "items": [
        {
            "id": 1,
            "summary_text": "string",
            "model_used": "string",
            "keywords": ["string"],
            "created_at": "datetime",
            "article": {
                "title": "string",
                "url": "string",
                "source": "string"
            }
        }
    ],
    "total": 100,
    "pages": 10
}
```

#### GET /api/summaries/search
Search through summaries.

**Query Parameters:**
- `q`: Search query string

**Response:**
```json
[
    {
        "id": 1,
        "summary_text": "string",
        "keywords": ["string"],
        "url": "string"
    }
]
```

### Sources

#### GET /api/sources
Get list of news sources.

**Query Parameters:**
- `type` (optional): Filter by source type (news, blog, social_media)

**Response:**
```json
[
    {
        "id": 1,
        "name": "string",
        "url": "string",
        "type": "string",
        "scraping_interval": "string",
        "added_by_user": boolean,
        "created_at": "datetime"
    }
]
```

#### POST /api/sources
Add new news source.

**Authentication Required:** Yes (ADMIN or EDITOR role)

**Request Body:**
```json
{
    "name": "string",
    "url": "string",
    "type": "string",
    "interval": "string" // optional
}
```

**Response:**
```json
{
    "status": "success",
    "source_id": 1
}
```

### Feedback

#### POST /api/feedback
Submit feedback for a summary.

**Request Body:**
```json
{
    "summary_id": 1,
    "feedback_type": "string", // downvote, irrelevant, poor_summary
    "comment": "string" // optional
}
```

**Response:**
```json
{
    "status": "success",
    "feedback_id": 1
}
```

## Error Responses
All endpoints return error responses in the following format:

```json
{
    "error": "Error message description"
}
```

Common HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting
API requests are limited to:
- Authenticated users: 1000 requests per hour
- Unauthenticated users: 100 requests per hour

## Monitoring
Metrics for API usage are available at `/metrics` endpoint (internal use only).
```

This documentation references the following code blocks:


```9:41:scraper/src/api/summary_routes.py
@summary_bp.route('/summaries', methods=['GET'])
def get_summaries():
    try:
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        query = Summary.query.join(Article)
        if category and category != 'all':
            query = query.filter(Article.source == category)
            
        summaries = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'items': [s.to_dict() for s in summaries.items],
            'total': summaries.total,
            'pages': summaries.pages
        })
    except Exception as e:
        logger.error(f"Error fetching summaries: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch summaries'}), 500

@summary_bp.route('/summaries/search', methods=['GET'])
def search_summaries():
    try:
        query = request.args.get('q', '')
        summaries = Summary.query.filter(
            Summary.summary_text.ilike(f'%{query}%')
        ).all()
        return jsonify([s.to_dict() for s in summaries])
    except Exception as e:
        logger.error(f"Error searching summaries: {str(e)}", exc_info=True)
        return jsonify({'error': 'Search failed'}), 500
```



```10:29:scraper/src/api/source_routes.py
@source_bp.route('/sources', methods=['GET'])
def get_sources():
    try:
        source_type = request.args.get('type')
        sources = SourceManager.get_sources(source_type)
        return jsonify(sources)
    except Exception as e:
        logger.error(f"Error fetching sources: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch sources'}), 500

@source_bp.route('/sources', methods=['POST'])
@require_auth([UserRole.ADMIN, UserRole.EDITOR])
def add_source():
    try:
        source_data = request.get_json()
        result = SourceManager.add_source(source_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error adding source: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to add source'}), 500
```



```9:22:scraper/src/api/feedback_routes.py
@feedback_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback_data = request.get_json()
        handler = FeedbackHandler(db.session)
        result = handler.handle_feedback(
            summary_id=feedback_data['summary_id'],
            feedback_type=feedback_data['feedback_type'],
            comment=feedback_data.get('comment')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to submit feedback'}), 500
```


The documentation provides:
1. Clear endpoint descriptions
2. Request/response formats
3. Authentication requirements
4. Error handling
5. Rate limiting information
6. Monitoring details

This should help developers integrate with the API more effectively.
