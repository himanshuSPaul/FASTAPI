from app.utils.logging import setup_logging
import logging

# Ensure you run this from project root so `app` is importable
log_file = setup_logging()
logger = logging.getLogger("test.run")
logger.info("This is a test message from scripts/test_looging_run.py")

# Ensure handlers flush to disk
logging.shutdown()

print("Wrote to:", log_file)