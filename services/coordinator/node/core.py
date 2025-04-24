# coordinator_node/core.py
import os
import shutil
from rid_lib.types import KoiNetNode, KoiNetEdge
from koi_net import NodeInterface
from koi_net.protocol.node import NodeProfile, NodeType, NodeProvides
from .config import settings

name = "coordinator" # Define the name explicitly

identity_dir = f".koi/{name}"
cache_dir = f".koi/{name}/rid_cache_{name}"
# Remove existing directories if they exist
shutil.rmtree(identity_dir, ignore_errors=True)
shutil.rmtree(cache_dir, ignore_errors=True)

# Recreate the directories
os.makedirs(identity_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)


node = NodeInterface(
    name=name,
    profile=NodeProfile(
        base_url=f"http://{settings.HOST}:{settings.PORT}/koi-net",
        node_type=NodeType.FULL,
        provides=NodeProvides(
            event=[KoiNetNode, KoiNetEdge],
            state=[KoiNetNode, KoiNetEdge]
        )
    ),
    use_kobj_processor_thread=True,
    identity_file_path=f"{identity_dir}/{name}_identity.json", # Use the variable
    event_queues_file_path=f"{identity_dir}/{name}_event_queues.json", # Use the variable
    cache_directory_path=cache_dir # Use the variable
)
