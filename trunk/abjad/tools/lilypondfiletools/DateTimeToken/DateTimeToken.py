from abjad.tools.abctools import AbjadObject
import time


class DateTimeToken(AbjadObject):
    '''.. versionadded:: 2.0

    Date time token:

    ::

        >>> lilypondfiletools.DateTimeToken()
        DateTimeToken(...)

    Return date / time token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self.lilypond_format)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Format contribution of date time token:

        ::

            >>> lilypondfiletools.DateTimeToken().lilypond_format
            '...'

        Return string.
        '''
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
