from experimental import selectortools
from experimental import specificationtools
import copy


def test_MultipleContextSelection___copy___01():

    timespan = specificationtools.segments_to_timespan('red')

    selection_1 = selectortools.MultipleContextSelection(contexts=['Voice 1', 'Voice 3'], timespan=timespan)
    selection_2 = copy.deepcopy(selection_1)

    assert isinstance(selection_1, selectortools.MultipleContextSelection)
    assert isinstance(selection_2, selectortools.MultipleContextSelection)
    assert not selection_1 is selection_2
    assert selection_1 == selection_2
