# import logging
# import os
# from app.utils.config import *
# import importlib.util

# # spec = importlib.util.find_spec("app")   # replace "app" with package name
# # if spec is None:
# #     print("NOT importable")
# # else:
# #     print("importable")
# #     print("origin:", spec.origin)
# #     print("is package:", bool(spec.submodule_search_locations))
# #     print("package search locations:", spec.submodule_search_locations)

# # spec = importlib.util.find_spec("app.utils.config")
# # if spec is None:
# #     print("NOT importable")
# # else:
# #     print("importable:", spec)
# #     # spec.origin, spec.loader, spec.submodule_search_locations are useful

# # def setup_logging():
# #     level = app_log_level()
# #     logging.basicConfig(
# #         level=level,
# #         format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
# #     )
# #     logging.getLogger(__name__).info("Logging initialized at %s", level)

# if __name__ == "__main__":
#     print("Current Root Dir :",os.getcwd())
#     setup_logging()
#     logger = logging.getLogger(__name__)
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")


# app/utils/logging.py
import logging
from app.utils.config import *
# from .config import app_log_level

def setup_logging():
    level = app_log_level()
    print()
    logging.basicConfig(
        level=level,
        format="%(asctime)15s -:-%(levelname)8s-:- %(name)s -:- %(message)s",
    )
    logging.getLogger(__name__).info("Logging initialized at %s", level)


if __name__ == "__main__":
    print("Current Root Dir :",os.getcwd())
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
