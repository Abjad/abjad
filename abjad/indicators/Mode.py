from .. import format as _format
from .. import sequence as _sequence
from ..pitch.intervals import NamedInterval
from ..pitch.segments import IntervalSegment


class Mode:
    """
    Mode.

    ..  container:: example

        Initializes from string:

        >>> abjad.Mode('major')
        Mode('major')

    ..  container:: example

        Initializes from other mode:

        >>> mode = abjad.Mode('dorian')
        >>> abjad.Mode(mode)
        Mode('dorian')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_named_interval_segment", "_mode_name")

    ### INITIALIZER ###

    def __init__(self, mode_name="dorian"):
        if isinstance(mode_name, str):
            mode_name = mode_name
        elif isinstance(mode_name, Mode):
            mode_name = mode_name.mode_name
        else:
            raise TypeError(f"must be mode or mode name: {mode_name!r}.")
        mdi_segment = self._initialize_with_mode_name(mode_name)
        self._named_interval_segment = mdi_segment
        self._mode_name = mode_name

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a mode with mode name equal to that of
        this mode.

        ..  container:: example

            >>> mode_1 = abjad.Mode('major')
            >>> mode_2 = abjad.Mode('major')
            >>> mode_3 = abjad.Mode('dorian')

            >>> mode_1 == mode_1
            True
            >>> mode_1 == mode_2
            True
            >>> mode_1 == mode_3
            False

            >>> mode_2 == mode_1
            True
            >>> mode_2 == mode_2
            True
            >>> mode_2 == mode_3
            False

            >>> mode_3 == mode_1
            False
            >>> mode_3 == mode_2
            False
            >>> mode_3 == mode_3
            True

        Returns true or false.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes mode.

        Returns integer.
        """
        return hash(self.__class__.__name__ + str(self))

    def __len__(self):
        """
        Length of mode.

        ..  container:: example

            >>> len(abjad.Mode('dorian'))
            7

        Returns nonnegative integer.
        """
        return len(self.named_interval_segment)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        """
        String representation of mode.

        ..  container:: example

            >>> str(abjad.Mode('dorian'))
            'dorian'

        Returns string.
        """
        return self.mode_name

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.mode_name]
        return _format.FormatSpecification(
            storage_format_is_not_indented=True,
            storage_format_args_values=values,
        )

    def _initialize_with_mode_name(self, mode_name):
        mdi_segment = []
        m2 = NamedInterval("m2")
        M2 = NamedInterval("M2")
        A2 = NamedInterval("aug2")
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if mode_name == "dorian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=0))
        elif mode_name == "phrygian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-1))
        elif mode_name == "lydian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-2))
        elif mode_name == "mixolydian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-3))
        elif mode_name in ("aeolian", "minor", "natural minor"):
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-4))
        elif mode_name == "locrian":
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-5))
        elif mode_name in ("ionian", "major"):
            mdi_segment.extend(_sequence.Sequence(dorian).rotate(n=-6))
        elif mode_name == "melodic minor":
            mdi_segment.extend([M2, m2, M2, M2, M2, M2, m2])
        elif mode_name == "harmonic minor":
            mdi_segment.extend([M2, m2, M2, M2, m2, A2, m2])
        else:
            raise ValueError(f"unknown mode name: {mode_name!r}.")
        return IntervalSegment(items=mdi_segment, item_class=NamedInterval)

    ### PUBLIC PROPERTIES ###

    @property
    def mode_name(self):
        """
        Gets mode name.

        ..  container:: example

            >>> abjad.Mode('major').mode_name
            'major'

            >>> abjad.Mode('dorian').mode_name
            'dorian'

        Returns string.
        """
        return self._mode_name

    @property
    def named_interval_segment(self):
        """
        Gets named interval segment.

        ..  container:: example

            >>> mode = abjad.Mode('major')
            >>> str(mode.named_interval_segment)
            '<+M2, +M2, +m2, +M2, +M2, +M2, +m2>'

            >>> mode = abjad.Mode('dorian')
            >>> str(mode.named_interval_segment)
            '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'

        Returns named interval segment.
        """
        return self._named_interval_segment
