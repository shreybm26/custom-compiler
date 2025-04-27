# utils.py
def get_token_stream(path):
    tokens = []
    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                tokens.append((parts[0], parts[1]))
            else:
                tokens.append((parts[0], None))
    return tokens
