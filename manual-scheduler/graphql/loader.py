import collections
import re
from functools import cache
from typing import Deque, Set, List


@cache
def load_graphql(name: str) -> str:
    file_name_queue: Deque[str] = collections.deque()
    file_name_queue.appendleft(f"./graphql/{name}.graphql")
    closed: Set[str] = set()
    result: List[str] = []
    fragment_pattern = re.compile(r"^\s*\.\.\.(\S+)\n$")

    while len(file_name_queue) > 0:
        file_name = file_name_queue.pop()
        if file_name in closed:
            continue
        result.extend(["\n", f"# {file_name}", "\n"])
        with open(file_name) as f:
            for line in f:
                result.append(line)
                match = fragment_pattern.match(line)
                if match is not None:
                    file_name_queue.appendleft(f"./graphql/fragments/{match[1]}.graphql")
        closed.add(file_name)
    return "".join(result)


if __name__ == '__main__':
    print(load_graphql("getPlansList"))
