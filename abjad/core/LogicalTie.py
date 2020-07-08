from ..selectx import Selection


class LogicalTie(Selection):
    """
    Logical tie of a component.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' ~ e'")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.select(staff[2]).logical_tie()
        LogicalTie([Note("e'4"), Note("e'4")])

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        Returns component or vanilla selection (not logical tie).
        """
        result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    ### PRIVATE METHODS ###

    def _scale(self, multiplier):
        for leaf in list(self):
            leaf._scale(multiplier)

    ### PUBLIC PROPERTIES ###

    @property
    def head(self):
        """
        Reference to element ``0`` in logical tie.

        Returns component.
        """
        if self.items:
            return self.items[0]

    @property
    def is_pitched(self):
        """
        Is true when logical tie head is a note or chord.

        Returns true or false.
        """
        return hasattr(self.head, "written_pitch") or hasattr(
            self.head, "written_pitches"
        )

    @property
    def is_trivial(self):
        """
        Is true when length of logical tie is less than or equal to ``1``.

        Returns true or false.
        """
        return len(self) <= 1

    @property
    def leaves(self):
        """
        Gets leaves in logical tie.

        Returns selection.
        """
        return Selection(self)

    @property
    def tail(self):
        """
        Gets last leaf in logical tie.

        Returns leaf.
        """
        if self.items:
            return self.items[-1]

    @property
    def written_duration(self):
        """
        Sum of written duration of all components in logical tie.

        Returns duration.
        """
        return sum([_.written_duration for _ in self])
