from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class SegmentSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import selectortools

    ::

        >>> selectortools.SegmentSelector(3)
        SegmentSelector(3)

    Select segment ``'red'``::

        >>> selectortools.SegmentSelector('red')
        SegmentSelector('red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, index, inequality=None):
        from experimental import specificationtools
        BackgroundElementSelector.__init__(self, specificationtools.Segment, index, inequality=inequality)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.index)
