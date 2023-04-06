from functools import cache

from devtools import debug


@cache
def load_fragments() -> str:
    with open(f"./graphql/fragments.graphql") as f:
        return f.read()


@cache
def load_graphql(name: str) -> str:
    fragments = load_fragments()
    with open(f"./graphql/{name}.graphql") as f:
        result = "\n".join([fragments, f.read()])
        return result
