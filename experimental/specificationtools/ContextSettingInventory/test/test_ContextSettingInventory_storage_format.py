from abjad.tools import *
from experimental import selectortools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification
from experimental.specificationtools import ContextSettingInventory


def test_ContextSettingInventory_storage_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    score_specification.interpret()

    setting_inventory_1 = segment.settings

    storage_format = setting_inventory_1.storage_format

    r'''
    specificationtools.ContextSettingInventory([
        specificationtools.ContextSetting(
            specificationtools.ContextSelection(
                'Grouped Rhythmic Staves Score',
                timespan=timespantools.Timespan(
                    start=timespantools.Timepoint(
                        anchor=selectortools.CounttimeCounttimeComponentSelector(
                            segment='1'
                            ),
                        edge=Left
                        ),
                    stop=timespantools.Timepoint(
                        anchor=selectortools.CounttimeCounttimeComponentSelector(
                            segment='1'
                            ),
                        edge=Right
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False,
            fresh=True
            )
        ])
    '''

    assert storage_format == "specificationtools.ContextSettingInventory([\n\tspecificationtools.ContextSetting(\n\t\tspecificationtools.ContextSelection(\n\t\t\t'Grouped Rhythmic Staves Score',\n\t\t\ttimespan=timespantools.Timespan(\n\t\t\t\tstart=timespantools.Timepoint(\n\t\t\t\t\tanchor=selectortools.CounttimeCounttimeComponentSelector(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Left\n\t\t\t\t\t),\n\t\t\t\tstop=timespantools.Timepoint(\n\t\t\t\t\tanchor=selectortools.CounttimeCounttimeComponentSelector(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Right\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False,\n\t\tfresh=True\n\t\t)\n\t])"

    setting_inventory_2 = eval(storage_format)

    assert isinstance(setting_inventory_1, ContextSettingInventory)
    assert isinstance(setting_inventory_2, ContextSettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
