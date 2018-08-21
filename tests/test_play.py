import abjad
import pytest


def test_play_01():
    """
    A note can be played.
    """
    note = abjad.Note(1, (1, 2))
    abjad.play(note, test=True)


def test_play_02():
    """
    A score can be played.
    """
    notes = [abjad.Note(i, (1, 64)) for i in range(10)]
    staff = abjad.Staff(notes)
    score = abjad.Score([staff])
    abjad.play(score, test=True)
