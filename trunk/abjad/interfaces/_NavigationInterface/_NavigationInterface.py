from abjad.interfaces._Interface import _Interface


class _NavigationInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PRIVATE PROPERTIES ###

    @property
    def _next(self):
        '''Returns next component in temporal order.
        '''
        from abjad.tools import componenttools
        for component in componenttools.get_improper_parentage_of_component(self._client):
            next_sibling = component._navigator._next_sibling
            if next_sibling is not None:
                return next_sibling

    @property
    def _next_bead(self):
        '''Returns the next bead (time-threaded leaf), if such exists.
        This method will search the whole (parentage) structure moving forward.
        This will only return if called on a leaf.
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
        '''Find the next component of the same type and with the same parentage signature.
        '''
        from abjad.tools import componenttools
        next = self._next
        if next is None:
            return
        dfs = componenttools.iterate_components_depth_first(next, capped=False)
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    @property
    def _next_sibling(self):
        '''Returns the next sequential element in the caller's parent, otherwise none.
        '''
        from abjad.tools import componenttools
        return componenttools.get_nth_sibling_from_component(self._client, 1)

    @property
    def _prev(self):
        '''Returns previous component in temporal order.
        '''
        from abjad.tools import componenttools
        for component in componenttools.get_improper_parentage_of_component(self._client):
            prev_sibling = component._navigator._prev_sibling
            if prev_sibling is not None:
                return prev_sibling

    @property
    def _prev_bead(self):
        '''Returns the previous bead (time-threaded leaf), if such exists.
        This method will search the whole (parentage) structure moving back.
        This will only return if called on a leaf.
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
    def _prev_sibling(self):
        '''Returns the previous sequential element in the caller's parent, otherwise none.
        '''
        from abjad.tools import componenttools
        return componenttools.get_nth_sibling_from_component(self._client, -1)

    ### PRIVATE METHODS ###

    def _find_fellow_bead(self, candidates):
        '''Helper method for prev_bead() and next_bead().
        Given a list of bead candiates of self, find and return the first one
        that matches thread parentage.
        '''
        for candidate in candidates:
            if self._is_threadable(candidate):
                return candidate

    def _get_immediate_temporal_successors(self):
        '''Return list of components immediately after client.
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
        '''True when client follows immediately after expr, otherwise false.
        '''
        return expr in self._get_immediate_temporal_successors()

    def _is_threadable(self, expr):
        '''Check if expr is threadable with respect to client.
        '''
        from abjad.tools import componenttools
        return componenttools.all_are_components_in_same_thread([self._client, expr])
