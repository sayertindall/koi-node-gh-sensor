from .core import node
from .handlers import network  # add more handlers as needed

def register_handlers():
    print("Registering COORDINATOR handlers...")
    # Trigger module-level handler registration
    _ = network