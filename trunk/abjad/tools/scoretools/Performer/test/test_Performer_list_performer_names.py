# -*- encoding: utf-8 -*-
from abjad import *


def test_Performer_list_performer_names_01():

    performer_names = scoretools.Performer.list_performer_names()

    assert all(str(x) for x in performer_names)
