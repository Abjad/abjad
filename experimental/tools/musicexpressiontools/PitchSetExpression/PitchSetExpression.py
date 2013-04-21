from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools import notetools
from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.LeafSetExpression import LeafSetExpression


class PitchSetExpression(LeafSetExpression):
    '''Pitch set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None,
        node_count=None, level=None, trope=None):
        LeafSetExpression.__init__(self, source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory)
        assert isinstance(node_count, (int, type(None))), repr(node_count)
        assert isinstance(level, (int, type(None))), repr(level)
        self._node_count = node_count
        self._level = level
        self._trope = trope

    ### READ-ONLY PUBLIC PROPERTIES ##

    @property
    def level(self):
        '''Pitch set expression level.

        Return integer or none.
        '''
        return self._level

    @property
    def node_count(self):
        '''Pitch set expression node count.

        Return nonnegative integer or none.
        '''
        return self._node_count

    @property
    def trope(self):
        '''Pitch set expression trope.
        '''
        return self._trope

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute pitch set expression against `score`.
        '''
        statal_server_cursor = self.source_expression.payload
        leaves = list(self._iterate_selected_leaves_in_score(score))
        assert all([isinstance(leaf, (notetools.Note, chordtools.Chord)) for leaf in leaves]), repr(leaves)
        if self.level is None:
            level = -1
        else:
            level = self.level
        if self.node_count is None:
            node_count = len(leaves)
        else:
            node_count = self.node_count
        chromatic_pitch_numbers = statal_server_cursor(n=node_count, level=level)
        chromatic_pitch_numbers = sequencetools.CyclicTuple(chromatic_pitch_numbers)
        for i, leaf in enumerate(leaves):
            leaf.sounding_pitch = chromatic_pitch_numbers[i]
