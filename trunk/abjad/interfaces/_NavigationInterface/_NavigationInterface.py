from abjad.interfaces._Interface import _Interface
import collections


class _NavigationInterface(_Interface):

    __slots__ = ( )

    def __init__(self, client):
        self._client = client

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contemporaneous_start_components(self):
        '''Return a list of all components in either the contents or
        parentage of client starting at the same moment as client,
        including client.
        '''
        result = [ ]
        result.extend(self._contemporaneous_start_contents)
        result.extend(self._contemporaneous_start_parentage)
        return list(set(result))

    @property
    def _contemporaneous_start_contents(self):
        '''Return a list of all components in the contents of client
        starting at the same moment as client, including client.
        '''
        from abjad.tools.containertools.Container import Container
        result = [ ]
        client = self._client
        result.append(client)
        if isinstance(client, Container):
            if client.is_parallel:
                for x in client:
                    result.extend(x._navigator._contemporaneous_start_contents)
            elif len(client):
                result.extend(client[0]._navigator._contemporaneous_start_contents)
        return result

    @property
    def _contemporaneous_start_parentage(self):
        '''Return a list of all components in the parentage of client
        starting at the same moment as client, including client.
        '''
        from abjad.tools import componenttools
        client = self._client
        result = [client]
        prev = client
        for parent in componenttools.get_proper_parentage_of_component(client):
            if parent.is_parallel:
                result.append(parent)
            elif parent.index(prev) == 0:
                result.append(parent)
            prev = parent
        return result

    @property
    def _contemporaneous_stop_components(self):
        '''Return a list of all components in either the contents or
        parentage of client stopping at the same moment as client,
        including client.
        '''
        result = [ ]
        result.extend(self._contemporaneous_stop_contents)
        result.extend(self._contemporaneous_stop_parentage)
        return list(set(result))

    @property
    def _contemporaneous_stop_contents(self):
        '''Return a list of all components in the contents of client
        stopping at the same moment as client, including client.
        '''
        from abjad.tools.containertools.Container import Container
        result = [ ]
        client = self._client
        result.append(client)
        if isinstance(client, Container):
            if client.is_parallel:
                client_duration = client.preprolated_duration
                for x in client:
                    if x.preprolated_duration == client_duration:
                        result.extend(x._navigator._contemporaneous_stop_contents)
            elif len(client):
                result.extend(client[-1]._navigator._contemporaneous_stop_contents)
        return result

    @property
    def _contemporaneous_stop_parentage(self):
        '''Return a list of all components in the parentage of client
        stopping at the same moment as client, including client.
        '''
        from abjad.tools import componenttools
        client = self._client
        result = [client]
        prev = client
        for parent in componenttools.get_proper_parentage_of_component(client):
            if parent.is_parallel:
                if prev.prolated_duration == parent.prolated_duration:
                    result.append(parent)
                else:
                    break
            elif parent.index(prev) == len(parent) - 1:
                result.append(parent)
            prev = parent
        return result

    @property
    def _first_leaves(self):
        '''Returns the first (leftmost) leaf or leaves
        (in case there's a parallel structure) in a tree.
        '''
        from abjad.tools.containertools.Container import Container
        from abjad.tools.leaftools._Leaf import _Leaf
        client = self._client
        if isinstance(client, _Leaf):
            return [client]
        elif isinstance(client, Container):
            leaves = [ ]
            if self._client.is_parallel:
                for e in self._client:
                    leaves.extend(e._navigator._first_leaves)
            elif len(self._client):
                leaves.extend(self._client[0]._navigator._first_leaves)
            else:
                return [ ]
            return leaves

    @property
    def _last_leaves(self):
        '''Returns the last (rightmost) leaf or leaves
        (in case there's a parallel structure) in a tree.
        '''
        from abjad.tools.containertools.Container import Container
        from abjad.tools.leaftools._Leaf import _Leaf
        client = self._client
        if isinstance(client, _Leaf):
            return [client]
        elif isinstance(client, Container):
            leaves = [ ]
            if self._client.is_parallel:
                for e in self._client:
                    leaves.extend(e._navigator._last_leaves)
            elif len(self._client):
                leaves.extend(self._client[-1]._navigator._last_leaves)
            else:
                return [ ]
            return leaves

    @property
    def _next(self):
        '''Returns next Component in temporal order.
        '''
        from abjad.tools import componenttools
        next = self._next_sibling
        if next:
            return next
        else:
            for p in componenttools.get_proper_parentage_of_component(self._client):
                next = p._navigator._next_sibling
                if next:
                    return next

    @property
    def _next_bead(self):
        '''Returns the next Bead (time threaded Leaf), if such exists.
        This method will search the whole (parentage) structure
        moving forward.
        This will only return if called on a Leaf.
        '''
        from abjad.tools.leaftools._Leaf import _Leaf
        if not isinstance(self._client, _Leaf):
            return None
        next = self._next
        if next is None:
            return None
        candidates = next._navigator._first_leaves
        return self._find_fellow_bead(candidates)

    @property
    def _next_namesake(self):
        '''Find the next Component of the same type and with the same
        parentage signature.
        '''
        from abjad.tools import componenttools
        next = self._next
        if next is None:
            return None
        dfs = componenttools.iterate_components_depth_first(next, capped = False)
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    # TODO: Write tests for _NavigationInterface._prev_namesake.                                    #
    #         Backwards depth first search has always had a bug that needs fixing. #

    @property
    def _prev_namesake(self):
        '''Find the prev component of same type and parentage signature.
        '''
        from abjad.tools import componenttools
        prev = self._prev
        if prev is None:
            return None
        dfs = componenttools.iterate_components_depth_first(prev, capped = False, direction = 'right')
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    @property
    def _next_sibling(self):
        '''Returns the next *sequential* element in the caller's parent;
        None otherwise.
        '''
        rank = self._rank( )
        if (not rank is None) and (not self._client._parentage.parent.is_parallel):
            if rank + 1 < len(self._client._parentage.parent._music):
                return self._client._parentage.parent._music[rank + 1]
        else:
            return None

    @property
    def _next_thread(self):
        '''Returns the next threadable Container.
        '''
        from abjad.tools.containertools.Container import Container
        from abjad.tools.leaftools._Leaf import _Leaf
        if not isinstance(self._client, Container):
            return None
        next = self._next
        if next is None or isinstance(next, _Leaf):
            return None
        containers = next._navigator._contemporaneous_start_components
        for c in containers:
            if self._is_threadable(c):
                return c

    @property
    def _prev(self):
        '''Returns previous Component in temporal order.
        '''
        from abjad.tools import componenttools
        prev = self._prev_sibling
        if prev:
            return prev
        else:
            for p in componenttools.get_proper_parentage_of_component(self._client):
                prev = p._navigator._prev_sibling
                if prev:
                    return prev

    @property
    def _prev_bead(self):
        '''Returns the previous Bead (time threaded Leaf), if such exists.
        This method will search the whole (parentage) structure moving back.
        This will only return if called on a Leaf.
        '''
        from abjad.tools.leaftools._Leaf import _Leaf
        if not isinstance(self._client, _Leaf):
            return None
        prev = self._prev
        if prev is None:
            return None
        candidates = prev._navigator._last_leaves
        return self._find_fellow_bead(candidates)

    @property
    def _prev_sibling(self):
        '''Returns the previous *sequential* element in the caller's parent;
        None otherwise.
        '''
        rank = self._rank( )
        if (not rank is None) and (not self._client._parentage.parent.is_parallel):
            if 0 <= rank - 1:
                return self._client._parentage.parent._music[rank - 1]
        else:
            return None

    ### PRIVATE METHODS ###

    def _advance(self, rank):
        '''Advance to self._client._music[rank], if possible,
        otherwise ascend.
        '''
        if hasattr(self._client, '_music'):
            if rank < len(self._client._music):
                return self._client._music[rank]
            else:
                return self._client.parentge.parent
        else:
            return self._client._parentage.parent

    def _find_fellow_bead(self, candidates):
        '''Helper method from prev_bead and next_bead.
        Given a list of bead candiates of self, find and return the first one
        that matches thread parentage.
        '''
        for candidate in candidates:
            if self._is_threadable(candidate):
                return candidate

    def _get_immediate_temporal_successors(self):
        '''Return Python list of components immediately after self._client.
        '''
        cur = self._client
        while cur is not None:
            next_sibling = cur._navigator._next_sibling
            if next_sibling is None:
                cur = cur._parentage.parent
            else:
                return next_sibling._navigator._contemporaneous_start_contents
        return [ ]

    def _is_immediate_temporal_successor_of(self, expr):
        '''True when client follows immediately after expr,
        otherwise False.
        '''
        return expr in self._get_immediate_temporal_successors( )

    def _is_threadable(self, expr):
        '''Check if expr is threadable with respect to self.
        '''
        from abjad.tools import componenttools
        return componenttools.all_are_components_in_same_thread([self._client, expr])

    # TODO: Move _NavigationInterface._rank to Parentage._rank #

    def _rank(self):
        '''Returns the index of the caller (its position) in
        the parent container. If caller has no parent,
        returns None.
        '''
        parent = self._client._parentage.parent
        if parent is not None:
            return parent.index(self._client)
        else:
            return None

    def _traverse(self, v, depthFirst=True, leftRight=True):
        '''Traverse with visitor visiting each node in turn.
        '''
        if depthFirst:
            self._traverse_depth_first(v)
        else:
            self._traverse_breadth_first(v, leftRight)

    def _traverse_breadth_first(self, v, leftRight = True):
        '''Traverse breadth-first with visitor visiting each node.
        '''
        queue = collections.deque([self._client])
        while queue:
            node = queue.popleft( )
            if hasattr(v, 'visit'):
                v.visit(node)
            elif hasattr(v, '_visit'):
                v._visit(node)
            if hasattr(node, '_music'):
                if leftRight:
                    queue.extend(node._music)
                else:
                    queue.extend(reversed(node._music))

    def _traverse_depth_first(self, v):
        '''Traverse depth-frist with visitor visiting each node.
        '''
        if hasattr(v, 'visit'):
            v.visit(self._client)
        elif hasatr(v, '_visit'):
            v._visit(self._client)
        if hasattr(self._client, '_music'):
            for m in self._client._music:
                m._navigator._traverse(v)
        if hasattr(v, 'unvisit'):
            v.unvisit(self._client)
        elif hasattr(v, '_unvisit'):
            v._unvisit(self._client)
