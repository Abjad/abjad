from abjad.tools.abctools import AbjadObject


class AbjadRevisionToken(AbjadObject):
    '''.. versionadded:: 2.0

    Abjad version token:

    ::

        >>> lilypondfiletools.AbjadRevisionToken()
        AbjadRevisionToken(Abjad revision ...)

    Return Abjad version token.
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
        '''Format contribution of Abjad version token:

        ::

            >>> lilypondfiletools.AbjadRevisionToken().lilypond_format
            'Abjad revision ...'

        Return string.
        '''
        from abjad import abjad_configuration
        abjad_revision_string = abjad_configuration.get_abjad_revision_string()
        return 'Abjad revision %s' % abjad_revision_string
