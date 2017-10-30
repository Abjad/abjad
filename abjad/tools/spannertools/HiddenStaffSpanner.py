from .Spanner import Spanner


class HiddenStaffSpanner(Spanner):
    r'''Hidden staff spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.HiddenStaffSpanner()
        >>> abjad.attach(spanner, staff[1:3])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'8
                \stopStaff
                d'8
                e'8
                \startStaff
                f'8
            }

    Formats LilyPond ``\stopStaff`` before first leaf in spanner.

    Formats LilyPond ``\startStaff`` command after last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_first_leaf(leaf):
            bundle.before.commands.append(r'\stopStaff')
        if self._is_my_last_leaf(leaf):
            bundle.after.commands.append(r'\startStaff')
        return bundle
