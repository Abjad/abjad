from experimental.tools import requesttools
from experimental.tools import settingtools
from experimental.tools import specificationtools
from experimental.tools import timeexpressiontools
from abjad.tools import timerelationtools


def test_SingleContextSetting___init___01():
    '''Initialize by hand.
    '''

    setting = settingtools.SingleContextSetting(
        'time_signatures', requesttools.AbsoluteRequest([(4, 8), (3, 8)]), 'red', context_name='Voice 1')

    assert isinstance(setting, settingtools.SingleContextSetting)
