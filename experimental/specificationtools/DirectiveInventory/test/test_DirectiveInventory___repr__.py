from abjad.tools import *
from experimental.specificationtools.Directive import Directive
from experimental.specificationtools.DirectiveInventory import DirectiveInventory
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.specificationtools.Selection import Selection
from experimental.specificationtools.TemporalCursor import TemporalCursor
from experimental.specificationtools.Timespan import Timespan


def test_DirectiveInventory___repr___01():
    '''Repr is evaluable.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives
    directive_inventory_2 = eval(repr(directive_inventory_1))

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
