from abjad.tools import chordtools
from abjad.tools import notetools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


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
        # TODO: assert trope type
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
        leaves = []
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, (notetools.Note, chordtools.Chord)), repr(leaf)
            chromatic_pitch_numbers = statal_server_cursor()
            assert len(chromatic_pitch_numbers) == 1
            leaf.sounding_pitch = chromatic_pitch_numbers[0]
