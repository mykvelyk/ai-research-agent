import logging
import time

from ai_research_agent.config import Settings
from ai_research_agent.observability import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    logger.info("worker_idle", extra={"outcome": "idle"})
    while True:
        # Claim/execute due runs once persistence exists.
        time.sleep(30)
