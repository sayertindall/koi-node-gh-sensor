import logging
import json
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # --- KOI-net Configuration ---
    URL: str = Field(..., description="Public URL where this Github node can be reached by other KOI-net nodes.")
    FIRST_CONTACT: str = Field(..., description="URL of the coordinator node or another known KOI-net node.")

    # --- Github Sensor Server Configuration ---
    HOST: str = Field(default="127.0.0.1", description="Host the FastAPI server should listen on.")
    PORT: int = Field(default=8001, description="Port the FastAPI server should listen on.")

    # --- Github Configuration ---
    GITHUB_TOKEN: Optional[str] = Field(default=None, description="Optional Github Personal Access Token.")
    # Load MONITORED_REPOS from env var as a string
    MONITORED_REPOS_STR: str = Field(alias="MONITORED_REPOS", default="", description="Comma-separated list of repositories (owner/repo).")
    GITHUB_WEBHOOK_SECRET: str = Field(..., description="Secret used to verify webhook signatures.")

    # --- State File ---
    STATE_FILE_PATH: str = Field(default="state.json", description="Path to the JSON file storing the last processed commit SHA.")

    # --- Logging Configuration ---
    LOG_LEVEL: str = Field(default="INFO", description="Logging level (e.g., DEBUG, INFO, WARNING).")

    @property
    def MONITORED_REPOS(self) -> List[str]:
        """Parses the comma-separated MONITORED_REPOS_STR into a list of 'owner/repo' strings."""
        if not self.MONITORED_REPOS_STR:
            return []
        # Split by comma, strip whitespace, and filter out empty strings
        repos = [repo.strip() for repo in self.MONITORED_REPOS_STR.split(',') if repo.strip()]
        logger.debug(f"Parsed monitored repos: {repos}")
        return repos

    class Config:
        env_file = 'services/github/.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

# Instantiate settings early to catch config errors on import
try:
    settings = Settings()
    # Apply log level from settings
    logging.getLogger().setLevel(settings.LOG_LEVEL.upper())
    logger.info("Configuration loaded successfully.")
    logger.info(f"Settings: {settings.model_dump(exclude={'GITHUB_TOKEN', 'GITHUB_WEBHOOK_SECRET'})}") # Exclude token and secret from debug logs
except Exception as e:
    logger.exception(f"Failed to load configuration from .env file: {e}")
    # Optionally re-raise or exit if config is critical
    raise

# --- Exported Variables ---
# Make settings easily accessible throughout the application
URL = settings.URL
FIRST_CONTACT = settings.FIRST_CONTACT
HOST = settings.HOST
PORT = settings.PORT
GITHUB_TOKEN = settings.GITHUB_TOKEN
GITHUB_WEBHOOK_SECRET = settings.GITHUB_WEBHOOK_SECRET
MONITORED_REPOS = settings.MONITORED_REPOS # Access the parsed list via the property
STATE_FILE_PATH = settings.STATE_FILE_PATH
LOG_LEVEL = settings.LOG_LEVEL

# --- State Management (Loading initial state & update function) ---
LAST_PROCESSED_SHA = {} # Dictionary mapping repo_name -> last_sha

def load_state():
    """Loads the last processed SHA state from the JSON file."""
    global LAST_PROCESSED_SHA
    try:
        with open(STATE_FILE_PATH, 'r') as f:
            LAST_PROCESSED_SHA = json.load(f)
        logger.info(f"Loaded state from '{STATE_FILE_PATH}': {list(LAST_PROCESSED_SHA.keys())}")
    except FileNotFoundError:
        logger.warning(f"State file '{STATE_FILE_PATH}' not found. Starting with empty state.")
        LAST_PROCESSED_SHA = {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from state file '{STATE_FILE_PATH}'. Starting with empty state.")
        LAST_PROCESSED_SHA = {}
    except Exception as e:
        logger.error(f"Unexpected error loading state file '{STATE_FILE_PATH}': {e}", exc_info=True)
        LAST_PROCESSED_SHA = {}

def update_state_file(repo_name: str, last_sha: str):
    """Updates the state file with the latest processed SHA for a repo."""
    global LAST_PROCESSED_SHA
    LAST_PROCESSED_SHA[repo_name] = last_sha
    try:
        # Create directory if it doesn't exist (though it should usually be just the filename)
        # import os
        # os.makedirs(os.path.dirname(STATE_FILE_PATH), exist_ok=True) # Uncomment if path can include dirs
        with open(STATE_FILE_PATH, 'w') as f:
            json.dump(LAST_PROCESSED_SHA, f, indent=4)
        logger.debug(f"Updated state file '{STATE_FILE_PATH}' for {repo_name} with SHA: {last_sha}")
    except IOError as e:
        logger.error(f"Failed to write state file '{STATE_FILE_PATH}': {e}")
    except Exception as e:
        logger.error(f"Unexpected error writing state file '{STATE_FILE_PATH}': {e}", exc_info=True)

# Load initial state when config module is imported
load_state()
