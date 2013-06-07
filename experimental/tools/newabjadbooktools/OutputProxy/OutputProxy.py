from abjad.tools.abctools import AbjadObject


class OutputProxy(AbjadObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload
        
    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def payload(self):
        return self._payload
