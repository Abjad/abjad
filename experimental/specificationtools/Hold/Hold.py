from abjad.tools.abctools.AbjadObject import AbjadObject


class Hold(AbjadObject):
    r'''.. versionadded:: 1.0

    Delayed evaluation wrapper similar to Mathematica ``Hold[]``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.Hold("'red' + 3")
        Hold("'red' + 3")

    Delays evaluation of string argument until later in interpretation.

    Used primarily as arguments to slice selector start and stop keywords.

    Hold objects are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, string):
        assert isinstance(string, str), repr(string)
        self._string = string

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def string(self):
        '''String initialized by user.

        Return string.
        '''
        return self._string
