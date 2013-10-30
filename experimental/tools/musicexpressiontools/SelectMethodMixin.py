# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools import AbjadObject


class SelectMethodMixin(AbjadObject):
    r'''Select-method mix-in.

    Definitions for examples, below:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that implement the select method interface.
    '''

    ### PUBLIC METHODS ###

    def select_beats(self, voice_name, time_relation=None):
        r'''Select voice ``1`` beats that start during segment ``'red'``:

        ::

            >>> beats = red_segment.select_beats('Voice 1')

        ::

            >>> print beats.storage_format
            musicexpressiontools.BeatSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Returns beat select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = musicexpressiontools.BeatSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_divisions(self, voice_name, time_relation=None):
        r'''Select voice ``1`` divisions that start during segment ``'red'``:

        ::

            >>> divisions = red_segment.select_divisions('Voice 1')

        ::

            >>> print divisions.storage_format
            musicexpressiontools.DivisionSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Returns division select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = \
            musicexpressiontools.DivisionSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation,
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_leaves(self, voice_name, time_relation=None):
        r'''Select voice ``1`` leaves that start during segment ``'red'``:

        ::

            >>> leaves = red_segment.select_leaves('Voice 1')

        ::

            >>> print leaves.storage_format
            musicexpressiontools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=musicexpressiontools.ClassInventory([
                    scoretools.Leaf
                    ]),
                voice_name='Voice 1'
                )

        Returns counttime component select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = \
            musicexpressiontools.CounttimeComponentSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation,
            classes=(scoretools.Leaf, ),
            voice_name=voice_name,
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_measures(self, voice_name, time_relation=None):
        r'''Select voice ``1`` measures that start during segment ``'red'``:

        ::

            >>> measures = red_segment.select_measures('Voice 1')

        ::

            >>> print measures.storage_format
            musicexpressiontools.MeasureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Returns measure select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = \
            musicexpressiontools.MeasureSelectExpression(
            anchor=self._expression_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation,
            )
        select_expression._score_specification = self.score_specification
        return select_expression

    def select_notes_and_chords(self, voice_name, time_relation=None):
        r'''Select voice ``1`` notes and chords that start during segment 
        ``'red'``:

        ::

            >>> notes_and_chords = red_segment.select_notes_and_chords('Voice 1')

        ::

            >>> print notes_and_chords.storage_format
            musicexpressiontools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=musicexpressiontools.ClassInventory([
                    scoretools.Note,
                    scoretools.Chord
                    ]),
                voice_name='Voice 1'
                )

        Returns counttime component select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = \
            musicexpressiontools.CounttimeComponentSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation,
            classes=(scoretools.Note, scoretools.Chord),
            voice_name=voice_name,
            )
        select_expression._score_specification = self.score_specification
        return select_expression

#    def select_segments(self, voice_name):
#        r'''Select voice ``1`` segments in score:
#
#        ::
#
#            >>> select_expression = score_specification.select_segments('Voice 1')
#
#        ::
#
#            >>> print select_expression.storage_format
#            musicexpressiontools.SegmentSelectExpression(
#                voice_name='Voice 1'
#                )
#
#        Returns segment select expression.
#        '''
#        from experimental.tools import musicexpressiontools
#        select_expression = musicexpressiontools.SegmentSelectExpression(voice_name=voice_name)
#        select_expression._score_specification = self.score_specification
#        return select_expression

    def select_time_signatures(self, voice_name, time_relation=None):
        r'''Select voice ``1`` time signatures that start during segment 
        ``'red'``:

        ::

            >>> time_signatures = red_segment.select_time_signatures('Voice 1')

        ::

            >>> print time_signatures.storage_format
            musicexpressiontools.TimeSignatureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Returns time signature select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = \
            musicexpressiontools.TimeSignatureSelectExpression(
            anchor=self._expression_abbreviation,
            time_relation=time_relation,
            voice_name=voice_name,
            )
        select_expression._score_specification = self.score_specification
        return select_expression
