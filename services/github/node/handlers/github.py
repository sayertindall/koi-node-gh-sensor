import logging
from rid_lib.ext import Bundle
# Assuming GithubCommit RID type is accessible
from ..core import node # Import the initialized node instance
from ..types import GithubCommit # Ensure this import is correct

# Imports needed for coordinator_contact handler from refactor.md
from koi_net.processor.handler import HandlerType
from koi_net.processor.knowledge_object import KnowledgeObject, KnowledgeSource
from koi_net.processor.interface import ProcessorInterface
from koi_net.protocol.node import NodeProfile
from koi_net.protocol.event import EventType
from koi_net.protocol.edge import EdgeType
from koi_net.protocol.helpers import generate_edge_bundle
from rid_lib.types import KoiNetNode # Assuming this RID type is accessible

logger = logging.getLogger(__name__)

@node.processor.register_handler(HandlerType.Network, rid_types=[KoiNetNode])
def coordinator_contact(processor: ProcessorInterface, kobj: KnowledgeObject):
    """Handles discovery of the coordinator node (or other nodes providing KoiNetNode events).
    
    On discovering a NEW coordinator, proposes a WEBHOOK edge for bidirectional
    communication and requests a list of other known nodes (sync).
    (Based on refactor.md example)
    """
    if kobj.normalized_event_type != EventType.NEW:
        logger.debug(f"Ignoring non-NEW event for KoiNetNode {kobj.rid}")
        return
        
    # Validate that the discovered node actually provides network events
    try:
        profile = kobj.bundle.validate_contents(NodeProfile)
        if KoiNetNode not in profile.provides.event:
            logger.debug(f"Node {kobj.rid} does not provide KoiNetNode events. Ignoring.")
            return
    except Exception as e:
        logger.warning(f"Could not validate NodeProfile for {kobj.rid}: {e}")
        return

    logger.info(f"Identified potential coordinator/peer: {kobj.rid}; proposing WEBHOOK edge")
    try:
        # Propose edge FROM coordinator TO self
        edge_bundle = generate_edge_bundle(
            source=kobj.rid, 
            target=node.identity.rid,
            edge_type=EdgeType.WEBHOOK,
            rid_types=[KoiNetNode] # Specify the type of information this edge carries
        )
        processor.handle(bundle=edge_bundle)
    except Exception as e:
        logger.error(f"Failed to generate or handle WEBHOOK edge bundle for {kobj.rid}: {e}", exc_info=True)

    # Sync network nodes from the discovered node
    logger.info(f"Syncing network nodes from {kobj.rid}")
    try:
        payload = processor.network.request_handler.fetch_rids(kobj.rid, rid_types=[KoiNetNode])
        if not payload or not payload.rids:
             logger.warning(f"Received empty RIDs payload from {kobj.rid} during sync.")
             return
             
        logger.debug(f"Received {len(payload.rids)} RIDs from {kobj.rid}")
        for rid in payload.rids:
            # Don't process self or already known nodes
            if rid == processor.identity.rid or processor.cache.exists(rid):
                continue
            logger.debug(f"Handling discovered RID from sync: {rid}")
            # Handle the RID to fetch its details (profile, etc.)
            processor.handle(rid=rid, source=KnowledgeSource.External)
    except Exception as e:
        logger.error(f"Failed during network sync with {kobj.rid}: {e}", exc_info=True)

@node.processor.register_handler(HandlerType.Bundle, rid_types=[GithubCommit])
def handle_github_commit(processor: ProcessorInterface, kobj: KnowledgeObject):
    """
    Basic handler for processing GithubCommit bundles.
    Currently just logs information.
    
    Args:
        bundle: The Bundle object containing the GithubCommit RID and contents.
    """
    try:
        # kobj.bundle is guaranteed to exist in Bundle handler phase
        bundle = kobj.bundle
        rid: GithubCommit = bundle.rid
        contents: dict = bundle.contents
        
        logger.info(f"Processing commit: {rid} (Normalized Type: {kobj.normalized_event_type}, Source: {kobj.source})")
        # Log some details from the contents for visibility
        logger.debug(f"  Author: {contents.get('author_name')} <{contents.get('author_email')}>")
        logger.debug(f"  Message: {contents.get('message', '').splitlines()[0][:80]}...") # Log first line up to 80 chars
        logger.debug(f"  URL: {contents.get('html_url')}")

        # Default Bundle handler will write to cache based on normalized_event_type.
        # If you needed to modify contents *before* caching, you would return
        # the modified kobj here: return kobj

        # If you wanted to stop processing this specific KObj (e.g., based on content),
        # you could return STOP_CHAIN here: return STOP_CHAIN

        # Returning None passes the kobj unchanged to the next handler in the chain
        # (likely the default handler which performs the cache write)
        return None

    except Exception as e:
        logger.error(f"Error handling GithubCommit bundle {kobj.rid}: {e}", exc_info=True)
        # Decide if error should stop the pipeline for this KObj
        # return STOP_CHAIN
        return None # Continue processing despite handler error

# Add a NEW handler specifically to propose a GithubCommit edge to the coordinator
@node.processor.register_handler(HandlerType.Final, rid_types=[KoiNetNode])
def propose_github_commit_edge_to_coordinator(processor: ProcessorInterface, kobj: KnowledgeObject):
    # This handler runs after a NEW KoiNetNode is fully processed (cached, graph updated, default edges proposed)
    # It's in the Final phase, less intrusive to core pipeline flow.
    # Simplified logic: If we just processed a NEW KoiNetNode and it's the *only* other node in our graph besides ourselves,
    # assume it's the coordinator and propose the GithubCommit edge.
    if kobj.normalized_event_type != EventType.NEW:
        return
        
    known_peers = processor.network.graph.get_neighbors()
    if len(known_peers) == 1 and known_peers[0] == kobj.rid:
        logger.info(f"Assuming {kobj.rid} is the coordinator. Proposing WEBHOOK edge for GithubCommit events.")
        try:
            github_edge_bundle = generate_edge_bundle(
                source=node.identity.rid, # I am the source of these events
                target=kobj.rid,           # The coordinator is the target
                edge_type=EdgeType.WEBHOOK, # Use webhook
                rid_types=[GithubCommit]    # Specify GithubCommit events
            )
            # Queue this new edge bundle for processing
            processor.handle(bundle=github_edge_bundle)
        except Exception as e:
            logger.error(f"Failed to generate/handle GithubCommit edge bundle for {kobj.rid}: {e}", exc_info=True)

logger.info("GithubCommit Bundle handler and KoiNetNode handlers registered.")
