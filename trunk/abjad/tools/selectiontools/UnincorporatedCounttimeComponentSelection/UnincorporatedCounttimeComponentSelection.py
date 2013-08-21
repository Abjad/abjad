from abjad.tools.selectiontools.FreeComponentSelection \
    import FreeComponentSelection


class UnincorporatedCounttimeComponentSelection(FreeComponentSelection):
    '''A selection of counttime components not yet incorporated in any score.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import componenttools
        music = music or []
        for x in music:
            assert isinstance(x, componenttools.Component), repr(x)
            assert x._is_counttime_component, repr(x)
            assert x._get_parentage().is_orphan, repr(x)
        FreeComponentSelection.__init__(self, music=music)
