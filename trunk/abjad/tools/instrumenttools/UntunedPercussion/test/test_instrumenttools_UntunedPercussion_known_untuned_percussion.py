from abjad import *


def test_instrumenttools_UntunedPercussion_known_untuned_percussion_01():

    percussion = instrumenttools.UntunedPercussion()

    assert 'castanets' in percussion.known_untuned_percussion
    assert 'caxixi' in percussion.known_untuned_percussion
    assert 'ratchet' in percussion.known_untuned_percussion
    assert 'whistle' in percussion.known_untuned_percussion
