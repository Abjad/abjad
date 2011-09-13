from abjad import *


def test_contexttools_get_instrument_mark_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    instrument_mark = contexttools.InstrumentMark('Violin ', 'Vn. ')
    instrument_mark.attach(staff)

    found_instrument_mark = contexttools.get_instrument_mark_attached_to_component(staff)

    assert found_instrument_mark is instrument_mark
