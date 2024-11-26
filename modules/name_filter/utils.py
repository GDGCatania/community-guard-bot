def parse_block_expressions_from_string(source: str):
    lines = source.splitlines()
    return list(filter(lambda line: len(line) > 0, lines))
