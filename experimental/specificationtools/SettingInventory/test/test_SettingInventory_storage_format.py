from abjad.tools import *
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import library
from experimental.specificationtools.Setting import Setting
from experimental.specificationtools.SettingInventory import SettingInventory
from experimental.specificationtools.ComponentSelector import ComponentSelector
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.specificationtools.Selection import Selection
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan


def test_SettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    storage_format = directive_inventory_1.storage_format

    r'''
    specificationtools.SettingInventory([
        specificationtools.Setting(
            specificationtools.Selection(
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.Timespan(
                    start=timespantools.Timepoint(
                        anchor=specificationtools.ComponentSelector(
                            segment='1'
                            ),
                        edge=Left
                        ),
                    stop=timespantools.Timepoint(
                        anchor=specificationtools.ComponentSelector(
                            segment='1'
                            ),
                        edge=Right
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False
            )
        ])
    '''

    assert storage_format == "specificationtools.SettingInventory([\n\tspecificationtools.Setting(\n\t\tspecificationtools.Selection(\n\t\t\tcontexts=['Grouped Rhythmic Staves Score'],\n\t\t\ttimespan=timespantools.Timespan(\n\t\t\t\tstart=timespantools.Timepoint(\n\t\t\t\t\tanchor=specificationtools.ComponentSelector(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Left\n\t\t\t\t\t),\n\t\t\t\tstop=timespantools.Timepoint(\n\t\t\t\t\tanchor=specificationtools.ComponentSelector(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Right\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(storage_format)

    assert isinstance(directive_inventory_1, SettingInventory)
    assert isinstance(directive_inventory_2, SettingInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
