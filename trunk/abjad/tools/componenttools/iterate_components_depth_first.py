import collections


def iterate_components_depth_first(component, capped=True, unique=True,
    forbid=None, direction='left'):
    '''.. versionadded:: 1.1

    Iterate components depth-first from `component`.

    .. todo:: Add usage examples.

    .. versionchanged:: 2.0
        renamed ``iterate.depth_first()`` to
        ``componenttools.iterate_components_depth_first()``.
    '''

    client_parent, node, rank = component._parentage.parent, component, 0
    queue = collections.deque([])
    while node is not None and not (capped and node is client_parent):
        result = _find_yield(node, rank, queue, unique)
        if result is not None:
            yield result
        if _is_node_forbidden(node, forbid):
            node, rank = _handle_forbidden_node(node, queue)
        else:
            node, rank = _advance_node_depth_first(node, rank, direction)
    queue.clear()

def _next_node_depth_first(component, total):
    '''If client has unvisited music, return next unvisited node in client's music.

    If client has no univisited music and has a parent, return client's parent.

    If client has no univisited music and no parent, return None.
    '''

    client = component
    if hasattr(client, '_music') and 0 < len(client) and total < len(client):
        return client[total], 0
    else:
        parent = client._parentage.parent
        if parent is not None:
            return parent, parent.index(client) + 1
        else:
            return None, None

def _prev_node_depth_first(component, total=0):
    '''If client has unvisited music, return prev unvisited node in client's music.

    If client has no univisited music and has a parent, return client's parent.

    If client has no univisited music and no parent, return None.
    '''

    client = component
    if hasattr(client, '_music') and 0 < len(client) and total < len(client):
        return client[len(client) - 1 - total], 0
    else:
        parent = client._parentage.parent
        if parent is not None:
            return parent, len(parent) - parent.index(client)
        else:
            return None, None

def _handle_forbidden_node(node, queue):
    node_parent = node._parentage.parent
    if node_parent is not None:
        rank = node_parent.index(node) + 1
        node = node_parent
    else:
        node, rank = None, None
    queue.pop()
    return node, rank

def _advance_node_depth_first(node, rank, direction):
    if direction == 'left':
        node, rank = _next_node_depth_first(node, rank)
    else:
        node, rank = _prev_node_depth_first(node, rank)
    return node, rank

def _is_node_forbidden(node, forbid):
    if forbid is None:
        return False
    elif forbid == 'parallel':
        return getattr(node, 'is_parallel', False)
    else:
        return isinstance(node, forbid)

def _find_yield(node, rank, queue, unique):
    if hasattr(node, '_music'):
        try:
            visited = node is queue[-1]
        except IndexError:
            visited = False
        if not visited or unique is not True:
            queue.append(node)
            return node
        elif rank == len(node):
            queue.pop()
            return None
    else:
        return node
