import os
import shutil
import logging

from koi_net import NodeInterface
from koi_net.protocol.node import NodeProfile, NodeType, NodeProvides

from .config import HOST, PORT, FIRST_CONTACT
from .types import GithubCommit

logger = logging.getLogger(__name__)

name = "sensor"

identity_dir = f".koi/{name}"
cache_dir = f".koi/{name}/rid_cache_{name}"
# Remove existing directories if they exist
shutil.rmtree(identity_dir, ignore_errors=True)
shutil.rmtree(cache_dir, ignore_errors=True)

# Recreate the directories
os.makedirs(identity_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)

# Initialize the KOI-net Node Interface for the GitHub Sensor
node = NodeInterface(
    name=name,
    profile=NodeProfile(
        base_url=f"http://{HOST}:{PORT}/koi-net",
        node_type=NodeType.FULL, # Assuming it provides data and potentially processes
        provides=NodeProvides(
            event=[GithubCommit], # Provides GithubCommit events
            state=[GithubCommit]  # Can serve state for GithubCommit RIDs
        )
    ),
    use_kobj_processor_thread=True, # Use a background thread for processing
    first_contact=FIRST_CONTACT,   # Coordinator node to connect to initially
    identity_file_path=f"{identity_dir}/{name}_identity.json", # Use the variable
    event_queues_file_path=f"{identity_dir}/{name}_event_queues.json", # Use the variable
    cache_directory_path=cache_dir # Use the variable
)

logger.info(f"Initialized NodeInterface: {node.identity.rid}")
logger.info(f"Node attempting first contact with: {FIRST_CONTACT}")
