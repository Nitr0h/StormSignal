import psutil


def is_fortnite_running() -> bool:
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == "FortniteClient-Win64-Shipping.exe":
            return True

    return False
