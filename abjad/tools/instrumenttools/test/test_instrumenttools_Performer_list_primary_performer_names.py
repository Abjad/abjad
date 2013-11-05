# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_list_primary_performer_names_01():

    performer_names = instrumenttools.Performer.list_performer_names()

    assert all(str(x) for x in performer_names)
