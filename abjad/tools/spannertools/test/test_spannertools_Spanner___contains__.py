# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___contains___01():

    class MockSpanner(spannertools.Spanner):

        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)

    note = Note("c'4")

    spanner = MockSpanner()
    attach(spanner, Note("c'4"))

    assert not note in spanner
