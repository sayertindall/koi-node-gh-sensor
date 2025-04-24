import uvicorn
import logging
from .config import settings

logger = logging.getLogger(__name__)

logger.info(f"Coordinator node starting on {settings.HOST}:{settings.PORT}")
uvicorn.run("services.coordinator.node.server:app", host=settings.HOST, port=settings.PORT, log_config=None)
