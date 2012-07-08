from experimental.selectortools.CounttimeComponentSliceSelector import CounttimeComponentSliceSelector


class CounttimeContainerSliceSelector(CounttimeComponentSliceSelector):
    r'''.. versionadded:: 1.0

    Select zero or more tuplets, counttime measures or other counttime containers.
    '''

    ### INITIALIZER ###

    def __init__(self, container, inequality=None, klass=None, predicate=None, start=None, stop=None):
        CounttimeComponentSliceSelector.__init__(            
            self, container, inequality=None, klass=None, predicate=None, start=None, stop=None)
