from abjad.tools.lilypondproxytools.LilyPondObjectProxy import LilyPondObjectProxy


class LilyPondGrobProxy(LilyPondObjectProxy):
    '''.. versionadded:: 2.0

    LilyPond grob proxy.
    '''

    def __copy__(self):
        return eval(repr(self))
