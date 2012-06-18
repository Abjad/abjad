from experimental import specificationtools
import copy


def test_Selection___copy___01():

    timespan = specificationtools.segments_to_timespan('red')

    selection_1 = specificationtools.Selection(contexts=['Voice 1', 'Voice 3'], timespan=timespan)
    selection_2 = copy.deepcopy(selection_1)

    assert isinstance(selection_1, specificationtools.Selection)
    assert isinstance(selection_2, specificationtools.Selection)
    assert not selection_1 is selection_2
    assert selection_1 == selection_2
