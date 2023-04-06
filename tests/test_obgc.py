import pytest

import abjad


def test_obgc_01():
    """
    Raises exception when duration of on-beat grace container exceeds duration
    of anchor container.
    """

    music_voice = abjad.Voice("c'4 d' e' f'", name="MusicVoice")
    string = "g'8 a' b' c'' d'' c'' b' a' b' c'' d''"
    with pytest.raises(Exception):
        abjad.on_beat_grace_container(
            string,
            music_voice[1:2],
            grace_leaf_duration=(1, 8),
        )
