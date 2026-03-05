"""Authentication helpers for PRAW Reddit instances."""

import configparser
import praw


def load_config(config_path="config.ini"):
    """Load configuration from INI file."""
    config = configparser.ConfigParser()
    files_read = config.read(config_path)
    if not files_read:
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Copy config.example.ini to config.ini and fill in your credentials."
        )
    return config


def get_reddit_instance(config, section):
    """Create an authenticated PRAW Reddit instance from a config section."""
    return praw.Reddit(
        client_id=config[section]["client_id"],
        client_secret=config[section]["client_secret"],
        username=config[section]["username"],
        password=config[section]["password"],
        user_agent=config[section]["user_agent"],
    )


def get_source(config_path="config.ini"):
    """Return an authenticated Reddit instance for the source account."""
    config = load_config(config_path)
    return get_reddit_instance(config, "source")


def get_target(config_path="config.ini"):
    """Return an authenticated Reddit instance for the target account."""
    config = load_config(config_path)
    return get_reddit_instance(config, "target")
