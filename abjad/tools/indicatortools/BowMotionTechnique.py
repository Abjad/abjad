# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BowMotionTechnique(AbjadValueObject):
    r'''Bow motion technique.

    ::

        >>> import abjad

    ..  container:: example

        Jété:

        ::

            >>> bow_motion_technique = abjad.BowMotionTechnique('jete')
            >>> f(bow_motion_technique)
            abjad.BowMotionTechnique(
                technique_name='jete',
                )

    ..  container:: example

        Ordinario:

        ::

            >>> bow_motion_technique = abjad.BowMotionTechnique('ordinario')
            >>> f(bow_motion_technique)
            abjad.BowMotionTechnique(
                technique_name='ordinario',
                )

    Valid technique names include 'ordinario', 'jeté' and 'circular'.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_technique_name',
        )

    _publish_storage_format = True

    _valid_technique_names = (
        'circular',
        'jete',
        'ordinario',
        None,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        technique_name=None,
        ):
        assert technique_name in self._valid_technique_names
        self._technique_name = technique_name

    ### PUBLIC PROPERTIES ###

    @property
    def glissando_style(self):
        r'''Gets glissando style of bow motion technique.

        Returns string.
        '''
        if self.technique_name == 'circular':
            return 'zigzag'
        elif self.technique_name == 'jete':
            return 'dotted-line'
        return 'line'

    @property
    def technique_name(self):
        r'''Gets technique name of bow motion technique.

        Returns string.
        '''
        return self._technique_name
