from .Spanner import Spanner


class StaffLinesSpanner(Spanner):
    r'''Staff lines spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.StaffLinesSpanner(lines=1)
        >>> abjad.attach(spanner, staff[1:3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'8
                \stopStaff
                \once \override Staff.StaffSymbol.line-count = 1
                \startStaff
                d'8
                e'8
                \stopStaff
                \startStaff
                f'8
            }

    Stops and restarts staff on first leaf in spanner.

    Overrides ``line-count`` attribute of LilyPond ``Staff.StaffSymbol`` grob
    on first leaf in spanner.

    Stops and restarts staff on last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lines',
        '_forbid_restarting',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lines=5,
        forbid_restarting=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        if isinstance(lines, int) and 0 < lines:
            self._lines = lines
        elif (isinstance(lines, (tuple, list)) and
            all(isinstance(x, (int, float)) for x in lines)):
            self._lines = tuple(lines)
        else:
            message = 'must be integer or a sequence of integers: {!r}.'
            message = message.format(lines)
            raise ValueError(message)
        self._lines = lines
        if forbid_restarting is not None:
            forbid_restarting = bool(forbid_restarting)
        self._forbid_restarting = forbid_restarting

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._lines = self.lines

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_last_leaf(leaf) and not self.forbid_restarting:
            bundle.after.commands.append(r'\stopStaff')
            bundle.after.commands.append(r'\startStaff')
        if self._is_my_first_leaf(leaf):
            bundle.before.commands.append(r'\stopStaff')
            if isinstance(self.lines, int):
                override = abjad.LilyPondGrobOverride(
                    context_name='Staff',
                    grob_name='StaffSymbol',
                    once=True,
                    property_path='line-count',
                    value=self.lines,
                    )
                string = override.override_string
                bundle.before.commands.append(string)
            else:
                override = abjad.LilyPondGrobOverride(
                    context_name='Staff',
                    grob_name='StaffSymbol',
                    once=True,
                    property_path='line-positions',
                    value=abjad.SchemeVector(self.lines),
                    )
                string = override.override_string
                bundle.before.commands.append(string)
            bundle.before.commands.append(r'\startStaff')
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def forbid_restarting(self):
        r'''Is true if staff lines spanner is forbidden from re-stopping and
        re-starting the staff on its last leaf. Otherwise false.

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.StaffLinesSpanner(
        ...     lines=1,
        ...     forbid_restarting=True,
        ...     )
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \stopStaff
                \once \override Staff.StaffSymbol.line-count = 1
                \startStaff
                c'8
                d'8
                e'8
                f'8
            }

        This is useful when the final leaf of a score is covered by a staff
        lines spanner, to prevent unexpected LilyPond typesetting behavior.

        Returns true or false.
        '''
        return self._forbid_restarting

    @property
    def lines(self):
        r'''Gets line of staff lines spanner.

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.StaffLinesSpanner(lines=1)
        >>> abjad.attach(spanner, staff[1:3])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> spanner.lines
        1

        Returns nonnegative integer.
        '''
        return self._lines
