def parse_block_expressions_from_string(source: str):
    if source is None:
        return list()

    lines = source.splitlines()
    return list(filter(lambda line: len(line) > 0, lines))
