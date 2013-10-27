# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class AbjadRevisionToken(AbjadObject):
    '''Abjad version token:

    ::

        >>> lilypondfiletools.AbjadRevisionToken()
        AbjadRevisionToken(Abjad revision ...)

    Returns Abjad version token.
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
        r'''Format contribution of Abjad version token:

        ::

            >>> lilypondfiletools.AbjadRevisionToken().lilypond_format
            'Abjad revision ...'

        Returns string.
        '''
        from abjad import abjad_configuration
        abjad_revision_string = abjad_configuration.get_abjad_revision_string()
        return 'Abjad revision %s' % abjad_revision_string
