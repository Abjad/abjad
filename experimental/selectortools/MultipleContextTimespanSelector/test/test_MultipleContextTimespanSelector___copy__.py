from experimental import selectortools
from experimental import specificationtools
import copy


def test_MultipleContextTimespanSelector___copy___01():

    segment_selector = selectortools.SegmentSelector(index='red')

    context_names = ['Voice 1', 'Voice 3']
    selection_1 = selectortools.MultipleContextTimespanSelector(
        context_names=context_names, timespan=segment_selector.timespan)
    selection_2 = copy.deepcopy(selection_1)

    assert isinstance(selection_1, selectortools.MultipleContextTimespanSelector)
    assert isinstance(selection_2, selectortools.MultipleContextTimespanSelector)
    assert not selection_1 is selection_2
    assert selection_1 == selection_2
