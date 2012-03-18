from abjad.tools.abctools import AbjadObject
import time


class DateTimeToken(AbjadObject):
    '''.. versionadded:: 2.0

    Date time token::

        abjad> lilypondfiletools.DateTimeToken()
        DateTimeToken(...)

    Return date / time token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.format)

    ### PUBLIC PROPERTIES ###

    @property
    def format(self):
        '''Format contribution of date time token::

            abjad> lilypondfiletools.DateTimeToken().format
            '...'

        Return string.
        '''
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
