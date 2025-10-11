#Add Root path to sys.path for imports to work when running this test directly
import logging,sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.utils.logging import setup_logging

log_file = setup_logging()
logger = logging.getLogger(__name__)
logger.debug("This is a debug message")

# Ensure handlers flush to disk
logging.shutdown()

print("Wrote to:", log_file)