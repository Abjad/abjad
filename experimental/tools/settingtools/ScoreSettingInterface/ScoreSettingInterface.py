from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.timeexpressiontools.SelectMethodMixin import SelectMethodMixin


class ScoreSettingInterface(SelectMethodMixin, SetMethodMixin):
    r'''Score setting interface.

    ::

        >>> from experimental.tools import *

    Score specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    With three named segments::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    All score setting interface properties are read-only.
    '''
    
    ### INITIALIZER ###

    def __init__(self, score_specification):
        #SettingInterface.__init__(self, score_specification)
        self._score_specification = score_specification

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}()'.format(self._class_name)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        return self.specification_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Read-only reference to score against which segment specification is defined.

        Return score specification.
        '''
        return self._score_specification

    @property
    def specification_name(self):
        return

    @property
    def timespan(self):
        from experimental.tools import timeexpressiontools
        timespan = timeexpressiontools.TimespanExpression()
        timespan._score_specification = self.score_specification
        return timespan

    ### PUBLIC METHODS ###

    def select_segments(self, voice_name):
        '''Select voice ``1`` segments in score::

            >>> selector = score_specification.interface.select_segments('Voice 1')

        ::

            >>> z(selector)
            selectortools.SegmentSelector(
                voice_name='Voice 1'
                )

        Return segment selector.
        '''
        from experimental.tools import selectortools
        selector = selectortools.SegmentSelector(voice_name=voice_name)
        selector._score_specification = self
        return selector
