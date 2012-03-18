from abjad.tools.abctools import AbjadObject
from abjad.tools.configurationtools.get_abjad_revision_string import get_abjad_revision_string


class AbjadRevisionToken(AbjadObject):
    '''.. versionadded:: 2.0

    Abjad version token::

        abjad> lilypondfiletools.AbjadRevisionToken()
        AbjadRevisionToken(Abjad revision ...)

    Return Abjad version token.
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
        '''Format contribution of Abjad version token::

            abjad> lilypondfiletools.AbjadRevisionToken().format
            'Abjad revision ...'

        Return string.
        '''
        abjad_revision_string = get_abjad_revision_string()
        return 'Abjad revision %s' % abjad_revision_string
