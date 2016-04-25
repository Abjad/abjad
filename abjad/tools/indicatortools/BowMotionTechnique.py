# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BowMotionTechnique(AbjadValueObject):
    r'''Bow motion technique.

    ..  container:: example

        **Example 1.** Jété:

        ::

            >>> bow_motion_technique = indicatortools.BowMotionTechnique('jete')
            >>> print(format(bow_motion_technique))
            indicatortools.BowMotionTechnique(
                technique_name='jete',
                )

    ..  container:: example

        **Example 2.** Ordinario:

        ::

            >>> bow_motion_technique = indicatortools.BowMotionTechnique('ordinario')
            >>> print(format(bow_motion_technique))
            indicatortools.BowMotionTechnique(
                technique_name='ordinario',
                )

    Valid technique names include 'ordinario', 'jeté' and 'circular'.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_technique_name',
        )

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
        self._default_scope = None
        assert technique_name in self._valid_technique_names
        self._technique_name = technique_name

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of bow motion technique.

        ..  container:: example

            ::

                >>> technique = indicatortools.BowMotionTechnique('jete')
                >>> technique.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

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
