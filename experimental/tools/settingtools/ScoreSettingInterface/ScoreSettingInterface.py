from experimental.tools.settingtools.SettingInterface import SettingInterface


class ScoreSettingInterface(SettingInterface):
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
        SettingInterface.__init__(self, score_specification)
    
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
