from abjad.interfaces._Interface import _Interface


class _ComponentFormatterSlotsInterface(_Interface):

    __slots__ = ()

    def __init__(self, client):
        _Interface.__init__(self, client)

    ### PRIVATE METHODS ###

    def _format_contributor_name(self, contributor):
        '''Formater contributor name.'''
        result = []
        for part in contributor:
            if isinstance(part, str):
                result.append(part)
            else:
                result.append(part.__class__.__name__)
        result = '.'.join(result)
        return result

    def _format_slot(self, label, slot,
        verbose = False, output = 'screen'):
        '''Format slot.'''
        result = label + '\n'
        for (contributor, contributions) in slot:
            if contributions or verbose:
                result += '\t%s\n' % self._format_contributor_name(contributor)
                for contribution in contributions:
                    result += '\t\t%s\n' % contribution
        if output == 'screen':
            print result
        else:
            return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def formatter(self):
        return self._client

    @property
    def slot_1(self):
        '''Format contributions immediately before open brackets.'''
        return ()

    @property
    def slot_2(self):
        '''Open brackets, possibly including with-block.'''
        return ()

    @property
    def slot_3(self):
        '''Format contributions immediately after open brackets.'''
        return ()

    @property
    def slot_4(self):
        '''Formatted container contents or formatted leaf body.'''
        return ()

    @property
    def slot_5(self):
        '''Format contributions immediately before close brackets.'''
        return ()

    @property
    def slot_6(self):
        '''Close brackets.'''
        return ()

    @property
    def slot_7(self):
        '''Format contributions immediately after close brackets.'''
        return ()

    ### PUBLIC METHODS ###

    def contributions(self, attr):
        result = []
        for contributor, contributions in getattr(self, attr):
            result.extend(contributions)
        return result

    def wrap(self, contributor, attr):
        '''Wrap format contribution with format source.'''
        if False:
            pass
        else:
            return [(contributor, attr), getattr(contributor, attr)]
