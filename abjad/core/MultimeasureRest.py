from .Leaf import Leaf


class MultimeasureRest(Leaf):
    """
    Multimeasure rest.

    ..  container:: example

        >>> rest = abjad.MultimeasureRest((1, 4))
        >>> abjad.show(rest) # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *arguments):
        import abjad
        if len(arguments) == 0:
            arguments = ((1, 4),)
        rest = abjad.Rest(*arguments)
        Leaf.__init__(self, rest.written_duration)

    ### PRIVATE METHODS ###

    def _get_body(self):
        """
        Gets list of string representation of body of rest.
        Picked up as format contribution at format-time.
        """
        result = 'R' + str(self._get_formatted_duration())
        return [result]

    def _get_compact_representation(self):
        return f'R{self._get_formatted_duration()}'
