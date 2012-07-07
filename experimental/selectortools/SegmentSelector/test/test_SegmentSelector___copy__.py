from experimental import selectortools
import copy


def test_SegmentSelector___copy___01():

    selector_1 = selectortools.SegmentSelector(index='red')
    selector_2 = copy.copy(selector_1)
    selector_3 = copy.deepcopy(selector_1)

    assert isinstance(selector_1, selectortools.SegmentSelector)
    assert isinstance(selector_2, selectortools.SegmentSelector)
    assert isinstance(selector_3, selectortools.SegmentSelector)
    assert not selector_2 is selector_1
    assert not selector_3 is selector_1
    assert selector_1 == selector_2 == selector_3
