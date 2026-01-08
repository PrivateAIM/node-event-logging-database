import os


def get_env(env_name: str, default: str | None = None) -> str:
    value = os.getenv(env_name, default)

    if value is None:
        raise ValueError(f"Environment variable `{env_name}` is not set.")

    return value


def postgres_user():
    return get_env("POSTGRES_USER")


def postgres_password():
    return get_env("POSTGRES_PASSWORD")


def postgres_database():
    return get_env("POSTGRES_DB")


def postgres_host():
    return get_env("POSTGRES_HOST", "localhost")


def postgres_port():
    return get_env("POSTGRES_PORT", "5432")
