from abjad import *
from abjad.tools import contexttools
import scf


def test_SCFObject_expr_to_parent_package_short_name_01():

    scf_object = scf.core.SCFObject()

    assert scf_object.expr_to_parent_package_short_name(Note("c'4")) == 'notetools'
    assert scf_object.expr_to_parent_package_short_name(Rest('r4')) == 'resttools'

    tempo_mark = contexttools.TempoMark('Allegro', (1, 4), 84)
    assert scf_object.expr_to_parent_package_short_name(tempo_mark) == 'contexttools'
