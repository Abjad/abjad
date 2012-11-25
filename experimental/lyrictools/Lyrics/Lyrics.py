from abjad.tools.contexttools.Context import Context


class Lyrics(Context):
    r'''Abjad model of LilyPond `\lyrics` context:

    ::

        >>> from experimental import lyrictools 
        >>> lyrics = lyrictools.Lyrics()
        >>> show(lyrics)

    Return `Lyrics` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None):
        Context.__init__(self, music)
        self.context_name = 'Lyrics'
