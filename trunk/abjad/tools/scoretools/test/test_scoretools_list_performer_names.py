from abjad import *


def test_scoretools_list_performer_names_01():

    performer_names = scoretools.list_performer_names()

    assert all([str(x) for x in performer_names])
