from experimental.selectortools.CounttimeComponentSliceSelector import CounttimeComponentSliceSelector


class LeafSliceSelector(CounttimeComponentSliceSelector):
    r'''.. versionadded:: 1.0

    Select zero or more leaves.
    '''

    ### INITIALIZER ###

    def __init__(self, container, inequality=None, klass=None, predicate=None, start=None, stop=None):
        CounttimeComponentSliceSelector.__init__(
            self, container, inequality=None, klass=None, predicate=None, start=None, stop=None)
