from abjad.tools import *
from experimental import specificationtools
from experimental.specificationtools import library
from experimental.specificationtools.Directive import Directive
from experimental.specificationtools.DirectiveInventory import DirectiveInventory
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.specificationtools.Selection import Selection
from experimental.specificationtools.TemporalCursor import TemporalCursor
from experimental.specificationtools.Timespan import Timespan


def test_DirectiveInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    storage_format = directive_inventory_1.storage_format

    r'''
    specificationtools.DirectiveInventory([
        specificationtools.Directive(
            specificationtools.Selection(
                contexts=['Grouped Rhythmic Staves Score'],
                scope=specificationtools.Timespan(
                    start=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
                            segment='1'
                            ),
                        edge=Left
                        ),
                    stop=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
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

    assert storage_format == "specificationtools.DirectiveInventory([\n\tspecificationtools.Directive(\n\t\tspecificationtools.Selection(\n\t\t\tcontexts=['Grouped Rhythmic Staves Score'],\n\t\t\tscope=specificationtools.Timespan(\n\t\t\t\tstart=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Left\n\t\t\t\t\t),\n\t\t\t\tstop=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=Right\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(storage_format)

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
