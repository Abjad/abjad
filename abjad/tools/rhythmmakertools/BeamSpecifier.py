# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class BeamSpecifier(AbjadValueObject):
    r'''Beam specifier.

    ..  container:: example

        Beam notes in each cell together but do not beam between cells:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=False
            ...     )

    ..  container:: example

        Beam everything:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=True
            ...     )

    ..  container:: example

        Beam nothing:

        ::

            >>> specifier = rhythmmakertools.BeamSpecifier(
            ...     beam_each_division=True,
            ...     beam_divisions_together=True
            ...     )

    Beam specifiers are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_divisions_together',
        '_beam_each_division',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_each_division=True,
        beam_divisions_together=False,
        ):
        assert isinstance(beam_each_division, bool)
        assert isinstance(beam_divisions_together, bool)
        self._beam_each_division = beam_each_division
        self._beam_divisions_together = beam_divisions_together

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
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __hash__(self):
        r'''Hashes beam specifier.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(BeamSpecifier, self).__hash__()

    def __repr__(self):
        r'''Gets interpreter representation of beam specifier.

        ..  container:: example

            ::

                >>> rhythmmakertools.BeamSpecifier()
                BeamSpecifier(beam_each_division=True, beam_divisions_together=False)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='beam_divisions_together',
                command='bdt',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='beam_each_division',
                command='bed',
                editor=idetools.getters.get_boolean,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def beam_divisions_together(self):
        r'''Is true when target should beam cells together.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_divisions_together
                False

        Defaults to false.

        Returns boolean.
        '''
        return self._beam_divisions_together


    @property
    def beam_each_division(self):
        r'''Is true when target should beam each cell.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.BeamSpecifier()
                >>> specifier.beam_each_division
                True

        Defaults to true.

        Returns boolean.
        '''
        return self._beam_each_division