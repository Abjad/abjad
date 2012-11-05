from experimental.requesttools.AbsoluteRequest import AbsoluteRequest
from experimental.selectortools.SingleSegmentSelector import SingleSegmentSelector
from experimental.settingtools.SingleContextSetting import SingleContextSetting
from experimental.symbolictimetools.SymbolicOffset import SymbolicOffset
from experimental.symbolictimetools.SingleSourceSymbolicTimespan import SingleSourceSymbolicTimespan


def test_SingleContextSetting___repr___01():
    '''Repr is evaluable.
    '''

    selector = SingleSegmentSelector(identifier='red')
    setting_1 = SingleContextSetting('time_signatures', AbsoluteRequest([(4, 8), (3, 8)]), selector, fresh=False)
    setting_2 = eval(repr(setting_1))

    assert isinstance(setting_1, SingleContextSetting)
    assert isinstance(setting_2, SingleContextSetting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
