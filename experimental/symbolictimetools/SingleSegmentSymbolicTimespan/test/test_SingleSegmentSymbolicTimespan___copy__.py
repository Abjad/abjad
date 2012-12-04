from experimental import symbolictimetools
import copy


def test_SingleSegmentSymbolicTimespan___copy___01():

    selector_1 = symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')
    selector_2 = copy.copy(selector_1)
    selector_3 = copy.deepcopy(selector_1)

    assert isinstance(selector_1, symbolictimetools.SingleSegmentSymbolicTimespan)
    assert isinstance(selector_2, symbolictimetools.SingleSegmentSymbolicTimespan)
    assert isinstance(selector_3, symbolictimetools.SingleSegmentSymbolicTimespan)
    assert not selector_2 is selector_1
    assert not selector_3 is selector_1
    assert selector_1 == selector_2 == selector_3
