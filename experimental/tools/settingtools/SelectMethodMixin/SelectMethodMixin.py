from abjad.tools import chordtools
from abjad.tools import leaftools
from abjad.tools import notetools
from abjad.tools.abctools import AbjadObject


class SelectMethodMixin(AbjadObject):
    '''Select-method mix-in.

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select-method mix-ins are immutable.
    '''
    
    ### PUBLIC METHODS ###

    def select_beats(self, voice_name, time_relation=None):
        '''Select voice ``1`` beats that start during segment ``'red'``::

            >>> beats = red_segment.select_beats('Voice 1')

        ::

            >>> z(beats)
            settingtools.BeatSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return beat selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.BeatSelectExpression(
            anchor=self._anchor_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_divisions(self, voice_name, time_relation=None):
        '''Select voice ``1`` divisions that start during segment ``'red'``::

            >>> divisions = red_segment.select_divisions('Voice 1')

        ::
            
            >>> z(divisions)
            settingtools.DivisionSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return division selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.DivisionSelectExpression(
            anchor=self._anchor_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_leaves(self, voice_name, time_relation=None):
        '''Select voice ``1`` leaves that start during segment ``'red'``::

            >>> leaves = red_segment.select_leaves('Voice 1')

        ::

            >>> z(leaves)
            settingtools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=settingtools.ClassInventory([
                    leaftools.Leaf
                    ]),
                voice_name='Voice 1'
                )

        Return counttime component selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.CounttimeComponentSelectExpression(
            anchor=self._anchor_abbreviation,
            time_relation=time_relation, 
            classes=(leaftools.Leaf, ), 
            voice_name=voice_name
            )
        selector._score_specification = self.score_specification
        return selector

    def select_measures(self, voice_name, time_relation=None):
        '''Select voice ``1`` measures 
        that start during segment ``'red'``::

            >>> measures = red_segment.select_measures('Voice 1')

        ::

            >>> z(measures)
            settingtools.MeasureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return measure selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.MeasureSelectExpression(
            anchor=self._anchor_abbreviation,
            voice_name=voice_name,
            time_relation=time_relation
            )
        selector._score_specification = self.score_specification
        return selector

    def select_notes_and_chords(self, voice_name, time_relation=None):
        '''Select voice ``1`` notes and chords that start during segment ``'red'``::

            >>> notes_and_chords = red_segment.select_notes_and_chords('Voice 1')

        ::

            >>> z(notes_and_chords)
            settingtools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=settingtools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                )

        Return counttime component selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.CounttimeComponentSelectExpression(
            anchor=self._anchor_abbreviation,
            time_relation=time_relation, 
            classes=(notetools.Note, chordtools.Chord),
            voice_name=voice_name
            )
        selector._score_specification = self.score_specification
        return selector

    def select_time_signatures(self, voice_name, time_relation=None):
        '''Select voice ``1`` time signatures that start during segment ``'red'``::

            >>> time_signatures = red_segment.select_time_signatures('Voice 1')

        ::

            >>> z(time_signatures)
            settingtools.TimeSignatureSelectExpression(
                anchor='red',
                voice_name='Voice 1'
                )

        Return time signature selector.
        '''
        from experimental.tools import settingtools
        selector = settingtools.TimeSignatureSelectExpression(
            anchor=self._anchor_abbreviation,
            time_relation=time_relation, 
            voice_name=voice_name
            )
        selector._score_specification = self.score_specification
        return selector
