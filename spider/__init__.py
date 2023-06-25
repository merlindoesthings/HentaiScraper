import toml

def string_format(string: str):
    characters = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "{",
        "}",
        "\\",
        ";",
        ":",
        "'",
        '"',
        "<",
        ">",
        ",",
        ".",
        "/",
        "?",
        "-",
        "=",
        "_",
        "`",
        "|"
    ]

    for char in characters:
        if char in string:
            string = string.replace(char, "")
            
    return string

class Parser:
    def __init__(self):
        self.FILE = "settings.toml"

    def read_file(self):
        data = toml.load(self.FILE)
            
        return data
