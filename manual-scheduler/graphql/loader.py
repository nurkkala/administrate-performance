from functools import cache


@cache
def load_graphql(name: str) -> str:
    with open(f"./graphql/{name}.graphql") as f:
        return f.read()
