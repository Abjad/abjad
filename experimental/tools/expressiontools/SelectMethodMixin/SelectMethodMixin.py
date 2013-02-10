from abjad.tools import chordtools
from abjad.tools import leaftools
from abjad.tools import notetools
from abjad.tools.abctools import AbjadObject


class SelectMethodMixin(AbjadObject):
    '''Select-method mix-in.

    Definitions for examples, below:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that implement the select method interface.
    '''
    
    ### PUBLIC METHODS ###

    def select_beats(self, voice_name, time_relation=None):
        '''Select voice ``1`` beats that start during segment ``'red'``::

            >>> beats = red_segment.select_beats('Voice 1')

        ::

            >>> z(beats)
            expressiontools.BeatSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return beat select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.BeatSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_divisions(self, voice_name, time_relation=None):
        '''Select voice ``1`` divisions that start during segment ``'red'``::

            >>> divisions = red_segment.select_divisions('Voice 1')

        ::
            
            >>> z(divisions)
            expressiontools.DivisionSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return division select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.DivisionSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_leaves(self, voice_name, time_relation=None):
        '''Select voice ``1`` leaves that start during segment ``'red'``::

            >>> leaves = red_segment.select_leaves('Voice 1')

        ::

            >>> z(leaves)
            expressiontools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=expressiontools.ClassInventory([
                    leaftools.Leaf
                    ]),
                voice_name='Voice 1'
                )

        Return counttime component select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.CounttimeComponentSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation, 
            classes=(leaftools.Leaf, ), 
            voice_name=voice_name
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_measures(self, voice_name, time_relation=None):
        '''Select voice ``1`` measures 
        that start during segment ``'red'``::

            >>> measures = red_segment.select_measures('Voice 1')

        ::

            >>> z(measures)
            expressiontools.MeasureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return measure select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.MeasureSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_notes_and_chords(self, voice_name, time_relation=None):
        '''Select voice ``1`` notes and chords that start during segment ``'red'``::

            >>> notes_and_chords = red_segment.select_notes_and_chords('Voice 1')

        ::

            >>> z(notes_and_chords)
            expressiontools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=expressiontools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                )

        Return counttime component select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.CounttimeComponentSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation, 
            classes=(notetools.Note, chordtools.Chord),
            voice_name=voice_name
            )
        select_expression._score_specification = self.score_specification
        return select_expression

#    def select_segments(self, voice_name):
#        '''Select voice ``1`` segments in score::
#
#            >>> select_expression = score_specification.select_segments('Voice 1')
#
#        ::
#
#            >>> z(select_expression)
#            expressiontools.SegmentSelectExpression(
#                voice_name='Voice 1'
#                )
#
#        Return segment select expression.
#        '''
#        from experimental.tools import expressiontools
#        select_expression = expressiontools.SegmentSelectExpression(voice_name=voice_name)
#        select_expression._score_specification = self.score_specification
#        return select_expression

    def select_time_signatures(self, voice_name, time_relation=None):
        '''Select voice ``1`` time signatures that start during segment ``'red'``::

            >>> time_signatures = red_segment.select_time_signatures('Voice 1')

        ::

            >>> z(time_signatures)
            expressiontools.TimeSignatureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return time signature select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.TimeSignatureSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation, 
            voice_name=voice_name
            )
        select_expression._score_specification = self.score_specification
        return select_expression
