import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """Initializes a standard corporate-formatted production log stream."""
    logger = logging.getLogger(name)
    
    # Prevent adding duplicate handlers if initialized across multiple modules
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.propagate = False
        
    return logger
