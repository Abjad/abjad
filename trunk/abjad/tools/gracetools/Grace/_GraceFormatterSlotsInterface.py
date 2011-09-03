from abjad.tools.containertools.Container._ContainerFormatterSlotsInterface import _ContainerFormatterSlotsInterface


class _GraceFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

    def __init__(self, client):
        _ContainerFormatterSlotsInterface.__init__(self, client)

    ### PUBLIC ATTRIBUTES ###

    @property
    def slot_2(self):
        result = []
        grace = self.formatter.grace
        kind = grace.kind
        if kind == 'after':
            #result.append(self.wrap(grace.brackets, 'open'))
            result.append([('grace_brackets', 'open'), ['{']])
        else:
            #contributor = (grace.brackets, 'open')
            #contributions = [r'\%s %s' % (kind, grace.brackets.open[0])]
            contributor = ('grace_brackets', 'open')
            contributions = [r'\%s {' % kind]
            result.append([contributor, contributions])
        return tuple(result)
