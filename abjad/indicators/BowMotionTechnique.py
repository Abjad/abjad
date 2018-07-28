import typing
from abjad.system.AbjadValueObject import AbjadValueObject


class BowMotionTechnique(AbjadValueObject):
    """
    Bow motion technique.

    ..  container:: example

        Jété:

        >>> bow_motion_technique = abjad.BowMotionTechnique('jete')
        >>> abjad.f(bow_motion_technique)
        abjad.BowMotionTechnique(
            technique_name='jete',
            )

    ..  container:: example

        Ordinario:

        >>> bow_motion_technique = abjad.BowMotionTechnique('ordinario')
        >>> abjad.f(bow_motion_technique)
        abjad.BowMotionTechnique(
            technique_name='ordinario',
            )

    Valid technique names include 'ordinario', 'jeté' and 'circular'.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_technique_name',
        )

    _parameter = True

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
        technique_name: str = None,
        ) -> None:
        assert technique_name in self._valid_technique_names
        self._technique_name = technique_name

    ### PUBLIC PROPERTIES ###

    @property
    def glissando_style(self) -> str:
        """
        Gets glissando style of bow motion technique.

        ..  container:: example

            >>> abjad.BowMotionTechnique('jete').glissando_style
            'dotted-line'

        """
        if self.technique_name == 'circular':
            return 'zigzag'
        elif self.technique_name == 'jete':
            return 'dotted-line'
        return 'line'

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.BowMotionTechnique('jete').parameter
            True

        """
        return self._parameter

    @property
    def technique_name(self) -> typing.Optional[str]:
        """
        Gets technique name of bow motion technique.

        ..  container:: example

            >>> abjad.BowMotionTechnique('jete').technique_name
            'jete'

        """
        return self._technique_name

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on bow motion technique.
        """
        pass
