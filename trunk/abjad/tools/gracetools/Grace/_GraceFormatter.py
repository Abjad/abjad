from abjad.tools.containertools.Container._ContainerFormatter import _ContainerFormatter
from abjad.tools.gracetools.Grace._GraceFormatterSlotsInterface import _GraceFormatterSlotsInterface


class _GraceFormatter(_ContainerFormatter):

    def __init__(self, client):
        _ContainerFormatter.__init__(self, client)
        self._slots = _GraceFormatterSlotsInterface(self)

    ### PUBLIC ATTRIBUTES ###

    @property
    def grace(self):
        return self._client

    @property
    def slots(self):
        return self._slots
