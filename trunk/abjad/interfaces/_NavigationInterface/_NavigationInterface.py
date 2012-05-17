from abjad.interfaces._Interface import _Interface
import collections


class _NavigationInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PRIVATE PROPERTIES ###

    @property
    def _next(self):
        '''Returns next Component in temporal order.
        '''
        from abjad.tools import componenttools
        next = self._next_sibling
        if next is not None:
            return next
        else:
            for p in componenttools.get_proper_parentage_of_component(self._client):
                next = p._navigator._next_sibling
                if next is not None:
                    return next

    @property
    def _next_bead(self):
        '''Returns the next Bead (time threaded Leaf), if such exists.
        This method will search the whole (parentage) structure
        moving forward.
        This will only return if called on a Leaf.
        '''
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        if not isinstance(self._client, leaftools.Leaf):
            return
        next = self._next
        if next is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_start_with_component(next)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        return self._find_fellow_bead(candidates)

    @property
    def _next_namesake(self):
        '''Find the next Component of the same type and with the same
        parentage signature.
        '''
        from abjad.tools import componenttools
        next = self._next
        if next is None:
            return
        dfs = componenttools.iterate_components_depth_first(next, capped = False)
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    # TODO: Write tests for _NavigationInterface._prev_namesake.
    #       Backwards depth first search has always had a bug that needs fixing.
    @property
    def _prev_namesake(self):
        '''Find the prev component of same type and parentage signature.
        '''
        from abjad.tools import componenttools
        prev = self._prev
        if prev is None:
            return
        dfs = componenttools.iterate_components_depth_first(prev, capped=False, direction='right')
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    @property
    def _next_sibling(self):
        '''Returns the next sequential element in the caller's parent;
        None otherwise.
        '''
        rank = self._rank()
        #if (not rank is None) and (not self._client._parentage.parent.is_parallel):
        if rank is not None and not self._client.parent.is_parallel:
            if rank + 1 < len(self._client._parentage.parent._music):
                return self._client._parentage.parent._music[rank + 1]

    @property
    def _next_thread(self):
        '''Returns the next threadable Container.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        from abjad.tools import leaftools
        if not isinstance(self._client, containertools.Container):
            return
        next = self._next
        if next is None or isinstance(next, leaftools.Leaf):
            return
        containers = componenttools.get_component_lineage_that_start_with_component(next)
        for container in containers:
            if self._is_threadable(container):
                return container

    @property
    def _prev(self):
        '''Returns previous Component in temporal order.
        '''
        from abjad.tools import componenttools
        prev = self._prev_sibling
        if prev is not None:
            return prev
        else:
            for parent in componenttools.get_proper_parentage_of_component(self._client):
                prev = parent._navigator._prev_sibling
                if prev is not None:
                    return prev

    @property
    def _prev_bead(self):
        '''Returns the previous Bead (time threaded Leaf), if such exists.
        This method will search the whole (parentage) structure moving back.
        This will only return if called on a Leaf.
        '''
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        if not isinstance(self._client, leaftools.Leaf):
            return
        prev = self._prev
        if prev is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_stop_with_component(prev)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        return self._find_fellow_bead(candidates)

    @property
    def _prev_sibling(self):
        '''Returns the previous sequential element in the caller's parent;
        None otherwise.
        '''
        rank = self._rank()
        if rank is not None and not self._client._parentage.parent.is_parallel:
            if 0 <= rank - 1:
                return self._client._parentage.parent._music[rank - 1]
        else:
            return

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
        from abjad.tools import componenttools
        cur = self._client
        while cur is not None:
            next_sibling = cur._navigator._next_sibling
            if next_sibling is None:
                cur = cur._parentage.parent
            else:
                return componenttools.get_improper_descendents_of_component_that_start_with_component(
                    next_sibling)
        return []

    def _is_immediate_temporal_successor_of(self, expr):
        '''True when client follows immediately after expr,
        otherwise False.
        '''
        return expr in self._get_immediate_temporal_successors()

    def _is_threadable(self, expr):
        '''Check if expr is threadable with respect to self.
        '''
        from abjad.tools import componenttools
        return componenttools.all_are_components_in_same_thread([self._client, expr])

    # TODO: Move _NavigationInterface._rank to Parentage._rank
    def _rank(self):
        '''Returns the index of the caller (its position) in
        the parent container. If caller has no parent,
        returns None.
        '''
        parent = self._client._parentage.parent
        if parent is not None:
            return parent.index(self._client)
