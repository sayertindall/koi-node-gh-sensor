import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()]
)




