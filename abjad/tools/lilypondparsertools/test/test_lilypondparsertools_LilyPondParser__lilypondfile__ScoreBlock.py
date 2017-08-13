import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__lilypondfile__ScoreBlock_01():

    target = abjad.Block(name='score')
    target.items.append(abjad.Score())
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
