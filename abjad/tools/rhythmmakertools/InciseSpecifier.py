# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class InciseSpecifier(AbjadValueObject):
    r'''Incision specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_body_ratio',
        '_fill_with_notes',
        '_incise_divisions',
        '_incise_output',
        '_prefix_talea',
        '_prefix_lengths',
        '_suffix_talea',
        '_suffix_lengths',
        '_talea_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        incise_divisions=False,
        incise_output=False,
        prefix_talea=(-1,),
        prefix_lengths=(0, 1),
        suffix_talea=(-11,),
        suffix_lengths=(1,),
        talea_denominator=32,
        body_ratio=None,
        fill_with_notes=True,
        ):
        assert isinstance(incise_divisions, bool)
        self._incise_divisions = incise_divisions
        assert isinstance(incise_output, bool)
        self._incise_output = incise_output
        assert self._is_integer_tuple(prefix_talea)
        self._prefix_talea = prefix_talea
        assert self._is_length_tuple(prefix_lengths)
        self._prefix_lengths = prefix_lengths
        assert self._is_integer_tuple(suffix_talea)
        self._suffix_talea = suffix_talea
        assert self._is_length_tuple(suffix_lengths)
        self._suffix_lengths = suffix_lengths
        assert mathtools.is_nonnegative_integer_power_of_two(talea_denominator)
        self._talea_denominator = talea_denominator
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self._body_ratio = body_ratio
        assert isinstance(fill_with_notes, bool)
        self._fill_with_notes = fill_with_notes

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_integer_tuple(expr):
        if expr is None:
            return True
        if all(isinstance(x, int) for x in expr):
            return True
        return False

    @staticmethod
    def _is_length_tuple(expr):
        if expr is None:
            return True
        if mathtools.all_are_nonnegative_integer_equivalent_numbers(expr):
            if isinstance(expr, tuple):
                return True
        return False

    @staticmethod
    def _reverse_tuple(expr):
        if expr is not None:
            return tuple(reversed(expr))

    @staticmethod
    def _rotate_tuple(expr, n):
        if expr is not None:
            return tuple(sequencetools.rotate_sequence(expr, n))

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def body_ratio(self):
        r'''Gets body ratio of incise specifier.

        ..  container:: example

            Sets `body_ratio` to divide middle part proportionally:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     incise_divisions=True,
                ...     prefix_talea=(-1,),
                ...     prefix_lengths=(0, 1),
                ...     suffix_talea=(-1,),
                ...     suffix_lengths=(1,),
                ...     talea_denominator=16,
                ...     body_ratio=(1, 1),
                ...     )
                >>> maker = rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=incise_specifier,
                ...     )

            ::

                >>> divisions = 4 * [(5, 16)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/16
                        c'8 [
                        c'8 ]
                        r16
                    }
                    {
                        r16
                        c'16. [
                        c'16. ]
                        r16
                    }
                    {
                        c'8 [
                        c'8 ]
                        r16
                    }
                    {
                        r16
                        c'16. [
                        c'16. ]
                        r16
                    }
                }

        Defaults to none.

        Returns ratio or none.
        '''
        return self._body_ratio

    @property
    def fill_with_notes(self):
        r'''Is true when rhythm-maker should fill divisions with notes.
        Otherwise false.

        Defaults to true.

        Returns boolean.
        '''
        return self._fill_with_notes

    @property
    def incise_divisions(self):
        r'''Is true when rhythm-maker should incise every division.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._incise_divisions

    @property
    def incise_output(self):
        r'''Is true when rhythm-maker should incise first and last divisions.
        Otherwise false.

        Defaults to false.

        Returns boolean.
        '''
        return self._incise_output

    @property
    def prefix_lengths(self):
        r'''Gets prefix lengths of incision specifier.

        Returns tuple or none.
        '''
        return self._prefix_lengths

    @property
    def prefix_talea(self):
        r'''Gets prefix talea of incision specifier.

        Returns tuple or none.
        '''
        return self._prefix_talea

    @property
    def suffix_lengths(self):
        r'''Gets suffix lengths of incision specifier.

        Returns tuple or none.
        '''
        return self._suffix_lengths

    @property
    def suffix_talea(self):
        r'''Gets suffix talea of incision specifier.

        Returns tuple or none.
        '''
        return self._suffix_talea

    @property
    def talea_denominator(self):
        r'''Gets talea denominator of incision specifier.

        Returns positive integer-equivalent number.
        '''
        return self._talea_denominator

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses incision specifier.

        Returns new incision specifier.
        '''
        from abjad.tools import rhythmmakertools
        prefix_lengths = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.prefix_lengths)
        prefix_talea = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.prefix_talea)
        suffix_lengths = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.suffix_lengths)
        suffix_talea = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.suffix_talea)
        maker = new(
            self,
            prefix_lengths=prefix_lengths,
            prefix_talea=prefix_talea,
            suffix_lengths=suffix_lengths,
            suffix_talea=suffix_talea,
            )
        return maker

    def rotate(self, n=0):
        r'''Rotates incision specifier.

        ..  container:: example

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     incise_divisions=True,
                ...     prefix_talea=(-1,),
                ...     prefix_lengths=(0, 2, 1),
                ...     suffix_talea=(-1, 1),
                ...     suffix_lengths=(1, 0, 0),
                ...     talea_denominator=16,
                ...     body_ratio=(1, 1),
                ...     )

            ::

                >>> print(format(incise_specifier.rotate(1)))
                rhythmmakertools.InciseSpecifier(
                    incise_divisions=True,
                    incise_output=False,
                    prefix_talea=(-1,),
                    prefix_lengths=(1, 0, 2),
                    suffix_talea=(1, -1),
                    suffix_lengths=(0, 1, 0),
                    talea_denominator=16,
                    body_ratio=mathtools.Ratio(1, 1),
                    fill_with_notes=True,
                    )

        Returns new incision specifier.
        '''
        from abjad.tools import rhythmmakertools
        prefix_lengths = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.prefix_lengths, n)
        prefix_talea = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.prefix_talea, n)
        suffix_lengths = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.suffix_lengths, n)
        suffix_talea = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.suffix_talea, n)
        maker = new(
            self,
            prefix_lengths=prefix_lengths,
            prefix_talea=prefix_talea,
            suffix_lengths=suffix_lengths,
            suffix_talea=suffix_talea,
            )
        return maker
