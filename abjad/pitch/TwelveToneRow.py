from abjad.top.new import new
from .PitchClassSegment import PitchClassSegment


class TwelveToneRow(PitchClassSegment):
    """
    Twelve-tone row.

    ..  container:: example

        Initializes from defaults:

        >>> row = abjad.TwelveToneRow()
        >>> abjad.show(row) # doctest: +SKIP

    ..  container:: example

        Initializes from integers:

        >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
        >>> row = abjad.TwelveToneRow(numbers)
        >>> abjad.show(row) # doctest: +SKIP

    ..  container:: example

        Interpreter representation:

        >>> row
        TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)):
        import abjad
        assert items is not None
        PitchClassSegment.__init__(
            self,
            items=items,
            item_class=abjad.NumberedPitchClass,
            )
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __call__(self, pitch_classes):
        r"""
        Calls row on `pitch_classes`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Permutes pitch-classes:

            >>> row([abjad.NumberedPitchClass(2)])
            [NumberedPitchClass(9)]

            >>> row([abjad.NumberedPitchClass(3)])
            [NumberedPitchClass(3)]

            >>> row([abjad.NumberedPitchClass(4)])
            [NumberedPitchClass(6)]

        ..  container:: example

            Permutes pitch-class segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment = abjad.PitchClassSegment(items=items)
            >>> abjad.show(segment) # doctest: +SKIP

            >>> segment_ = row(segment)
            >>> abjad.show(segment_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    af'8
                    c'8
                    f'8
                    e'8
                    c'8
                    e'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row_2) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_2.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> abjad.show(row_3) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_3.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row_2) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_2.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    b'8
                    bf'8
                    a'8
                    af'8
                    g'8
                    fs'8
                    f'8
                    e'8
                    ef'8
                    d'8
                    cs'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> abjad.show(row_3) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_3.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Permutes row:

            >>> numbers = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
            >>> row_2 = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row_2) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_2.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    c'8
                    d'8
                    fs'8
                    af'8
                    g'8
                    f'8
                    ef'8
                    cs'8
                    a'8
                    e'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> row_3 = row(row_2)
            >>> abjad.show(row_3) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row_3.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    af'8
                    cs'8
                    a'8
                    f'8
                    bf'8
                    e'8
                    g'8
                    ef'8
                    b'8
                    d'8
                    fs'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns permuted pitch-classes in object of type `pitch_classes`.
        """
        import abjad
        new_pitch_classes = []
        for pitch_class in pitch_classes:
            pitch_class = abjad.NumberedPitchClass(pitch_class)
            i = pitch_class.number
            new_pitch_class = self[i]
            new_pitch_classes.append(new_pitch_class)
        result = type(pitch_classes)(new_pitch_classes)
        return result

    def __getitem__(self, argument):
        r"""
        Gets item or slice identified by `argument`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Gets first hexachord:

            >>> abjad.show(row[:6]) # doctest: +SKIP
            PitchClassSegment([0, 1, 11, 9, 3, 6])

            ..  docs::

                >>> lilypond_file = row[:6].__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets second hexachord:

            >>> abjad.show(row[-6:]) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row[-6:].__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> row[-6:]
            PitchClassSegment([5, 4, 10, 2, 8, 0])

        """
        import abjad
        item = self._collection.__getitem__(argument)
        try:
            return PitchClassSegment(
                items=item,
                item_class=abjad.NumberedPitchClass,
                )
        except TypeError:
            return item

    def __illustrate__(self, **keywords):
        r"""
        Illustrates row.

        ..  container:: example

            Illustrates row:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }


        ..  container:: example

            Illustrates row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = row.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns LilyPond file:

            >>> type(row.__illustrate__())
            <class 'abjad.lilypondfile.LilyPondFile.LilyPondFile'>

        """
        return super().__illustrate__(**keywords)

    def __mul__(self, argument):
        r"""
        Multiplies row by `argument`.

        ..  container:: example

            Multiplies row:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP

            >>> segment = 2 * row
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            >>> segment = 2 * row
            >>> abjad.show(segment) # doctest: +SKIP


            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        Returns pitch-class segment.
        """
        return PitchClassSegment(self) * argument

    def __rmul__(self, argument):
        r"""
        Multiplies `argument` by row.

        ..  container:: example

            Multiplies integer by row:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP

            >>> segment = row * 2
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                    fs'8
                    g'8
                    af'8
                    a'8
                    bf'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies integer by row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            >>> segment = row * 2
            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            >>> segment
            PitchClassSegment([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return PitchClassSegment(self) * argument

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ', '.join([str(abs(pc)) for pc in self])

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = 'must contain all twelve pitch-classes: {!r}.'
            message = message.format(pitch_classes)
            raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets item class of row.

        ..  container:: example

            Gets item class:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP

            >>> row.item_class
            <class 'abjad.pitch.NumberedPitchClass.NumberedPitchClass'>

        ..  container:: example

            Gets item class:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            >>> row.item_class
            <class 'abjad.pitch.NumberedPitchClass.NumberedPitchClass'>

        ..  container:: example

            Returns numbered pitch-class class:

            >>> type(row.item_class)
            <class 'abc.ABCMeta'>

        """
        return super().item_class

    @property
    def items(self):
        """
        Gets items in row.

        ..  container:: example

            Gets items in row:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP


            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(0)
            NumberedPitchClass(1)
            NumberedPitchClass(2)
            NumberedPitchClass(3)
            NumberedPitchClass(4)
            NumberedPitchClass(5)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(8)
            NumberedPitchClass(9)
            NumberedPitchClass(10)
            NumberedPitchClass(11)

        ..  container:: example

            Gets items in row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            >>> for item in row.items:
            ...     item
            ...
            NumberedPitchClass(1)
            NumberedPitchClass(11)
            NumberedPitchClass(9)
            NumberedPitchClass(3)
            NumberedPitchClass(6)
            NumberedPitchClass(7)
            NumberedPitchClass(5)
            NumberedPitchClass(4)
            NumberedPitchClass(10)
            NumberedPitchClass(2)
            NumberedPitchClass(8)
            NumberedPitchClass(0)

        ..  container:: example

            Returns list:

            >>> isinstance(row.items, list)
            True

        """
        return super().items

    ### PUBLIC METHODS ###

    def count(self, item):
        """
        Counts `item` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Counts pitch-class 11 in row:

            >>> row.count(11)
            1

        ..  container:: example

            Counts pitch-class 9 in row:

            >>> row.count(9)
            1

        ..  container:: example

            Counts string in row:

            >>> row.count('text')
            0

        ..  container:: example

            Returns nonnegative integer equal to 0 or 1:

            >>> isinstance(row.count('text'), int)
            True

        """
        return super().count(item)

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes row from `selection`.

        Not yet implemented.

        Returns twelve-tone row.
        """
        raise NotImplementedError

    def has_duplicates(self):
        """
        Is false for all rows.

        ..  container:: example

            Is false:

            >>> row = abjad.TwelveToneRow()
            >>> abjad.show(row) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        ..  container:: example

            Is false:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

            >>> row.has_duplicates()
            False

        Twelve-tone rows have no duplicates.

        Returns false.
        """
        return super().has_duplicates()

    def index(self, item):
        """
        Gets index of `item` in row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Gets index of pitch-class 11:

            >>> row.index(11)
            1

        ..  container:: example

            Gets index of pitch-class 9:

            >>> row.index(9)
            2

        ..  container:: example

            Returns nonnegative integer less than 12:

            >>> isinstance(row.index(9), int)
            True

        """
        return super().index(item)

    def invert(self, axis=None):
        r"""
        Inverts row about optional `axis`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Inverts row about first pitch-class when `axis` is none:

            >>> inversion = row.invert()
            >>> abjad.show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            First pitch-classes are equal:

            >>> row[0] == inversion[0]
            True

        ..  container:: example

            Inverts row about pitch-class 1:

            >>> inversion = row.invert(axis=1)
            >>> abjad.show(inversion) # doctest: +SKIP
            TwelveToneRow([1, 3, 5, 11, 8, 7, 9, 10, 4, 0, 6, 2])

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    ef'8
                    f'8
                    b'8
                    af'8
                    g'8
                    a'8
                    bf'8
                    e'8
                    c'8
                    fs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            Same result as above.

        ..  container:: example

            Inverts row about pitch-class 0:

            >>> inversion = row.invert(axis=0)
            >>> abjad.show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    b'8
                    cs'8
                    ef'8
                    a'8
                    fs'8
                    f'8
                    g'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts row about pitch-class 5:

            >>> inversion = row.invert(axis=5)
            >>> abjad.show(inversion) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    a'8
                    b'8
                    cs'8
                    g'8
                    e'8
                    ef'8
                    f'8
                    fs'8
                    c'8
                    af'8
                    d'8
                    bf'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns twelve-tone row:

            >>> inversion
            TwelveToneRow([9, 11, 1, 7, 4, 3, 5, 6, 0, 8, 2, 10])

        """
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return new(self, items=items)

    def multiply(self, n=1):
        r"""
        Multiplies pitch-classes in row by `n`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in row by 5:

            >>> multiplication = row.multiply(n=5)
            >>> abjad.show(multiplication) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = multiplication.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    f'8
                    g'8
                    a'8
                    ef'8
                    fs'8
                    b'8
                    cs'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 7:

            >>> multiplication = row.multiply(n=7)
            >>> abjad.show(multiplication) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = multiplication.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    g'8
                    f'8
                    ef'8
                    a'8
                    fs'8
                    cs'8
                    b'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in row by 1:

            >>> multiplication = row.multiply(n=1)
            >>> abjad.show(multiplication) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = multiplication.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns twelve-tone row:

            >>> multiplication
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().multiply(n=n)

    def retrograde(self):
        r"""
        Gets retrograde of row.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of row:

            >>> retrograde = row.retrograde()
            >>> abjad.show(retrograde) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = retrograde.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    af'8
                    d'8
                    bf'8
                    e'8
                    f'8
                    g'8
                    fs'8
                    ef'8
                    a'8
                    b'8
                    cs'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of row:

            >>> retrograde = row.retrograde().retrograde()
            >>> abjad.show(retrograde) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = retrograde.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> retrograde == row
            True

        ..  container:: example

            Returns row:

            >>> retrograde
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().retrograde()

    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates row by index `n`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Rotates row to the right:

            >>> rotation = row.rotate(n=1)
            >>> abjad.show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row to the left:

            >>> rotation = row.rotate(n=-1)
            >>> abjad.show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    cs'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates row by zero:

            >>> rotation = row.rotate(n=0)
            >>> abjad.show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> rotation == row
            True

        ..  container:: example

            Stravinsky-style rotation back-transposes row to zero:

            >>> rotation = row.rotate(n=-1, stravinsky=True)
            >>> abjad.show(rotation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    d'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns row:

            >>> rotation
            TwelveToneRow([0, 10, 4, 7, 8, 6, 5, 11, 3, 9, 1, 2])

        """
        return super().rotate(n=n, stravinsky=stravinsky)

    def transpose(self, n=0):
        r"""
        Transposes row by index `n`.

        ..  container:: example

            Example row:

            >>> numbers = [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
            >>> row = abjad.TwelveToneRow(numbers)
            >>> abjad.show(row) # doctest: +SKIP

        ..  container:: example

            Transposes row by positive index:

            >>> transposition = row.transpose(n=13)
            >>> abjad.show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    d'8
                    c'8
                    bf'8
                    e'8
                    g'8
                    af'8
                    fs'8
                    f'8
                    b'8
                    ef'8
                    a'8
                    cs'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by negative index:

            >>> transposition = row.transpose(n=-13)
            >>> abjad.show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    c'8
                    bf'8
                    af'8
                    d'8
                    f'8
                    fs'8
                    e'8
                    ef'8
                    a'8
                    cs'8
                    g'8
                    b'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes row by zero index:

            >>> transposition = row.transpose(n=0)
            >>> abjad.show(transposition) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    cs'8
                    b'8
                    a'8
                    ef'8
                    fs'8
                    g'8
                    f'8
                    e'8
                    bf'8
                    d'8
                    af'8
                    c'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

            >>> transposition == row
            True

        ..  container:: example

            Returns row:

            >>> transposition
            TwelveToneRow([1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0])

        """
        return super().transpose(n=n)
