from abjad.core import _Immutable
import time


class DateTimeToken(_Immutable):
    '''.. versionadded:: 2.0

    Date time token::

        abjad> lilyfiletools.DateTimeToken( )
        DateTimeToken(...)

    Return date / time token.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.format)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Format contribution of date time token::

            abjad> lilyfiletools.DateTimeToken( ).format
            '...'

        Return string.
        '''
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
