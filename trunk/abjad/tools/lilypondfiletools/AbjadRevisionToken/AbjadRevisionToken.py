from abjad.core import _Immutable
from abjad.tools.configurationtools.get_abjad_revision_string import get_abjad_revision_string


class AbjadRevisionToken(_Immutable):
    '''.. versionadded:: 2.0

    Abjad version token::

        abjad> lilypondfiletools.AbjadRevisionToken()
        AbjadRevisionToken(Abjad revision ...)

    Return Abjad version token.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.format)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Format contribution of Abjad version token::

            abjad> lilypondfiletools.AbjadRevisionToken().format
            'Abjad revision ...'

        Return string.
        '''
        abjad_revision_string = get_abjad_revision_string()
        return 'Abjad revision %s' % abjad_revision_string
