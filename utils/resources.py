RESOURCES_FOLDER = "res/"


def resources(path: str) -> str:
    if path[0] == "/":
        path = path[1:]

    return RESOURCES_FOLDER + path
