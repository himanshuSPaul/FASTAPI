# app/utils/logging.py
import logging
import inspect
import os
from pathlib import Path
from app.utils.config import _root_dir, app_log_level, app_name
from datetime import datetime


def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_level = app_log_level()
    logs_dir = _root_dir() / "logs"
    log_file = str(logs_dir / f"{app_name()}_{timestamp}.log")
    logs_dir.mkdir(parents=True, exist_ok=True)
    # Use logger name once (%(name)s). Removed duplicate %(module)s which caused repeated "looging -:- looging" output
    log_format = "%(asctime)s -:- %(levelname)s -:- %(name)s -:- %(message)s"
    formatter = logging.Formatter(log_format)
    stream_hdl = logging.StreamHandler()
    stream_hdl.setFormatter(formatter)
    file_hdl = logging.FileHandler(log_file, encoding="utf-8")
    file_hdl.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(stream_hdl)
    root.addHandler(file_hdl)
    # Log the initialization message using the caller's module logger so the log shows who called setup_logging()
    try:
        caller_frame = inspect.stack()[1][0]
        caller_module = inspect.getmodule(caller_frame)

        # If the caller module has a proper name (not '__main__'), use it directly.
        if caller_module is not None and getattr(caller_module, "__name__", None) not in (None, "__main__"):
            caller_name = caller_module.__name__
        else:
            # When the caller is executed as a script, __name__ is '__main__'. Derive a dotted module path
            # from the caller file relative to the project root (e.g. 'tests.test_looging_run').
            try:
                caller_file = caller_frame.f_code.co_filename
                caller_path = Path(caller_file).resolve()
                root = _root_dir()
                caller_name = str(caller_path.relative_to(root).with_suffix("")).replace(os.sep, ".")
            except Exception:
                caller_name = caller_module.__name__ if caller_module is not None else __name__
    except Exception:
        caller_name = __name__

    logging.getLogger(caller_name).info("Logging initialized at %s, file=%s", log_level, log_file)
    return log_file



    # print()
    # logging.basicConfig(
    #     level=level,
    #     format=,
    # )
    # logging.getLogger(__name__).info("Logging initialized at %s", level)


if __name__ == "__main__":
    # print("Current Root Dir :",os.getcwd())
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
