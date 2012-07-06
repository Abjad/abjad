from experimental.specificationtools.ContextSelection import ContextSelection
from experimental.selectortools.CounttimeComponentSelector import CounttimeComponentSelector
from experimental.specificationtools.ContextSetting import ContextSetting
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan
import py


def test_ContextSetting___repr___01():
    '''Repr is evaluable.
    '''
    py.test.skip('make repr evaluable again.')

    anchor = CounttimeComponentSelector(segment='1')
    start = Timepoint(anchor=anchor)
    stop = Timepoint(anchor=anchor, edge=Right)
    timespan = Timespan(start=start, stop=stop)
    target = ContextSelection('Voice 1', timespan=timespan)
    setting_1 = ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    setting_2 = eval(repr(setting_1))

    assert isinstance(setting_1, ContextSetting)
    assert isinstance(setting_2, ContextSetting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
