from flask import Blueprint, request, jsonify
from src.pipeline.generator_pipeline import ContentGeneratorPipeline
from src.models.content import Article
import logging

content_bp = Blueprint('content', __name__)
logger = logging.getLogger(__name__)

@content_bp.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        summaries = data.get('summaries', [])
        topic = data.get('topic')
        
        if not summaries or not topic:
            return jsonify({'error': 'Missing required fields'}), 400
            
        generator = ContentGeneratorPipeline()
        article = generator.generate_article(summaries, topic)
        
        return jsonify({
            'status': 'success',
            'article': article.__dict__,
            'metrics': {
                'source_count': len(article.sources),
                'generated_at': article.generated_at.isoformat(),
                'sentiment_summary': article.sentiment_scores,
                'bias_metrics': article.bias_metrics
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500