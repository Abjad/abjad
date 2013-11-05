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

    def __format__(self, format_specification=''):
        r'''Gets format.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._lilypond_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        from abjad import abjad_configuration
        abjad_revision_string = abjad_configuration.get_abjad_revision_string()
        return 'Abjad revision %s' % abjad_revision_string
