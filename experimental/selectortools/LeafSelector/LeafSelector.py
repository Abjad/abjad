from experimental.selectortools.CounttimeComponentSelector import CounttimeComponentSelector


class LeafSelector(CounttimeComponentSelector):
    r'''.. versionadded:: 1.0

    Select one leaf.
    '''

    ### INITIALIZER ###

    def __init__(self, container, inequality=None, klass=None, predicate=None, index=None):
        CounttimeComponentSelector.__init__(            
            self, container, inequality=None, klass=None, predicate=None, index=None)
