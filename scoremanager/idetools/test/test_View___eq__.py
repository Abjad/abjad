# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import idetools


def test_View___eq___01():
    
    view_1 = idetools.View(["md:flavor == 'cherry'"])
    view_2 = idetools.View(["md:flavor == 'cherry'"])
    view_3 = idetools.View(["md:flavor == 'chocolate'"])

    assert view_1 == view_1
    assert view_1 == view_2
    assert not view_1 == view_3
    assert view_2 == view_1
    assert view_2 == view_2
    assert not view_2 == view_3
    assert not view_3 == view_1
    assert not view_3 == view_2
    assert view_3 == view_3

def test_View___eq___02():
    
    view_1 = idetools.View(["md:flavor == 'cherry'"])
    view_2 = idetools.View([
        "md:flavor == 'cherry'", 
        "md:flavor == 'chocolate'",
        ])

    assert view_1 == view_1
    assert not view_1 == view_2
    assert not view_2 == view_1
    assert view_2 == view_2