from abjad.interfaces._Interface import _Interface


class _NavigationInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PRIVATE PROPERTIES ###

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
        next_component = componenttools.get_nth_component_in_time_order_from_component(self._client, 1)
        if next_component is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_start_with_component(
            next_component)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if componenttools.all_are_components_in_same_thread([self._client, candidate]):
                return candidate

    @property
    def _next_namesake(self):
        '''Find the next component of the same type and with the same parentage signature.
        '''
        from abjad.tools import componenttools
        next_component = componenttools.get_nth_component_in_time_order_from_component(self._client, 1)
        if next_component is None:
            return
        dfs = componenttools.iterate_components_depth_first(next_component, capped=False)
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

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
        prev = componenttools.get_nth_component_in_time_order_from_component(self._client, -1)
        if prev is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_stop_with_component(prev)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if componenttools.all_are_components_in_same_thread([self._client, candidate]):
                return candidate

    # TODO: Write tests for _NavigationInterface._prev_namesake.
    #       Backwards depth first search has always had a bug that needs fixing.
    @property
    def _prev_namesake(self):
        '''Find the prev component of same type and parentage signature.
        '''
        from abjad.tools import componenttools
        prev = componenttools.get_nth_component_in_time_order_from_component(self._client, -1)
        if prev is None:
            return
        dfs = componenttools.iterate_components_depth_first(prev, capped=False, direction='right')
        for node in dfs:
            if type(node) == type(self._client) and \
                componenttools.component_to_parentage_signature(node) == \
                componenttools.component_to_parentage_signature(self._client):
                return node

    ### PRIVATE METHODS ###

    def _get_immediate_temporal_successors(self):
        '''Return list of components immediately after client.
        '''
        from abjad.tools import componenttools
        cur = self._client
        while cur is not None:
            next_sibling = componenttools.get_nth_sibling_from_component(cur, 1)
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
