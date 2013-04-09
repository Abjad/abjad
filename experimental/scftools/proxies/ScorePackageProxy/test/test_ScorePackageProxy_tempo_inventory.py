from abjad.tools import contexttools
from abjad.tools import durationtools
import scftools


def test_ScorePackageProxy_tempo_inventory_01():

    score_package_proxy = scftools.proxies.ScorePackageProxy('example_score_1')

    assert score_package_proxy.tempo_inventory == contexttools.TempoMarkInventory([
        contexttools.TempoMark(durationtools.Duration(1, 8), 72),
        contexttools.TempoMark(durationtools.Duration(1, 8), 108),
        contexttools.TempoMark(durationtools.Duration(1, 8), 90),
        contexttools.TempoMark(durationtools.Duration(1, 8), 135)])
