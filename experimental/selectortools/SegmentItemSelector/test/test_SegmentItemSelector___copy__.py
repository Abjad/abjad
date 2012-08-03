from experimental import selectortools
import copy


def test_SegmentItemSelector___copy___01():

    selector_1 = selectortools.SegmentItemSelector(identifier='red')
    selector_2 = copy.copy(selector_1)
    selector_3 = copy.deepcopy(selector_1)

    assert isinstance(selector_1, selectortools.SegmentItemSelector)
    assert isinstance(selector_2, selectortools.SegmentItemSelector)
    assert isinstance(selector_3, selectortools.SegmentItemSelector)
    assert not selector_2 is selector_1
    assert not selector_3 is selector_1
    assert selector_1 == selector_2 == selector_3
