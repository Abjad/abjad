from abjad.tools.selectiontools.HorizontalSelection import HorizontalSelection


class LeafSelection(HorizontalSelection):
    '''Selection of leaves.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import leaftools
        HorizontalSelection.__init__(self, music=music)
        assert all(isinstance(x, leaftools.Leaf) for x in self)
