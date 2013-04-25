from abjad import *
from abjad.tools import contexttools
from experimental import *


def test_ScoreManagerObject_expr_to_parent_package_short_name_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    assert score_manager_object.expr_to_parent_package_short_name(Note("c'4")) == 'notetools'
    assert score_manager_object.expr_to_parent_package_short_name(Rest('r4')) == 'resttools'

    tempo_mark = contexttools.TempoMark('Allegro', (1, 4), 84)
    assert score_manager_object.expr_to_parent_package_short_name(tempo_mark) == 'contexttools'
