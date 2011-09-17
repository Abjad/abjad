from abjad.core import _Immutable
import time


class DateTimeToken(_Immutable):
    '''.. versionadded:: 2.0

    Date time token::

        abjad> lilypondfiletools.DateTimeToken()
        DateTimeToken(...)

    Return date / time token.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.format)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Format contribution of date time token::

            abjad> lilypondfiletools.DateTimeToken().format
            '...'

        Return string.
        '''
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
