import yaml
import logging
import os
from datetime import datetime

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        raise

def setup_logging(log_file: str) -> None:
    """Configure logging with custom format."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        filemode='a',
        format='%(asctime)s [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logging initialized")

def get_timestamp() -> str:
    """Return current timestamp for logging or display."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')