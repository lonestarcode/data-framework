from src.pipeline.llm_handler import LLMHandler
from src.logging.logger import get_logger, log_execution_time
from src.monitoring.metrics import SUMMARY_GENERATION_TIME
from typing import Dict, List

logger = get_logger('summarizer')

class SummarizerPipeline:
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
        self.logger = logger

    @log_execution_time(logger)
    def generate_summary(self, text: str, source: str) -> Dict:
        try:
            with SUMMARY_GENERATION_TIME.time():
                summary_data = self.llm_handler.generate_summary(
                    f"Article from {source}: {text}"
                )
            
            return {
                "summary": summary_data["summary"],
                "model": summary_data["model"],
                "source": source
            }
        except Exception as e:
            self.logger.error(
                f"Summary generation failed: {str(e)}",
                extra={"source": source, "error": str(e)},
                exc_info=True
            )
            raise
