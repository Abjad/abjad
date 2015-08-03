# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class BeamSpecifier(AbjadValueObject):
    r'''Beam specifier.

    ..  container:: example

        **Example 1.** Beams notes in each cell together but does not beam 
        between cells:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=False
            ...     )

    ..  container:: example

        **Example 2.** Beams everything:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=True
            ...     )

    ..  container:: example

        **Example 3.** Beams nothing:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=False,
            ...     beam_divisions_together=False
            ...     )

    Beam specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_beam_divisions_together',
        '_beam_each_division',
        '_use_feather_beams',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_each_division=True,
        beam_divisions_together=False,
        use_feather_beams=False,
        ):
        assert isinstance(beam_each_division, bool)
        assert isinstance(beam_divisions_together, bool)
        assert isinstance(use_feather_beams, bool)
        self._beam_each_division = beam_each_division
        self._beam_divisions_together = beam_divisions_together
        self._use_feather_beams = use_feather_beams

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a beam specifier with `beam_each_division`
        and `beam_divisions_together` equal to those of this beam specifier.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier_1 = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=True,
                ...     )
                >>> specifier_2 = rhythmmakertools.BeamSpecifier(
                ...     beam_each_division=False,
                ...     )

            ::

                >>> specifier_1 == specifier_1
                True
                >>> specifier_1 == specifier_2
                False
                >>> specifier_2 == specifier_1
                False
                >>> specifier_2 == specifier_2
                True

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.beam_each_division == arg.beam_each_division and \
                self.beam_divisions_together == arg.beam_divisions_together:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats beam specifier.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> print(format(specifier))
                rhythmmakertools.BeamSpecifier(
                    beam_each_division=True,
                    beam_divisions_together=False,
                    use_feather_beams=False,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __hash__(self):
        r'''Hashes beam specifier.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(BeamSpecifier, self).__hash__()

    def __repr__(self):
        r'''Gets interpreter representation of beam specifier.

        ..  container:: example

            ::

                >>> rhythmmakertools.BeamSpecifier()
                BeamSpecifier(beam_each_division=True, beam_divisions_together=False, use_feather_beams=False)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def beam_divisions_together(self):
        r'''Is true when divisions should beam together. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_divisions_together
                False

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._beam_divisions_together


    @property
    def beam_each_division(self):
        r'''Is true when each division should be beamed. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_each_division
                True

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._beam_each_division

    @property
    def use_feather_beams(self):
        r'''Is true when multiple beams should feather. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.use_feather_beams
                False

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._use_feather_beams