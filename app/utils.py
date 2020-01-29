import os


def env(env_var: str, default=None):
    try:
        value = os.environ[env_var]
        return value
    except KeyError:
        if default is not None:
            return default

        raise KeyError(f"You have to specify the environment variable {env_var}")
