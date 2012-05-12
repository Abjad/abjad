from abjad.tools.containertools.Container._ContainerFormatter import _ContainerFormatter
from abjad.tools.tuplettools.Tuplet._TupletFormatterSlotsInterface import _TupletFormatterSlotsInterface


class _TupletFormatter(_ContainerFormatter):

    def __init__(self, client):
        _ContainerFormatter.__init__(self, client)
        self.label = None
        self._slots = _TupletFormatterSlotsInterface(self)

    ### PUBLIC PROPERTIES ###

    @property
    def slots(self):
        return self._slots

    @property
    def tuplet(self):
        return self._client
