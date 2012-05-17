from abjad.interfaces._Interface import _Interface


class _NavigationInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PRIVATE PROPERTIES ###

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
