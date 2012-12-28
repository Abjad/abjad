from experimental.tools.requesttools.AbsoluteRequest import AbsoluteRequest
from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting
from experimental.tools.timeexpressiontools.OffsetExpression import OffsetExpression


def test_SingleContextSetting___repr___01():
    '''Repr is evaluable.
    '''

    setting_1 = SingleContextSetting('time_signatures', AbsoluteRequest([(4, 8), (3, 8)]), 'red', fresh=False)
    setting_2 = eval(repr(setting_1))

    assert isinstance(setting_1, SingleContextSetting)
    assert isinstance(setting_2, SingleContextSetting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
