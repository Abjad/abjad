from experimental.selectortools.CounttimeComponentSelector import CounttimeComponentSelector


class CounttimeContainerSelector(CounttimeComponentSelector):
    r'''.. versionadded:: 1.0

    Select one tuplet, counttime measure or other counttime container.
    '''

    ### INITIALIZER ##

    def __init__(self, container, inequality=None, klass=None, predicate=None, index=None):
        CounttimeComponentSelector.__init__(
            self, container, inequality=None, klass=None, predicate=None, index=None)
