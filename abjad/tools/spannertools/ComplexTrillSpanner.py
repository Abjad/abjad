# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class ComplexTrillSpanner(Spanner):
    r'''A complex trill spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 ~ c'8 d'8 r8 e'8 ~ e'8 r8")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                c'4 ~
                c'8
                d'8
                r8
                e'8 ~
                e'8
                r8
            }

        ::

            >>> complex_trill = spannertools.ComplexTrillSpanner(
            ...     interval='P4',
            ...     )
            >>> attach(complex_trill, staff.select_leaves())
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                \pitchedTrill
                c'4 ~ \startTrillSpan f'
                c'8
                <> \stopTrillSpan
                \pitchedTrill
                d'8 \startTrillSpan g'
                <> \stopTrillSpan
                r8
                \pitchedTrill
                e'8 ~ \startTrillSpan a'
                e'8
                <> \stopTrillSpan
                r8
            }

    Allows for specifying a trill pitch via a named interval.

    Avoids silences.

    Restarts the trill on every new pitched logical tie.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_interval',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        interval=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        if interval is not None:
            interval = pitchtools.NamedInterval(interval)
        self._interval = interval

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._interval = self.interval

    def _format_before_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        prototype = (
            scoretools.Rest,
            scoretools.MultimeasureRest,
            scoretools.Skip,
            )
        if isinstance(leaf, prototype):
            return result
        leaf_ids = [id(x) for x in self._leaves]
        previous_leaf = leaf._get_leaf(-1)
        if id(previous_leaf) not in leaf_ids or \
            isinstance(previous_leaf, prototype) or \
            inspect_(leaf).get_logical_tie() != \
            inspect_(previous_leaf).get_logical_tie():
            if self.interval is not None:
                result.append(r'\pitchedTrill')
        return result

    def _format_right_of_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        prototype = (
            scoretools.Rest,
            scoretools.MultimeasureRest,
            scoretools.Skip,
            )
        if not isinstance(leaf, prototype):
            logical_tie = inspect_(leaf).get_logical_tie()
            if leaf is logical_tie.head:
                if self.interval is not None:
                    if hasattr(leaf, 'written_pitch'):
                        written_pitch = leaf.written_pitch
                    elif hasattr(leaf, 'written_pitches'):
                        written_pitch = leaf.written_pitches[0]
                    trill_pitch = written_pitch.transpose(self.interval)
                    string = r'\startTrillSpan {!s}'.format(trill_pitch)
                else:
                    string = r'\startTrillSpan'
                result.append(string)
        return result

    def _format_after_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        prototype = (
            scoretools.Rest,
            scoretools.MultimeasureRest,
            scoretools.Skip,
            )
        if not isinstance(leaf, prototype):
            logical_tie = inspect_(leaf).get_logical_tie()
            if leaf is logical_tie.tail:
                result.append(r'<> \stopTrillSpan')
        return result

    def _format_trill_start(self, leaf):
        result = []
        return result

    def _format_trill_stop(self):
        return [r'\stopTrillSpan']

    ### PUBLIC PROPERTIES ###

    @property
    def interval(self):
        r'''Gets optional interval of trill spanner.

        ..  container:: example

            ::
                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> interval = pitchtools.NamedInterval('m3')
                >>> complex_trill = spannertools.ComplexTrillSpanner(
                ...     interval=interval)
                >>> attach(complex_trill, staff[1:-1])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'4
                    \pitchedTrill
                    d'4 \startTrillSpan f'
                    <> \stopTrillSpan
                    \pitchedTrill
                    e'4 \startTrillSpan g'
                    <> \stopTrillSpan
                    f'4
                }

            ::

                >>> complex_trill.interval
                NamedInterval('+m3')

        '''
        return self._interval
