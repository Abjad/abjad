from experimental.tools.settingtools.SpecificationInterface import SpecificationInterface


class ScoreSpecificationInterface(SpecificationInterface):
    r'''Score setting interface.

    Score specification:

    ::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    With three named segments:

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    All score setting interface properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_specification):
        SpecificationInterface.__init__(self, score_specification)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Score setting interface score specification reference::

            >>> score_specification.interface.score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Return score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

    @property
    def specification_name(self):
        '''Score setting interface specification name::

            >>> score_specification.interface.specification_name is None
            True

        Return none.
        '''
        return SpecificationInterface.specification_name.fget(self)

    @property
    def storage_format(self):
        '''Score setting interface storage format::

            >>> z(score_specification.interface)
            settingtools.ScoreSpecificationInterface(
                specificationtools.ScoreSpecification(
                    scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                        staff_count=4
                        )
                    )
                )

        Return string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        '''Score setting interface timespan::

            >>> score_specification.interface.timespan
            TimespanExpression()

        Return timespan expression.
        '''
        return SpecificationInterface.timespan.fget(self)
    
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
