# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class InciseSpecifier(AbjadValueObject):
    r'''Incise specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_body_ratio',
        '_fill_with_notes',
        '_outer_divisions_only',
        '_prefix_counts',
        '_prefix_talea',
        '_suffix_counts',
        '_suffix_talea',
        '_talea_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        prefix_talea=None,
        prefix_counts=None,
        suffix_talea=None,
        suffix_counts=None,
        talea_denominator=None,
        body_ratio=None,
        fill_with_notes=True,
        outer_divisions_only=False,
        ):
        prefix_talea = prefix_talea or ()
        prefix_talea = tuple(prefix_talea)
        assert self._is_integer_tuple(prefix_talea)
        self._prefix_talea = prefix_talea
        prefix_counts = prefix_counts or ()
        prefix_counts = tuple(prefix_counts)
        assert self._is_length_tuple(prefix_counts)
        self._prefix_counts = prefix_counts
        if prefix_counts and prefix_counts != (0,):
            assert prefix_talea
        if prefix_talea:
            assert prefix_counts
        suffix_talea = suffix_talea or ()
        suffix_talea = tuple(suffix_talea)
        assert self._is_integer_tuple(suffix_talea)
        self._suffix_talea = suffix_talea
        assert self._is_length_tuple(suffix_counts)
        suffix_counts = suffix_counts or ()
        suffix_counts = tuple(suffix_counts)
        self._suffix_counts = suffix_counts
        if suffix_counts and suffix_counts != (0,):
            assert suffix_talea
        if suffix_talea:
            assert suffix_counts
        if talea_denominator is not None:
            if not mathtools.is_nonnegative_integer_power_of_two(
                talea_denominator):
                message = 'talea denominator {!r} must be nonnegative'
                message += ' integer power of 2.'
                message = message.format(talea_denominator)
                raise Exception(message)
        self._talea_denominator = talea_denominator
        if prefix_talea or suffix_talea:
            assert talea_denominator is not None
        if body_ratio is not None:
            body_ratio = mathtools.Ratio(body_ratio)
        self._body_ratio = body_ratio
        assert isinstance(fill_with_notes, bool)
        self._fill_with_notes = fill_with_notes
        assert isinstance(outer_divisions_only, bool)
        self._outer_divisions_only = outer_divisions_only

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats incise specifier.

        ..  container:: example

            **Example 1.**

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 1],
                ...     suffix_talea=[-1],
                ...     suffix_counts=[1],
                ...     talea_denominator=16,
                ...     )

            ::

                >>> print(format(incise_specifier))
                rhythmmakertools.InciseSpecifier(
                    prefix_talea=(-1,),
                    prefix_counts=(0, 1),
                    suffix_talea=(-1,),
                    suffix_counts=(1,),
                    talea_denominator=16,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if not self.prefix_talea: 
            keyword_argument_names.remove('prefix_talea')
        if not self.prefix_counts:
            keyword_argument_names.remove('prefix_counts')
        if not self.suffix_talea:
            keyword_argument_names.remove('suffix_talea')
        if not self.suffix_counts:
            keyword_argument_names.remove('suffix_counts')
        if self.body_ratio is None:
            keyword_argument_names.remove('body_ratio')
        if self.fill_with_notes == True:
            keyword_argument_names.remove('fill_with_notes')
        if self.outer_divisions_only == False:
            keyword_argument_names.remove('outer_divisions_only')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

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
        from ide import idetools
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

            **Example 1.** Divides middle part of every division ``1:1``:

            ::

                >>> incise_specifier = rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 1],
                ...     suffix_talea=[-1],
                ...     suffix_counts=[1],
                ...     talea_denominator=16,
                ...     body_ratio=mathtools.Ratio((1, 1)),
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

        ..  todo:: Add examples.

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._fill_with_notes

    @property
    def outer_divisions_only(self):
        r'''Is true when rhythm-maker should incise outer divisions only.
        Is false when rhythm-maker should incise all divisions.

        ..  todo:: Add examples.

        Defaults to false.

        Set to true or false.
        
        Returns true or false.
        '''
        return self._outer_divisions_only

    @property
    def prefix_counts(self):
        r'''Gets prefix lengths of incision specifier.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        return self._prefix_counts

    @property
    def prefix_talea(self):
        r'''Gets prefix talea of incision specifier.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        return self._prefix_talea

    @property
    def suffix_counts(self):
        r'''Gets suffix lengths of incision specifier.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        return self._suffix_counts

    @property
    def suffix_talea(self):
        r'''Gets suffix talea of incision specifier.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        return self._suffix_talea

    @property
    def talea_denominator(self):
        r'''Gets talea denominator of incision specifier.

        ..  todo:: Add examples.

        Returns positive integer-equivalent number.
        '''
        return self._talea_denominator