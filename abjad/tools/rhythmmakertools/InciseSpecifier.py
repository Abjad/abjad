from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject


class InciseSpecifier(AbjadValueObject):
    r'''Incise specifier.

    ..  container:: example

        Specifies one sixteenth rest cut out of the beginning of every
        division:

        ::

            >>> specifier = abjad.rhythmmakertools.InciseSpecifier(
            ...     prefix_talea=[-1],
            ...     prefix_counts=[1],
            ...     talea_denominator=16,
            ...     )

    ..  container:: example

        Specifies sixteenth rests cut out of the beginning and end of each
        division:

        ::

            >>> specifier = abjad.rhythmmakertools.InciseSpecifier(
            ...     prefix_talea=[-1],
            ...     prefix_counts=[1],
            ...     suffix_talea=[-1],
            ...     suffix_counts=[1],
            ...     talea_denominator=16,
            ...     )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

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

    _publish_storage_format = True

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
        outer_divisions_only=None,
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
        assert isinstance(outer_divisions_only, (bool, type(None)))
        self._outer_divisions_only = outer_divisions_only

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats incise specifier.

        ..  container:: example

            Formats incise specifier:

            ::

                >>> specifier = abjad.rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[1],
                ...     talea_denominator=16,
                ...     )

            ::

                >>> f(specifier)
                abjad.rhythmmakertools.InciseSpecifier(
                    prefix_talea=[-1],
                    prefix_counts=[1],
                    talea_denominator=16,
                    )

        ..  container:: example

            Formats incise specifier:

            ::

                >>> specifier = abjad.rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 1],
                ...     suffix_talea=[-1],
                ...     suffix_counts=[1],
                ...     talea_denominator=16,
                ...     )

            ::

                >>> f(specifier)
                abjad.rhythmmakertools.InciseSpecifier(
                    prefix_talea=[-1],
                    prefix_counts=[0, 1],
                    suffix_talea=[-1],
                    suffix_counts=[1],
                    talea_denominator=16,
                    )

        Returns string.
        '''
        superclass = super(InciseSpecifier, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        for name in names[:]:
            if name == 'talea_denominator':
                continue
            if not getattr(self, name):
                names.remove(name)
        # TODO: keywords defaults checking
        if self.fill_with_notes:
            names.remove('fill_with_notes')
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    @staticmethod
    def _is_integer_tuple(argument):
        if argument is None:
            return True
        if all(isinstance(x, int) for x in argument):
            return True
        return False

    @staticmethod
    def _is_length_tuple(argument):
        if argument is None:
            return True
        if mathtools.all_are_nonnegative_integer_equivalent_numbers(argument):
            if isinstance(argument, (tuple, list)):
                return True
        return False

    @staticmethod
    def _reverse_tuple(argument):
        if argument is not None:
            return tuple(reversed(argument))

    @staticmethod
    def _rotate_tuple(argument, n):
        import abjad
        if argument is not None:
            return tuple(abjad.sequence(argument).rotate(n=n))

    ### PUBLIC PROPERTIES ###

    @property
    def body_ratio(self):
        r'''Gets body ratio.

        ..  container:: example

            Divides middle part of every division ``1:1``:

            ::

                >>> specifier = abjad.rhythmmakertools.InciseSpecifier(
                ...     prefix_talea=[-1],
                ...     prefix_counts=[0, 1],
                ...     suffix_talea=[-1],
                ...     suffix_counts=[1],
                ...     talea_denominator=16,
                ...     body_ratio=abjad.Ratio((1, 1)),
                ...     )
                >>> rhythm_maker = abjad.rhythmmakertools.IncisedRhythmMaker(
                ...     incise_specifier=specifier,
                ...     )

            ::

                >>> divisions = 4 * [(5, 16)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
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

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._outer_divisions_only

    @property
    def prefix_counts(self):
        r'''Gets prefix counts.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        if self._prefix_counts:
            return list(self._prefix_counts)

    @property
    def prefix_talea(self):
        r'''Gets prefix talea.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        if self._prefix_talea:
            return list(self._prefix_talea)

    @property
    def suffix_counts(self):
        r'''Gets suffix counts.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        if self._suffix_counts:
            return list(self._suffix_counts)

    @property
    def suffix_talea(self):
        r'''Gets suffix talea.

        ..  todo:: Add examples.

        Returns tuple or none.
        '''
        if self._suffix_talea:
            return list(self._suffix_talea)

    @property
    def talea_denominator(self):
        r'''Gets talea denominator.

        ..  todo:: Add examples.

        Returns positive integer-equivalent number.
        '''
        return self._talea_denominator
