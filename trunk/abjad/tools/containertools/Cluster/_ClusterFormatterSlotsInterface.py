from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface


class _ClusterFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

    def __init__(self, client):
        _ContainerFormatterSlotsInterface.__init__(self, client)

    ### PUBLIC ATTRIBUTES ###

    @property
    def slot_2(self):
        result = []
        cluster = self.formatter.cluster
        contributor = ('cluster_brackets', 'open')
        if self._client._client.is_parallel:
            brackets_open = ['<<']
        else:
            brackets_open = ['{']
        contributions = [r'\makeClusters %s' % brackets_open[0]]
        result.append([contributor, contributions])
        return tuple(result)
