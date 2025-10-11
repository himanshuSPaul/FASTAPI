# app/utils/config.py
from __future__ import annotations
import os
from pathlib import Path
from configparser import ConfigParser

_CONFIG: ConfigParser | None = None


def _root_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_config_path() -> Path:
    # Config File will be in project_root/config/config.ini (relative to this file)
    config_dir = _root_dir() / "config"
    config_file = config_dir / "config.ini"
    return config_file

def _load_config() -> ConfigParser:
    conf = ConfigParser()
    read_ok = conf.read(_default_config_path())
    if not read_ok:
        raise FileNotFoundError(f"Could not read configuration.ini at: {_default_config_path()}")
    return conf

def get_config() -> ConfigParser:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _load_config()
    return _CONFIG

# # --------- Convenience accessors ---------
def app_log_level() -> str:
    return get_config().get("app", "log_level", fallback="INFO").upper()

def app_name() -> str:
    return get_config().get("app", "application_name", fallback="Not Found In Config File")

def db_settings() -> dict:
    cfg = get_config()
    return {
        "host": cfg.get("database", "host", fallback="127.0.0.1"),
        "name": cfg.get("database", "name", fallback="inv_db"),
        "user": cfg.get("database", "user", fallback="inv_user"),
        "password": cfg.get("database", "password", fallback="inv_pass"),
        "port": cfg.getint("database", "port", fallback=5432),
        "minconn": cfg.getint("database", "min_conn", fallback=1),
        "maxconn": cfg.getint("database", "max_conn", fallback=10),
        "connect_timeout": cfg.getint("database", "connect_timeout", fallback=5),
    }


def main(argv: list[str] | None = None) -> int:
    """Simple CLI to exercise the config accessors.
    
    Usage:
        python app/utils/config.py 
    
    Description :
        Test the config file  accessors from command line.

    """
    try:
        print("Config File Path :", _default_config_path())
        print("ConfigFile Exists :", _default_config_path().is_file())
        if not _default_config_path().is_file():
            raise FileNotFoundError(f"Config file does not exist at: {_default_config_path()}")

        print("Avaialbel Section in Config File :", get_config().sections())
        print("Application Name:", app_name())

    except FileNotFoundError as exc:
        print("Error loading configuration:", exc)
        return 2    




    # parser = argparse.ArgumentParser(description="Test app.utils.config")
    # parser.add_argument("-c", "--config", help="Path to an .ini configuration file")
    # args = parser.parse_args(argv)

    # if args.config:
    #     os.environ["APP_CONFIG"] = args.config
    #     # reset cached config so the new file is read
    #     global _CONFIG
    #     _CONFIG = None

    # try:
    #     print("os.getenv('APP_CONFIG') :", os.getenv("APP_CONFIG"))
    #     print("Config file exists:", Path(os.getenv("APP_CONFIG") or _default_config_path()).is_file())
    #     print("_default_config_path() :", _default_config_path() )
    #     print("Configuration path:", os.getenv("APP_CONFIG") or _default_config_path())
    #     print("application_name:", app_name())
    #     print("log_level:", app_log_level())
    #     print("database settings:")
    #     pprint(db_settings())
    # except FileNotFoundError as exc:
    #     print("Error loading configuration:", exc)
    #     return 2
    _default_config_path()
    _load_config()
    db_settings()

    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
