from experimental.specificationtools.ContextSelection import ContextSelection
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
from experimental.specificationtools.Setting import Setting
from experimental.specificationtools.TemporalCursor import TemporalCursor
from experimental.specificationtools.Timespan import Timespan


def test_Setting___repr___01():
    '''Repr is evaluable.
    '''

    anchor = ScoreObjectIndicator(segment='1')
    start = TemporalCursor(anchor=anchor)
    stop = TemporalCursor(anchor=anchor, edge=Right)
    timespan = Timespan(start=start, stop=stop)
    target = ContextSelection('Voice 1', timespan=timespan)
    setting_1 = Setting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    setting_2 = eval(repr(setting_1))

    assert isinstance(setting_1, Setting)
    assert isinstance(setting_2, Setting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
