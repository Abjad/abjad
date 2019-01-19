import typing
from abjad import enums
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tags import Tags


class StopTrillSpan(object):
    r"""
    LilyPond ``\stopTrillSpan`` command.

    ..  container:: example

        >>> abjad.StopTrillSpan()
        StopTrillSpan() 

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_leak',
        '_right_broken',
        )

    _context = 'Voice'

    _parameter = 'TRILL'

    _persistent = True

    _publish_storage_format = True

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        leak: bool = None,
        right_broken: bool = None,
        ) -> None:
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = r'\stopTrillSpan'
        if self.right_broken:
            string = self._tag_hide([string])[0]
        if self.leak:
            string = f'<> {string}'
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    @staticmethod
    def _tag_hide(strings):
        abjad_tags = Tags()
        return LilyPondFormatManager.tag(
            strings,
            deactivate=False,
            tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StopTrillSpan().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop trill spanner leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTrillSpan()
            >>> abjad.tweak(command).color = 'blue'
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTrillSpan()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startTrillSpan
                    d'4
                    e'4
                    \stopTrillSpan
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTrillSpan()
            >>> abjad.tweak(command).color = 'blue'
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTrillSpan(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startTrillSpan
                    d'4
                    e'4
                    <> \stopTrillSpan
                    r4
                }

        """
        return self._leak

    @property
    def parameter(self) -> str:
        """
        Returns ``'TRILL'``.

        ..  container:: example

            >>> abjad.StopTrillSpan().parameter
            'TRILL'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopTrillSpan().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def right_broken(self) -> typing.Optional[bool]:
        r"""
        Is true when stop trill spanner is right-broken.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_trill_span = abjad.StartTrillSpan()
            >>> abjad.attach(start_trill_span, staff[0])
            >>> stop_trill_span = abjad.StopTrillSpan(right_broken=True)
            >>> abjad.attach(stop_trill_span, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \startTrillSpan
                d'4
                e'4
                \stopTrillSpan %! HIDE_TO_JOIN_BROKEN_SPANNERS
                r4
            }

        """
        return self._right_broken

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopTrillSpan().spanner_stop
            True

        """
        return True
