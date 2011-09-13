from abjad.tools.containertools.Container.Container import _ContainerFormatter
from abjad.tools.contexttools._Context._ContextFormatterSlotsInterface import _ContextFormatterSlotsInterface


class _ContextFormatter(_ContainerFormatter):

    def __init__(self, client):
        _ContainerFormatter.__init__(self, client)
        self._slots = _ContextFormatterSlotsInterface(self)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_engraver_consists(self):
        result = []
        for engraver in sorted(self.context.engraver_consists):
            result.append(r'\consists %s' % engraver)
        return result

    @property
    def _formatted_engraver_removals(self):
        result = []
        for engraver in sorted(self.context.engraver_removals):
            result.append(r'\remove %s' % engraver)
        return result

    @property
    def _invocation(self):
        client = self._client
        if client.name is not None:
            return r'\context %s = "%s"' % (client.context, client.name)
        else:
            return r'\new %s' % client.context

    ### PUBLIC ATTRIBUTES ###

    @property
    def context(self):
        return self._client

    @property
    def slots(self):
        return self._slots
