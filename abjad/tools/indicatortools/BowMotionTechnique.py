# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BowMotionTechnique(AbjadValueObject):
    r'''Bow motion technique.

    ..  container:: example

        >>> bow_motion_technique = indicatortools.BowMotionTechnique('jete')
        >>> print(format(bow_motion_technique))
        indicatortools.BowMotionTechnique(
            technique_name='jete',
            )

    Valid technique names include 'ordinario', 'jeté' and 'circular'.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
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
        assert technique_name in self._valid_technique_names
        self._technique_name = technique_name

    ### PUBLIC PROPERTIES ###

    @property
    def glissando_style(self):
        r'''Gets glissando style.

        Returns string.
        '''
        if self.technique_name == 'circular':
            return 'zigzag'
        elif self.technique_name == 'jete':
            return 'dotted-line'
        return 'line'

    @property
    def technique_name(self):
        r'''Gets technique name.

        Returns string.
        '''
        return self._technique_name