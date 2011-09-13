from abjad.core import _StrictComparator


class _SpannerFormatInterface(_StrictComparator):
    '''Abstract base class.
    Model format interface for all Abjad spanners.
    '''

    ### OVERLOADS ###

    def __init__(self, spanner):
        '''Bind to spanner client.'''
        self._spanner = spanner

    ### PUBLIC ATTRIBUTES ###

    @property
    def spanner(self):
        '''Read-only reference to spanner client.'''
        return self._spanner

    ### PRIVATE METHODS ###

    def _after(self, leaf):
        '''Spanner format contributions to output after leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_last_leaf(leaf):
            result.extend(getattr(spanner, '_reverts', []))
        return result

    def _before(self, leaf):
        '''Spanner format contributions to output before leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.extend(getattr(spanner, '_overrides', []))
        return result

    def _left(self, leaf):
        '''Spanner format contributions to output left of leaf.'''
        result = []
        return result

    def _right(self, leaf):
        '''Spanner format contributions to output right of leaf.'''
        result = []
        return result

    ### PUBLIC METHODS ###

    def report(self, leaves = None, output = 'screen'):
        '''Print spanner format contributions for every leaf in leaves.'''
        result = ''
        leaves = leaves or self.spanner.leaves
        for leaf in leaves:
            result += str(leaf)
            result += '\tbefore: %s\n' % self._before(leaf)
            result += '\t after: %s\n' % self._after(leaf)
            result += '\t  left: %s\n' % self._left(leaf)
            result += '\t right: %s\n' % self._right(leaf)
            result += '\n'

        if result[-1] == '\n':
            result = result[:-1]

        if output == 'screen':
            print result
        else:
            return result
