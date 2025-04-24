# coordinator_node/handlers/network.py
import logging
from rid_lib.types import KoiNetNode, KoiNetEdge
from koi_net.processor import ProcessorInterface
from koi_net.processor.handler import HandlerType
from koi_net.processor.knowledge_object import KnowledgeObject
from koi_net.protocol.event import Event, EventType
from koi_net.protocol.helpers import generate_edge_bundle
from koi_net.protocol.edge import EdgeType
from ..core import node

logger = logging.getLogger(__name__)

@node.processor.register_handler(HandlerType.Network, rid_types=[KoiNetNode])
def handshake_handler(proc: ProcessorInterface, kobj: KnowledgeObject):
    logger.info("Handling node handshake")

    if kobj.event_type != EventType.NEW:
        return

    logger.info("Sharing this node's bundle with peer")
    proc.network.push_event_to(
        event=Event.from_bundle(EventType.NEW, proc.identity.bundle),
        node=kobj.rid,
        flush=True
    )

    logger.info("Proposing new edge")
    edge_bundle = generate_edge_bundle(
        source=kobj.rid,
        target=proc.identity.rid,
        edge_type=EdgeType.WEBHOOK,
        rid_types=[KoiNetNode, KoiNetEdge]
    )
    proc.handle(rid=edge_bundle.rid, event_type=EventType.FORGET)
    proc.handle(bundle=edge_bundle)