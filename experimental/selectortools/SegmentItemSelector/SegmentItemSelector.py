from experimental.selectortools.BackgroundElementItemSelector import BackgroundElementItemSelector


class SegmentItemSelector(BackgroundElementItemSelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import *

    ::

        >>> selectortools.SegmentItemSelector(identifier=3)
        SegmentItemSelector(identifier=3)

    Select segment ``'red'``::

        >>> selectortools.SegmentItemSelector(identifier='red')
        SegmentItemSelector(identifier='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, identifier=0):
        from experimental import specificationtools
        self._identifier = identifier
        BackgroundElementItemSelector.__init__(self, 
            klass=specificationtools.Segment, inequality=inequality, identifier=identifier)

    ### READ-ONLY PROPERTIES ###

    @property
    def context_name(self):
        '''Return none.
        '''
        return

    @property
    def context_names(self):
        '''Return empty list.
        '''
        return []

    @property
    def identifier(self):
        return self._identifier

    @property
    def segment_identifier(self):
        return self._identifier

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        segment_specification = score_specification.get_segment_specification(self)
        return segment_specification.duration
