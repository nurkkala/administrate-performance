from devtools import debug

from data.small import single_plan


def traverse_and_duplicate(obj):
    if isinstance(obj, dict):
        rtn = {}
        for key, val in obj.items():
            rtn[key] = traverse_and_duplicate(val)
        return rtn
    elif isinstance(obj, list):
        rtn = []
        for val in obj:
            rtn.append(traverse_and_duplicate(val))
        return rtn
    else:
        return obj


def unwrap_edge(obj):
    assert isinstance(obj, list)
    rtn = []
    for val in obj:
        assert isinstance(val, dict)
        rtn.append(traverse(val['node']))
    return rtn


def traverse(obj):
    if isinstance(obj, dict):
        if 'edges' in obj:
            assert len(obj) == 1
            return unwrap_edge(obj['edges'])
        else:
            rtn = {}
            for key, val in obj.items():
                rtn[key] = traverse(val)
            return rtn
    elif isinstance(obj, list):
        rtn = []
        for val in obj:
            rtn.append(traverse(val))
        return rtn
    else:
        return obj


if __name__ == '__main__':
    debug(traverse(single_plan))
    # traverse_and_filter(single_plan)
