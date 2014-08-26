# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class InciseSpecifier(AbjadValueObject):
    r'''Incise specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_body_ratio',
        '_fill_with_notes',
        '_outer_divisions_only',
        '_prefix_talea',
        '_prefix_lengths',
        '_suffix_talea',
        '_suffix_lengths',
        '_talea_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        prefix_talea=(-1,),
        prefix_counts=(0, 1),
        suffix_talea=(-11,),
        suffix_counts=(1,),
        talea_denominator=32,
        body_ratio=None,
        fill_with_notes=True,
        outer_divisions_only=False,
        ):
        assert self._is_integer_tuple(prefix_talea)
        self._prefix_talea = prefix_talea
        assert self._is_length_tuple(prefix_counts)
        self._prefix_lengths = prefix_counts
        assert self._is_integer_tuple(suffix_talea)
        self._suffix_talea = suffix_talea
        assert self._is_length_tuple(suffix_counts)
        self._suffix_lengths = suffix_counts
        assert mathtools.is_nonnegative_integer_power_of_two(talea_denominator)
        self._talea_denominator = talea_denominator
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self._body_ratio = body_ratio
        assert isinstance(fill_with_notes, bool)
        self._fill_with_notes = fill_with_notes
        assert isinstance(outer_divisions_only, bool)
        self._outer_divisions_only = outer_divisions_only

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
            if isinstance(expr, (tuple, list)):
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

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='prefix_talea',
                command='pt',
                editor=idetools.getters.get_nonzero_integers,
                ),
            systemtools.AttributeDetail(
                name='prefix_counts',
                command='pl',
                editor=idetools.getters.get_nonnegative_integers,
                ),
            systemtools.AttributeDetail(
                name='suffix_talea',
                command='st',
                editor=idetools.getters.get_nonzero_integers,
                ),
            systemtools.AttributeDetail(
                name='suffix_counts',
                command='sl',
                editor=idetools.getters.get_nonnegative_integers,
                ),
            systemtools.AttributeDetail(
                name='talea_denominator',
                command='td',
                editor=idetools.getters.get_positive_integer_power_of_two,
                ),
            systemtools.AttributeDetail(
                name='body_ratio',
                command='br',
                editor=idetools.getters.get_positive_integers,
                ),
            systemtools.AttributeDetail(
                name='fill_with_notes',
                command='fn',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='outer_divisions_only',
                command='oo',
                editor=idetools.getters.get_boolean,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def body_ratio(self):
        r'''Gets body ratio of incise specifier.

        ..  container:: example

            Divides middle part of every division ``1:1``:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 1],
                ...     suffix_talea=[-1],
                ...     suffix_counts=[1],
                ...     talea_denominator=16,
                ...     body_ratio=mathtools.Ratio(1, 1),
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
    def outer_divisions_only(self):
        r'''Is true when rhythm-maker should incise outer divisions only.

        Is false when rhythm-maker should incise all divisions.

        Defaults to false.

        Set to true or false.
        '''
        return self._outer_divisions_only

    @property
    def prefix_counts(self):
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
    def suffix_counts(self):
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
        prefix_counts = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.prefix_counts)
        prefix_talea = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.prefix_talea)
        suffix_counts = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.suffix_counts)
        suffix_talea = rhythmmakertools.RhythmMaker._reverse_tuple(
            self.suffix_talea)
        maker = new(
            self,
            prefix_counts=prefix_counts,
            prefix_talea=prefix_talea,
            suffix_counts=suffix_counts,
            suffix_talea=suffix_talea,
            )
        return maker

    def rotate(self, n=0):
        r'''Rotates incision specifier.

        ..  container:: example

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 2, 1],
                ...     suffix_talea=[-1, 1],
                ...     suffix_counts=[1, 0, 0],
                ...     talea_denominator=16,
                ...     body_ratio=mathtools.Ratio(1, 1),
                ...     )

            ::

                >>> print(format(incise_specifier.rotate(1)))
                rhythmmakertools.InciseSpecifier(
                    prefix_talea=(-1,),
                    prefix_counts=(1, 0, 2),
                    suffix_talea=(1, -1),
                    suffix_counts=(0, 1, 0),
                    talea_denominator=16,
                    body_ratio=mathtools.Ratio(1, 1),
                    fill_with_notes=True,
                    outer_divisions_only=False,
                    )

        Returns new incision specifier.
        '''
        from abjad.tools import rhythmmakertools
        prefix_counts = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.prefix_counts, n)
        prefix_talea = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.prefix_talea, n)
        suffix_counts = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.suffix_counts, n)
        suffix_talea = rhythmmakertools.RhythmMaker._rotate_tuple(
            self.suffix_talea, n)
        maker = new(
            self,
            prefix_counts=prefix_counts,
            prefix_talea=prefix_talea,
            suffix_counts=suffix_counts,
            suffix_talea=suffix_talea,
            )
        return maker