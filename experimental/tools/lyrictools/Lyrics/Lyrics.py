from abjad.tools.contexttools.Context import Context


class Lyrics(Context):
    r'''Abjad model of LilyPond `\lyrics` context:

    ::

        >>> from experimental.tools import lyrictools
        >>> lyrics = lyrictools.Lyrics()

    ::

        >>> note = Note("c'4")

    ::

        >>> show(note) # doctest: +SKIP

    ::

        >>> note.written_duration = (1, 2)

    ::

        >>> show(note) # doctest: +SKIP

    Return `Lyrics` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None):
        Context.__init__(self, music)
        self.context_name = 'Lyrics'
