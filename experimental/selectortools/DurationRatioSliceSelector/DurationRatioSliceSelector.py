from experimental.selectortools.CountRatioSelector import CountRatioSelector
from experimental.selectortools.SliceSelector import SliceSelector


class DurationRatioSliceSelector(CountRatioSelector, SliceSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select zero or more contiguous parts.
    '''

    ### INTIALIZER ###

    def __init__(self, reference, ratio, start=None, stop=None):
        CountRatioSelector.__init__(self, reference, ratio)
        SliceSelector.__init__(self, start=start, stop=stop)
