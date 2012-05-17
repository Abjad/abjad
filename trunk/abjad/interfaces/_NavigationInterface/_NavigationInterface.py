from abjad.interfaces._Interface import _Interface


class _NavigationInterface(_Interface):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client
