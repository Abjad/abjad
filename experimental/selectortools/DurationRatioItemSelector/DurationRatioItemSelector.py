from experimental.selectortools.RatioSelector import RatioSelector
from experimental.selectortools.ItemSelector import ItemSelector


class DurationRatioItemSelector(RatioSelector, ItemSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select exactly one part.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, index=None):
        RatioSelector.__init__(self, reference, ratio)
        ItemSelector.__init__(self, index=index)
