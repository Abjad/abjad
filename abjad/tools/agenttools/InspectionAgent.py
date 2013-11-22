# -*- encoding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools


class InspectionAgent(abctools.AbjadObject):
    r'''A wrapper around the Abjad inspection methods.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> inspect(staff)
            InspectionAgent({c'4, e'4, d'4, f'4})

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        from abjad.tools import scoretools
        assert isinstance(client, scoretools.Component)
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Client of inspection agent.

        Returns component.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def get_annotation(
        self,
        name,
        default=None,
        ):
        r'''Gets value of annotation with `name` attached to client.

        Returns `default` when no annotation with `name` is attached
        to client.

        Raises exception when more than one annotation with `name`
        is attached to client.
        '''
        from abjad.tools import indicatortools
        annotations = self.get_indicators(indicatortools.Annotation)
        if not annotations:
            return default
        with_correct_name = []
        for annotation in annotations:
            if annotation.name == name:
                with_correct_name.append(annotation)
        if not with_correct_name:
            return default
        if 1 < len(with_correct_name):
            message = 'multiple annotations with name {!r} attached.'
            message = message.format(name)
            raise Exception(message)
        annotation_value = with_correct_name[0].value
        return annotation_value

    def get_indicator(
        self,
        prototype=None,
        unwrap=True,
        ):
        r'''Gets exactly one indicator matching `prototype` attached to
        client.

        Raises exception when no indicator matching `prototype` is attached
        to client.

        Returns indicator.
        '''
        return self._client._get_indicator(
            prototype=prototype,
            unwrap=unwrap,
            )

    def get_indicators(
        self,
        prototype=None,
        unwrap=True,
        ):
        r'''Get all indicators matching `prototype` attached
        to client.

        Returns tuple.
        '''
        return self._client._get_indicators(
            prototype=prototype,
            unwrap=unwrap,
            )

    def get_badly_formed_components(self):
        r'''Gets badly formed components in client.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = Duration(1, 4)
                >>> beam = spannertools.Beam()
                >>> attach(beam, staff[:])

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> inspect(staff).get_badly_formed_components()
                [Note("d'4")]

            (Beamed quarter notes are not well formed.)

        Returns list.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager(self._client)
        violators = []
        for current_violators, total, check_name in manager():
            violators.extend(current_violators)
        return violators

    def get_components(
        self,
        prototype=None,
        include_self=True,
        ):
        r'''Gets all components of `prototype`
        in the descendants of client.

        Returns client selection.
        '''
        return self._client._get_components(
            prototype=prototype,
            include_self=include_self,
            )

    def get_contents(
        self,
        include_self=True,
        ):
        r'''Gets contents of client.

        Returns sequential selection.
        '''
        return self._client._get_contents(
            include_self=include_self,
            )

    def get_descendants(
        self,
        include_self=True,
        ):
        r'''Gets descendants of client.

        Returns descendants.
        '''
        return self._client._get_descendants(
            include_self=include_self,
            )

    def get_duration(
        self,
        in_seconds=False,
        ):
        r'''Gets duration of client.

        Returns duration.
        '''
        return self._client._get_duration(
            in_seconds=in_seconds,
            )

    def get_effective_indicator(
        self,
        prototype=None,
        ):
        r'''Gets effective indicator that matches `prototype`
        and governs client.

        Returns indicator or none.
        '''
        return self._client._get_effective_indicator(
            prototype=prototype,
            )

    def get_effective_staff(self):
        r'''Gets effective staff of client.

        Returns staff or none.
        '''
        return self._client._get_effective_staff()

    def get_grace_containers(
        self,
        kind=None,
        ):
        r'''Gets grace containers attached to leaf.

        ..  container:: example

            **Example 1.** Get all grace containers attached to note:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> grace_container = scoretools.GraceContainer(
                ...     [Note("cs'16")],
                ...     kind='grace',
                ...     )
                >>> attach(grace_container, staff[1])
                >>> after_grace = scoretools.GraceContainer(
                ...     [Note("ds'16")],
                ...     kind='after'
                ...     )
                >>> attach(after_grace, staff[1])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8
                    \grace {
                        cs'16
                    }
                    \afterGrace
                    d'8
                    {
                        ds'16
                    }
                    e'8
                    f'8
                }

            ::

                >>> inspect(staff[1]).get_grace_containers()
                (GraceContainer(cs'16), GraceContainer(ds'16))

        ..  container:: example

            **Example 2.** Get only (proper) grace containers attached to note:

            ::

                >>> inspect(staff[1]).get_grace_containers(kind='grace')
                (GraceContainer(cs'16),)

        ..  container:: example

            **Example 3.** Get only after grace containers attached to note:

            ::

                >>> inspect(staff[1]).get_grace_containers(kind='after')
                (GraceContainer(ds'16),)

        Set `kind` to ``'grace'``, ``'after'`` or none.

        Returns tuple.
        '''
        return self._client._get_grace_containers(
            kind=kind,
            )

    def get_leaf(self, n=0):
        r'''Gets leaf `n` **in logical voice**.

        ..  container:: example

            ::

                >>> staff = Staff()
                >>> staff.append(Voice("c'8 d'8 e'8 f'8"))
                >>> staff.append(Voice("g'8 a'8 b'8 c''8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    \new Voice {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                }

            ::

                >>> for n in range(8):
                ...     print n, inspect(staff[0][0]).get_leaf(n)
                ...
                0 c'8
                1 d'8
                2 e'8
                3 f'8
                4 None
                5 None
                6 None
                7 None

        Returns leaf or none.
        '''
        from abjad.tools import scoretools
        if not isinstance(self._client, scoretools.Leaf):
            return None
        return self._client._get_leaf(n=n)

    def get_lineage(self):
        r'''Gets lineage of client.

        Returns lineage.
        '''
        return self._client._get_lineage()

    def get_markup(
        self,
        direction=None,
        ):
        r'''Gets all markup attached to client.

        Returns tuple.
        '''
        return self._client._get_markup(
            direction=direction,
            )

    def get_parentage(
        self,
        include_self=True,
        ):
        r'''Gets parentage of client.

        Returns parentage.
        '''
        return self._client._get_parentage(
            include_self=include_self,
            )

    def get_spanner(
        self,
        prototype=None,
        ):
        r'''Gets exactly one spanner of `prototype` attached to
        client.

        Raises exception when no spanner of `prototype` is attached
        to client.

        Returns spanner.
        '''
        return self._client._get_spanner(
            prototype=prototype,
            )

    def get_spanners(
        self,
        prototype=None,
        ):
        r'''Gets spanners attached to client.

        Returns set.
        '''
        return self._client._get_spanners(
            prototype=prototype,
            )

    def get_tie_chain(self):
        r'''Gets tie chain that governs leaf.

        Returns tie chain.
        '''
        return self._client._get_tie_chain()

    def get_timespan(self,
        in_seconds=False,
        ):
        r'''Gets timespan of client.

        Returns timespan.
        '''
        return self._client._get_timespan(
            in_seconds=in_seconds,
            )

    def get_vertical_moment(
        self,
        governor=None,
        ):
        r'''Gets vertical moment starting with client.

        Returns vertical moment.
        '''
        return self._client._get_vertical_moment(
            governor=governor,
            )

    def get_vertical_moment_at(
        self,
        offset,
        ):
        r'''Gets vertical moment at `offset`.

        Returns vertical moment.
        '''
        return self._client._get_vertical_moment_at(
            offset,
            )

    def is_bar_line_crossing(self):
        r'''True when client crosses bar line.
        Otherwise false.

        ..  container:: example

            **Example.**

            ::

                >>> staff = Staff("c'4 d'4 e'4")
                >>> time_signature = TimeSignature((3, 8))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            ::

                >>> for note in staff:
                ...     result = inspect(note).is_bar_line_crossing()
                ...     print note, result
                ...
                c'4 False
                d'4 True
                e'4 False

        Returns boolean.
        '''
        from abjad.tools import indicatortools
        time_signature = self._client._get_effective_indicator(
            indicatortools.TimeSignature)
        if time_signature is None:
            time_signature_duration = durationtools.Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, 'partial', 0)
        partial = partial or 0
        start_offset = self._client._get_timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self._client._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def is_well_formed(
        self,
        allow_empty_containers=True,
        ):
        r'''True when client is well-formed.
        Otherwise false.

        Returns false.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager(
            self._client,
            allow_empty_containers=allow_empty_containers,
            )
        for violators, total, check_name in manager():
            if violators:
                return False
        return True

    def report_modifications(self):
        r'''Reports modifications of client.

        ..  container:: example

            **Example.** Report modifications of container in selection:

            ::

                >>> container = Container("c'8 d'8 e'8 f'8")
                >>> override(container).note_head.color = 'red'
                >>> override(container).note_head.style = 'harmonic'
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print format(container)
                {
                    \override NoteHead #'color = #red
                    \override NoteHead #'style = #'harmonic
                    c'8
                    d'8
                    e'8
                    f'8
                    \revert NoteHead #'color
                    \revert NoteHead #'style
                }

            ::

                >>> report = inspect(container).report_modifications()

            ::

                >>> print report
                {
                    \override NoteHead #'color = #red
                    \override NoteHead #'style = #'harmonic
                    %%% 4 components omitted %%%
                    \revert NoteHead #'color
                    \revert NoteHead #'style
                }

        Returns string.
        '''
        from abjad.tools import scoretools
        from abjad.tools import systemtools
        client = self._client
        bundle = systemtools.LilyPondFormatManager.bundle_format_contributions(
            client)
        result = []
        result.extend(client._get_format_contributions_for_slot(
            'before', bundle))
        result.extend(client._get_format_contributions_for_slot(
            'open brackets', bundle))
        result.extend(client._get_format_contributions_for_slot(
            'opening', bundle))
        result.append('\t%%%%%% %s components omitted %%%%%%' % len(client))
        result.extend(client._get_format_contributions_for_slot(
            'closing', bundle))
        result.extend(client._get_format_contributions_for_slot(
            'close brackets', bundle))
        result.extend(client._get_format_contributions_for_slot(
            'after', bundle))
        result = '\n'.join(result)
        return result

    def tabulate_well_formedness_violations(self):
        r'''Tabulates well-formedness violations in client.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = Duration(1, 4)
                >>> beam = spannertools.Beam()
                >>> attach(beam, staff[:])

            ..  doctest::

                >>> print format(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> result = inspect(staff).tabulate_well_formedness_violations()

            ::

                >>> print result
                1 / 4 beamed quarter notes
                0 / 1 discontiguous spanners
                0 / 5 duplicate ids
                0 / 0 intermarked hairpins
                0 / 0 misdurated measures
                0 / 0 misfilled measures
                0 / 4 mispitched ties
                0 / 4 misrepresented flags
                0 / 5 missing parents
                0 / 0 nested measures
                0 / 1 overlapping beams
                0 / 0 overlapping glissandi
                0 / 0 overlapping octavation spanners
                0 / 0 short hairpins

            Beamed quarter notes are not well formed.

        Returns string.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager(self._client)
        triples = manager()
        strings = []
        for violators, total, check_name in triples:
            violator_count = len(violators)
            string = '{} /\t{} {}'
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = string.format(violator_count, total, check_name)
            strings.append(string)
        return '\n'.join(strings)

def inspect(client):
    r'''Inspect `client`.

    Returns inspector.
    '''
    return InspectionAgent(client)
