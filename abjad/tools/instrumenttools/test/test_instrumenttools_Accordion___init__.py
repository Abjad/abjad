# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Accordion___init___01():

    accordion = instrumenttools.Accordion()

    assert isinstance(accordion, instrumenttools.Accordion)
