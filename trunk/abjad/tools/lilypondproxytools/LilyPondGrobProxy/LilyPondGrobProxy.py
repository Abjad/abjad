# -*- encoding: utf-8 -*-
from abjad.tools.lilypondproxytools.LilyPondObjectProxy \
	import LilyPondObjectProxy


class LilyPondGrobProxy(LilyPondObjectProxy):
    '''LilyPond grob proxy.
    '''

    ### SPECIAL METHODS ###

    def __copy__(self):
        return eval(repr(self))
