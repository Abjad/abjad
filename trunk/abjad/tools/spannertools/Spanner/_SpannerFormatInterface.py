from abjad.tools.abctools import AbjadObject


class _SpannerFormatInterface(AbjadObject):
    '''Abstract base class.
    Model format interface for all Abjad spanners.
    '''

    ### SPECIAL METHODS ###

    def __init__(self, spanner):
        '''Bind to spanner client.'''
        self._spanner = spanner

    ### PUBLIC PROPERTIES ###

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
