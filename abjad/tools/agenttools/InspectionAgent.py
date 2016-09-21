# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools.topleveltools.iterate import iterate


class InspectionAgent(abctools.AbjadObject):
    r'''Inspection agent.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> inspect_(staff)
            InspectionAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        prototype = (scoretools.Component, spannertools.Spanner, type(None))
        assert isinstance(client, prototype), repr(client)
        self._client = client

    ### PUBLIC METHODS ###

    def get_annotation(self, name, default=None):
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

    def get_badly_formed_components(self):
        r'''Gets badly formed components in client.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = Duration(1, 4)
                >>> beam = spannertools.Beam()
                >>> attach(beam, staff[:])

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> inspect_(staff).get_badly_formed_components()
                [Note("d'4")]

            (Beamed quarter notes are not well formed.)

        Returns list.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager()
        violators = []
        for current_violators, total, check_name in manager(self._client):
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

    def get_effective(
        self,
        prototype=None,
        unwrap=True,
        n=0,
        ):
        r'''Gets effective indicator that matches `prototype`
        and governs client.

        ..  container:: example

            **Example.** Gets components' effective clef:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> attach(Clef('alto'), staff)
                >>> grace_container = scoretools.GraceContainer(
                ...    [Note("fs'16")],
                ...     kind='acciaccatura',
                ...     )
                >>> attach(grace_container, staff[-1])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \clef "alto"
                    c'4
                    d'4
                    e'4
                    \acciaccatura {
                        fs'16
                    }
                    f'4
                }

            ::

                >>> for leaf in iterate(staff).by_class(with_grace_notes=True):
                ...     clef = inspect_(leaf).get_effective(Clef)
                ...     print(leaf, clef)
                Staff("c'4 d'4 e'4 f'4") Clef(name='alto')
                c'4 Clef(name='alto')
                d'4 Clef(name='alto')
                e'4 Clef(name='alto')
                fs'16 Clef(name='alto')
                f'4 Clef(name='alto')

        Returns indicator or none.
        '''
        return self._client._get_effective(
            prototype=prototype,
            unwrap=unwrap,
            n=n,
            )

    def get_effective_staff(self):
        r'''Gets effective staff of client.

        Returns staff or none.
        '''
        return self._client._get_effective_staff()

    def get_grace_container(
        self,
        kind=None,
        ):
        r'''Gets exactly one grace container of `kind` attached to client.

        Raises error when no grace container of `kind` attaches to client.

        Raises error when more than one grace container of `kind` attaches
        to client.

        Returns grace container.
        '''
        grace_containers = self.get_grace_containers(kind=kind)
        if not grace_containers:
            message = 'no grace containers of {!r} attached.'
            message = message.format(kind)
            raise Exception(message)
        if 1 < len(grace_containers):
            message = 'more than one grace container of {!r} attached.'
            message = message.format(kind)
            raise Exception(message)
        grace_container = grace_containers[0]
        return grace_container

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

                >>> f(staff)
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

                >>> inspect_(staff[1]).get_grace_containers()
                (GraceContainer("cs'16"), GraceContainer("ds'16"))

        ..  container:: example

            **Example 2.** Get only (proper) grace containers attached to note:

            ::

                >>> inspect_(staff[1]).get_grace_containers(kind='grace')
                (GraceContainer("cs'16"),)

        ..  container:: example

            **Example 3.** Get only after grace containers attached to note:

            ::

                >>> inspect_(staff[1]).get_grace_containers(kind='after')
                (GraceContainer("ds'16"),)

        Set `kind` to ``'grace'``, ``'after'`` or none.

        Returns tuple.
        '''
        return self._client._get_grace_containers(
            kind=kind,
            )

    def get_indicator(
        self,
        prototype=None,
        default=None,
        unwrap=True,
        ):
        r'''Gets indicator of `prototype` attached to client.

        Raises exception when more than one indicator of `prototype` attach to
        client.

        Returns default when no indicator of `prototype` attaches to client.

        Returns indicator or default.
        '''
        indicators = self._client._get_indicators(
                prototype=prototype,
                unwrap=unwrap,
                )
        if not indicators:
            return default
        elif len(indicators) == 1:
            return list(indicators)[0]
        else:
            message = 'multiple indicators attached to client.'
            raise Exception(message)

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

    def get_leaf(self, n=0):
        r'''Gets leaf `n`.

        ..  container:: example

            Example score:

            ::

                >>> staff = Staff()
                >>> staff.append(Voice("c'8 d'8 e'8 f'8"))
                >>> staff.append(Voice("g'8 a'8 b'8 c''8"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
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

        ..  container:: example

            **Example 1.** Gets leaf `n` **from** client of inspection agent
            when client of inspection agent is a leaf.

            With positive indices:

            ::

                >>> first_leaf = staff[0][0]
                >>> first_leaf
                Note("c'8")

            ::

                >>> for n in range(8):
                ...     print(n, inspect_(first_leaf).get_leaf(n))
                ...
                0 c'8
                1 d'8
                2 e'8
                3 f'8
                4 None
                5 None
                6 None
                7 None

            With negative indices:

            ::

                >>> last_leaf = staff[0][-1]
                >>> last_leaf
                Note("f'8")

            ::

                >>> for n in range(0, -8, -1):
                ...     print(n, inspect_(last_leaf).get_leaf(n))
                ...
                0 f'8
                -1 e'8
                -2 d'8
                -3 c'8
                -4 None
                -5 None
                -6 None
                -7 None

        ..  container:: example

            **Example 2.** Gets leaf `n` **in** client of inspection agent
            when client of inspection agent is a container.

            With positive indices:

            ::

                >>> first_voice = staff[0]
                >>> first_voice
                Voice("c'8 d'8 e'8 f'8")

            ::

                >>> for n in range(8):
                ...     print(n, inspect_(first_voice).get_leaf(n))
                ...
                0 c'8
                1 d'8
                2 e'8
                3 f'8
                4 None
                5 None
                6 None
                7 None

            With negative indices:

            ::

                >>> first_voice = staff[0]
                >>> first_voice
                Voice("c'8 d'8 e'8 f'8")

            ::

                >>> for n in range(-1, -9, -1):
                ...     print(n, inspect_(first_voice).get_leaf(n))
                ...
                -1 f'8
                -2 e'8
                -3 d'8
                -4 c'8
                -5 None
                -6 None
                -7 None
                -8 None

        Returns leaf or none.
        '''
        from abjad.tools import scoretools
        if isinstance(self._client, scoretools.Leaf):
            return self._client._get_leaf(n=n)
        if 0 <= n:
            leaves = iterate(self._client).by_class(
                scoretools.Leaf,
                start=0,
                stop=n+1,
                )
            leaves = list(leaves)
            if len(leaves) < n + 1:
                return
            leaf = leaves[n]
            return leaf
        else:
            leaves = iterate(self._client).by_class(
                scoretools.Leaf,
                start=0,
                stop=abs(n),
                reverse=True,
                )
            leaves = list(leaves)
            if len(leaves) < abs(n):
                return
            leaf = leaves[abs(n)-1]
            return leaf

    def get_lineage(self):
        r'''Gets lineage of client.

        Returns lineage.
        '''
        return self._client._get_lineage()

    def get_logical_tie(self):
        r'''Gets logical tie that governs leaf.

        Returns logical tie.
        '''
        return self._client._get_logical_tie()

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
        with_grace_notes=False,
        ):
        r'''Gets parentage of client.

        .. container:: example

            **Example 1.** Gets parentage without grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> grace_notes = [Note("c'16"), Note("d'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4
                    \grace {
                        c'16
                        d'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> inspect_(grace_notes[0]).get_parentage()
                Parentage([Note("c'16"), GraceContainer("c'16 d'16")])

        .. container:: example

            **Example 2.** Gets parentage with grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> grace_notes = [Note("c'16"), Note("d'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4
                    \grace {
                        c'16
                        d'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> inspector = inspect_(grace_notes[0])
                >>> inspector.get_parentage(with_grace_notes=True)
                Parentage([Note("c'16"), GraceContainer("c'16 d'16"), Note("d'4"), Voice("c'4 d'4 e'4 f'4")])

        Returns parentage.
        '''
        return self._client._get_parentage(
            include_self=include_self,
            with_grace_notes=with_grace_notes,
            )

    def get_sounding_pitch(self):
        r'''Gets sounding pitch of client.

        ..  container:: example

            ::

                >>> staff = Staff("d''8 e''8 f''8 g''8")
                >>> piccolo = instrumenttools.Piccolo()
                >>> attach(piccolo, staff)
                >>> instrumenttools.transpose_from_sounding_pitch_to_written_pitch(
                ...     staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Piccolo }
                    \set Staff.shortInstrumentName = \markup { Picc. }
                    d'8
                    e'8
                    f'8
                    g'8
                }
                >>> inspect_(staff[0]).get_sounding_pitch()
                NamedPitch("d''")

        Returns named pitch.
        '''
        return self._client._get_sounding_pitch()

    def get_sounding_pitches(self):
        r"""Gets sounding pitches of client.

        ..  container:: example

            ::

                >>> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
                >>> glockenspiel = instrumenttools.Glockenspiel()
                >>> attach(glockenspiel, staff)
                >>> instrumenttools.transpose_from_sounding_pitch_to_written_pitch(
                ...     staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Glockenspiel }
                    \set Staff.shortInstrumentName = \markup { Gkspl. }
                    <c' e'>4
                    <d' fs'>4
                }

            ::

                >>> inspect_(staff[0]).get_sounding_pitches()
                (NamedPitch("c'''"), NamedPitch("e'''"))

        Returns tuple.
        """
        return self._client._get_sounding_pitches()

    def get_spanner(
        self,
        prototype=None,
        default=None,
        in_parentage=False,
        ):
        r'''Gets spanner of `prototype` attached to client.

        Raises exception when more than one spanner of `prototype` attaches to
        client.

        Returns `default` when no spanner of `prototype` attaches to client.

        Returns spanner or default.
        '''
        spanners = self._client._get_spanners(
            prototype=prototype,
            in_parentage=in_parentage,
            )
        if not spanners:
            return default
        elif len(spanners) == 1:
            return list(spanners)[0]
        else:
            message = 'multiple spanners attached to client.'
            raise Exception(message)

    def get_spanners(
        self,
        prototype=None,
        in_parentage=False,
        ):
        r'''Gets spanners attached to client.

        Returns set.
        '''
        return self._client._get_spanners(
            prototype=prototype,
            in_parentage=in_parentage,
            )

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of client.

        ..  container:: example

            **Example.** Gets timespan of grace notes:

            ::

                >>> voice = Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [Note("c'16"), Note("d'16")]
                >>> grace = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace, voice[1])
                >>> after_grace_notes = [Note("e'16"), Note("f'16")]
                >>> after_grace = scoretools.GraceContainer(
                ...     after_grace_notes,
                ...     kind='after')
                >>> attach(after_grace, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'8 [
                    \grace {
                        c'16
                        d'16
                    }
                    \afterGrace
                    d'8
                    {
                        e'16
                        f'16
                    }
                    e'8
                    f'8 ]
                }

            ::

                >>> for leaf in iterate(voice).by_leaf(with_grace_notes=True):
                ...     timespan = inspect_(leaf).get_timespan()
                ...     print(str(leaf) + ':')
                ...     print(format(timespan, 'storage'))
                c'8:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(1, 8),
                    )
                c'16:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(
                        (1, 8),
                        grace_displacement=durationtools.Duration(-1, 8),
                        ),
                    stop_offset=durationtools.Offset(
                        (1, 8),
                        grace_displacement=durationtools.Duration(-1, 16),
                        ),
                    )
                d'16:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(
                        (1, 8),
                        grace_displacement=durationtools.Duration(-1, 16),
                        ),
                    stop_offset=durationtools.Offset(1, 8),
                    )
                d'8:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(1, 8),
                    stop_offset=durationtools.Offset(1, 4),
                    )
                e'16:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(
                        (1, 4),
                        grace_displacement=durationtools.Duration(-1, 8),
                        ),
                    stop_offset=durationtools.Offset(
                        (1, 4),
                        grace_displacement=durationtools.Duration(-1, 16),
                        ),
                    )
                f'16:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(
                        (1, 4),
                        grace_displacement=durationtools.Duration(-1, 16),
                        ),
                    stop_offset=durationtools.Offset(1, 4),
                    )
                e'8:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(1, 4),
                    stop_offset=durationtools.Offset(3, 8),
                    )
                f'8:
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 8),
                    stop_offset=durationtools.Offset(1, 2),
                    )

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

    def has_effective_indicator(self, prototype=None):
        r'''Is true when indicator that matches `prototype` is
        in effect for client. Otherwise false.

        Returns true or false.
        '''
        return self._client._has_effective_indicator(prototype=prototype)

    def has_indicator(self, prototype=None):
        r'''Is true when client has one or more
        indicators that match `prototype`. Otherwise false.

        Returns true or false.
        '''
        return self._client._has_indicator(prototype=prototype)

    def has_spanner(
        self,
        prototype=None,
        in_parentage=False,
        ):
        r'''Is true when client has one or more
        spanners that match `prototype`. Otherwise false.

        Returns true or false.
        '''
        return self._client._has_spanner(
            prototype=prototype,
            in_parentage=in_parentage,
            )

    def is_bar_line_crossing(self):
        r'''Is true when client crosses bar line.
        Otherwise false.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 d'4 e'4")
                >>> time_signature = TimeSignature((3, 8))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            ::

                >>> for note in staff:
                ...     result = inspect_(note).is_bar_line_crossing()
                ...     print(note, result)
                ...
                c'4 False
                d'4 True
                e'4 False

        Returns true or false.
        '''
        from abjad.tools import indicatortools
        time_signature = self._client._get_effective(
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

    def is_well_formed(self):
        r'''Is true when client is well-formed.
        Otherwise false.

        Returns false.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager()
        for violators, total, check_name in manager(self._client):
            if violators:
                return False
        return True

    def report_modifications(self):
        r'''Reports modifications of client.

        ..  container:: example

            Report modifications of container in selection:

            ::

                >>> container = Container("c'8 d'8 e'8 f'8")
                >>> override(container).note_head.color = 'red'
                >>> override(container).note_head.style = 'harmonic'
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    \override NoteHead.color = #red
                    \override NoteHead.style = #'harmonic
                    c'8
                    d'8
                    e'8
                    f'8
                    \revert NoteHead.color
                    \revert NoteHead.style
                }

            ::

                >>> report = inspect_(container).report_modifications()

            ::

                >>> print(report)
                {
                    \override NoteHead.color = #red
                    \override NoteHead.style = #'harmonic
                    %%% 4 components omitted %%%
                    \revert NoteHead.color
                    \revert NoteHead.style
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
        result.append('    %%%%%% %s components omitted %%%%%%' % len(client))
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

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> result = inspect_(staff).tabulate_well_formedness_violations()

            ::

                >>> print(result)
                1 / 4 beamed quarter notes
                0 / 1 conflicting clefs
                0 / 1 discontiguous spanners
                0 / 5 duplicate ids
                0 / 1 empty containers
                0 / 0 intermarked hairpins
                0 / 0 misdurated measures
                0 / 0 misfilled measures
                0 / 0 mismatched enchained hairpins
                0 / 0 mispitched ties
                0 / 4 misrepresented flags
                0 / 5 missing parents
                0 / 0 nested measures
                0 / 1 overlapping beams
                0 / 0 overlapping glissandi
                0 / 0 overlapping hairpins
                0 / 0 overlapping octavation spanners
                0 / 0 overlapping ties
                0 / 0 short hairpins
                0 / 0 tied rests

            Beamed quarter notes are not well formed.

        Returns string.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager()
        triples = manager(self._client)
        strings = []
        for violators, total, check_name in triples:
            violator_count = len(violators)
            string = '{} /\t{} {}'
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = string.format(violator_count, total, check_name)
            strings.append(string)
        return '\n'.join(strings)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Client of inspection agent.

        Returns component.
        '''
        return self._client
