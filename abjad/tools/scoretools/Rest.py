from .Leaf import Leaf


class Rest(Leaf):
    r"""
    Rest.

    ..  container:: example

        >>> rest = abjad.Rest('r8.')
        >>> measure = abjad.Measure((3, 16), [rest])
        >>> abjad.show(measure) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(measure)
            {   % measure
                \time 3/16
                r8.
            }   % measure

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, written_duration=None):
        import abjad
        original_input = written_duration
        if isinstance(written_duration, str):
            string = f'{{ {written_duration} }}'
            parsed = abjad.parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            written_duration = parsed[0]
        if isinstance(written_duration, Leaf):
            written_duration = written_duration.written_duration
        elif written_duration is None:
            written_duration = abjad.Duration(1, 4)
        else:
            written_duration = abjad.Duration(written_duration)
        Leaf.__init__(self, written_duration)
        if isinstance(original_input, Leaf):
            self._copy_override_and_set_from_leaf(original_input)

    ### PRIVATE METHODS ###

    def _get_body(self):
        return [self._get_compact_representation()]

    def _get_compact_representation(self):
        return f'r{self._get_formatted_duration()}'
