# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_01():

    target = Container([Note(0, 1), Note(0, 1)])
    glissando = spannertools.Glissando()
    attach(glissando, target[:])
    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_02():

    string = r'{ c \glissando }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_03():

    string = r'{ \glissando c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
