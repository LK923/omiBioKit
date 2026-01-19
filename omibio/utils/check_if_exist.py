def check_if_exist(string: str | None, default: str = "N/A") -> str:
    if not string:
        return default
    return string
