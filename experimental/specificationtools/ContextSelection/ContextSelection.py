from abjad.tools import contexttools
from experimental.specificationtools.Selection.Selection import Selection


class ContextSelection(Selection):
    r'''.. versionadded:: 1.0

    Exactly one context taken over arbitrary timespan.
    '''

    ### INITIALIZER ###

    def __init__(self, context, timespan=None):
        assert isinstance(context, (str, contexttools.Context)), repr(context)
        Selection.__init__(self, [context], timespan=timespan)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context(self):
        '''Name of context selection context specified by user.

        Return string.
        '''
        return self.contexts[0]
