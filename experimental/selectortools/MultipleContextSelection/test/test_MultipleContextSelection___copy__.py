from experimental import selectortools
from experimental import specificationtools
import copy


def test_MultipleContextSelection___copy___01():

    segment_selector = selectortools.SegmentSelector(index='red')

    contexts = ['Voice 1', 'Voice 3']
    selection_1 = selectortools.MultipleContextSelection(contexts=contexts, timespan=segment_selector.timespan)
    selection_2 = copy.deepcopy(selection_1)

    assert isinstance(selection_1, selectortools.MultipleContextSelection)
    assert isinstance(selection_2, selectortools.MultipleContextSelection)
    assert not selection_1 is selection_2
    assert selection_1 == selection_2
