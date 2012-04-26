from abjad.tools.abctools.ScoreSelection import ScoreSelection


class TieChain(ScoreSelection):
    '''.. versionadded:: 2.9

    All the notes in a tie chain.

    A tie chain of length 1 is a trivial tie chain.

    Nontied notes, rests, chords exists in a trivial tie chain.

    Tied notes, rests, chords exist in a nontrivial tie chain.

    Nontrivial tie chains exhibit length 2 or greater.

    Tie chains are immutable score selections.
    '''

    def __init__(self):
        pass
