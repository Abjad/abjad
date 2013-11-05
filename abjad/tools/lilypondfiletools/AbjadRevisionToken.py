# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class AbjadRevisionToken(AbjadObject):
    '''Abjad version token.

    ::

        >>> lilypondfiletools.AbjadRevisionToken()
        AbjadRevisionToken(Abjad revision ...)

    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats Abjad revision token.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self._lilypond_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        from abjad import abjad_configuration
        abjad_revision_string = abjad_configuration.get_abjad_revision_string()
        result = 'Abjad revision {}'.format(abjad_revision_string)
        return result
