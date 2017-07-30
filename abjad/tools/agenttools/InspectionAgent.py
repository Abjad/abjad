# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools


class InspectionAgent(abctools.AbjadObject):
    r'''Inspection agent.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> abjad.inspect(staff)
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
        if not isinstance(client, prototype):
            message = 'must be component, spanner or none: {!r}.'
            message = message.format(client)
            raise TypeError(message)
        self._client = client

    ### PUBLIC METHODS ###

    def get_after_grace_container(self):
        r'''Gets after grace containers attached to leaf.

        ..  container:: example

            Get after grace container attached to note:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> note = abjad.Note("ds'16")
                >>> container = abjad.AfterGraceContainer([note])
                >>> abjad.attach(container, staff[1])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8
                    \afterGrace
                    d'8
                    {
                        ds'16
                    }
                    e'8
                    f'8
                }

            ::

                >>> abjad.inspect(staff[1]).get_after_grace_container()
                AfterGraceContainer("ds'16")

        Returns after grace container or none.
        '''
        return self._client._after_grace_container

    def get_annotation(self, name, default=None):
        r'''Gets annotation attached to client.

        ..  container:: example

            Gets named indicator:

            ::

                >>> note = abjad.Note("c'4")
                >>> abjad.annotate(note, 'bow_direction', Down)

            ::

                >>> abjad.inspect(note).get_annotation('bow_direction')
                Down

            Returns none when no annotation is found:

            ::

                >>> abjad.inspect(note).get_annotation('bow_fraction') is None
                True

            Returns default when no annotation is found:

            ::

                >>> abjad.inspect(note).get_annotation('bow_fraction', 2)
                2

        Returns annotation or default.
        '''
        for wrapper in self.get_indicators(unwrap=False):
            if wrapper.name == name:
                return wrapper.indicator
        return default

    def get_badly_formed_components(self):
        r'''Gets badly formed components in client.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = (1, 4)
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> abjad.inspect(staff).get_badly_formed_components()
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

    def get_components(self, prototype=None, include_self=True):
        r'''Gets all components of `prototype` in the descendants of client.

        Returns client selection.
        '''
        return self._client._get_components(
            prototype=prototype,
            include_self=include_self,
            )

    def get_contents(self, include_self=True):
        r'''Gets contents of client.

        Returns sequential selection.
        '''
        return self._client._get_contents(
            include_self=include_self,
            )

    def get_descendants(self, include_self=True):
        r'''Gets descendants of client.

        Returns descendants.
        '''
        return self._client._get_descendants(
            include_self=include_self,
            )

    def get_duration(self, in_seconds=False):
        r'''Gets duration of client.

        Returns duration.
        '''
        return self._client._get_duration(
            in_seconds=in_seconds,
            )

    def get_effective(self, prototype=None, unwrap=True, n=0):
        r'''Gets effective indicator that matches `prototype`
        and governs client.

        ..  container:: example

            Gets components' effective clef:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> clef = abjad.Clef('alto')
                >>> abjad.attach(clef, staff[0])
                >>> note = abjad.Note("fs'16")
                >>> container = abjad.AcciaccaturaContainer([note])
                >>> abjad.attach(container, staff[-1])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

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

                >>> for leaf in abjad.iterate(staff).by_class(
                ...     with_grace_notes=True,
                ...     ):
                ...     agent = abjad.inspect(leaf)
                ...     clef = agent.get_effective(abjad.Clef)
                ...     print(leaf, clef)
                ...
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

    def get_grace_container(self):
        r'''Gets grace container attached to leaf.

        ..  container:: example

            Get acciaccatura container attached to note:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> note = abjad.Note("cs'16")
                >>> container = abjad.AcciaccaturaContainer([note])
                >>> abjad.attach(container, staff[1])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8
                    \acciaccatura {
                        cs'16
                    }
                    d'8
                    e'8
                    f'8
                }

            ::

                >>> abjad.inspect(staff[1]).get_grace_container()
                AcciaccaturaContainer("cs'16")

        Returns grace container, acciaccatura container, appoggiatura container
        or none.
        '''
        return self._client._grace_container

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
        r'''Get all indicators matching `prototype` attached to client.

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

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
                >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
                >>> show(staff) # doctest: +SKIP

            ..  docs::

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

            Gets leaf `n` **from** client of inspection agent when client of
            inspection agent is a leaf.

            With positive indices:

            ::

                >>> first_leaf = staff[0][0]
                >>> first_leaf
                Note("c'8")

            ::

                >>> for n in range(8):
                ...     leaf = abjad.inspect(first_leaf).get_leaf(n)
                ...     print(n, leaf)
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
                ...     leaf = abjad.inspect(last_leaf).get_leaf(n)
                ...     print(n, leaf)
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

            Gets leaf `n` **in** client of inspection agent when client of
            inspection agent is a container.

            With positive indices:

            ::

                >>> first_voice = staff[0]
                >>> first_voice
                Voice("c'8 d'8 e'8 f'8")

            ::

                >>> for n in range(8):
                ...     leaf = abjad.inspect(first_voice).get_leaf(n)
                ...     print(n, leaf)
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
                ...     leaf = abjad.inspect(first_voice).get_leaf(n)
                ...     print(n, leaf)
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
        import abjad
        if isinstance(self._client, abjad.Leaf):
            return self._client._get_leaf(n=n)
        if 0 <= n:
            leaves = abjad.iterate(self._client).by_leaf(start=0, stop=n+1)
            leaves = list(leaves)
            if len(leaves) < n + 1:
                return
            leaf = leaves[n]
            return leaf
        else:
            leaves = abjad.iterate(self._client).by_leaf(
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

    def get_markup(self, direction=None):
        r'''Gets all markup attached to client.

        Returns tuple.
        '''
        return self._client._get_markup(
            direction=direction,
            )

    def get_parentage(self, include_self=True, with_grace_notes=False):
        r'''Gets parentage of client.

        .. container:: example

            Gets parentage without grace notes:

            ::

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.GraceContainer("c'16 d'16")
                >>> abjad.attach(container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  docs::

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

                >>> abjad.inspect(container[0]).get_parentage()
                Parentage([Note("c'16"), GraceContainer("c'16 d'16")])

        .. container:: example

            Gets parentage with grace notes:

            ::

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.GraceContainer("c'16 d'16")
                >>> abjad.attach(container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  docs::

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

                >>> agent = abjad.inspect(container[0])
                >>> agent.get_parentage(with_grace_notes=True)
                Parentage([Note("c'16"), GraceContainer("c'16 d'16"), Note("d'4"), Voice("c'4 d'4 e'4 f'4")])

        Returns parentage.
        '''
        return self._client._get_parentage(
            include_self=include_self,
            with_grace_notes=with_grace_notes,
            )

    def get_piecewise(self, prototype=None, default=None):
        r'''Gets piecewise indicators attached to client.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
                >>> spanner = abjad.TextSpanner()
                >>> abjad.attach(spanner, staff[:])
                >>> spanner.attach(abjad.Markup('pont.'), staff[0])
                >>> spanner.attach(abjad.Markup('ord.'), staff[-1])
                >>> spanner.attach(abjad.ArrowLineSegment(), staff[0])

            ::

                >>> abjad.override(staff).text_script.staff_padding = 1.25
                >>> abjad.override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
                    \once \override TextSpanner.bound-details.left-broken.text = ##f
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                    \once \override TextSpanner.bound-details.left.text = \markup {
                        \concat
                            {
                                pont.
                                \hspace
                                    #0.25
                            }
                        }
                    \once \override TextSpanner.bound-details.right-broken.padding = 0
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup { ord. }
                }

            ::

                >>> for leaf in staff:
                ...     leaf, abjad.inspect(leaf).get_piecewise(abjad.Markup)
                ...
                (Note("c'4"), Markup(contents=['pont.']))
                (Note("d'4"), None)
                (Note("e'4"), None)
                (Note("f'4"), Markup(contents=['ord.']))

        Returns indicator or default.
        '''
        wrappers = self.get_indicators(prototype=prototype, unwrap=False)
        wrappers = wrappers or []
        wrappers = [_ for _ in wrappers if _.is_piecewise]
        if not wrappers:
            return default
        if len(wrappers) == 1:
            return wrappers[0].indicator
        if 1 < len(wrappers):
            message = 'multiple indicators attached to client.'
            raise Exception(message)

    def get_sounding_pitch(self):
        r'''Gets sounding pitch of client.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("d''8 e''8 f''8 g''8")
                >>> piccolo = abjad.instrumenttools.Piccolo()
                >>> abjad.attach(piccolo, staff[0])
                >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Piccolo }
                    \set Staff.shortInstrumentName = \markup { Picc. }
                    d'8
                    e'8
                    f'8
                    g'8
                }
                >>> abjad.inspect(staff[0]).get_sounding_pitch()
                NamedPitch("d''")

        Returns named pitch.
        '''
        return self._client._get_sounding_pitch()

    def get_sounding_pitches(self):
        r"""Gets sounding pitches of client.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
                >>> glockenspiel = abjad.instrumenttools.Glockenspiel()
                >>> abjad.attach(glockenspiel, staff[0])
                >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Glockenspiel }
                    \set Staff.shortInstrumentName = \markup { Gkspl. }
                    <c' e'>4
                    <d' fs'>4
                }

            ::

                >>> abjad.inspect(staff[0]).get_sounding_pitches()
                (NamedPitch("c'''"), NamedPitch("e'''"))

        Returns tuple.
        """
        return self._client._get_sounding_pitches()

    def get_spanner(self, prototype=None, default=None, in_parentage=False):
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

    def get_spanners(self, prototype=None, in_parentage=False):
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

            Gets timespan of grace notes:

            ::

                >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
                >>> grace_notes = [abjad.Note("c'16"), abjad.Note("d'16")]
                >>> container = abjad.GraceContainer(grace_notes)
                >>> abjad.attach(container, voice[1])
                >>> container = abjad.AfterGraceContainer("e'16 f'16")
                >>> abjad.attach(container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  docs::

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

                >>> for leaf in abjad.iterate(voice).by_leaf(
                ...     with_grace_notes=True,
                ...     ):
                ...     timespan = abjad.inspect(leaf).get_timespan()
                ...     print(str(leaf) + ':')
                ...     f(timespan)
                ...
                c'8:
                abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(1, 8),
                    )
                c'16:
                abjad.Timespan(
                    start_offset=abjad.Offset(
                        (1, 8),
                        grace_displacement=abjad.Duration(-1, 8),
                        ),
                    stop_offset=abjad.Offset(
                        (1, 8),
                        grace_displacement=abjad.Duration(-1, 16),
                        ),
                    )
                d'16:
                abjad.Timespan(
                    start_offset=abjad.Offset(
                        (1, 8),
                        grace_displacement=abjad.Duration(-1, 16),
                        ),
                    stop_offset=abjad.Offset(1, 8),
                    )
                d'8:
                abjad.Timespan(
                    start_offset=abjad.Offset(1, 8),
                    stop_offset=abjad.Offset(1, 4),
                    )
                e'16:
                abjad.Timespan(
                    start_offset=abjad.Offset(
                        (1, 4),
                        grace_displacement=abjad.Duration(-1, 8),
                        ),
                    stop_offset=abjad.Offset(
                        (1, 4),
                        grace_displacement=abjad.Duration(-1, 16),
                        ),
                    )
                f'16:
                abjad.Timespan(
                    start_offset=abjad.Offset(
                        (1, 4),
                        grace_displacement=abjad.Duration(-1, 16),
                        ),
                    stop_offset=abjad.Offset(1, 4),
                    )
                e'8:
                abjad.Timespan(
                    start_offset=abjad.Offset(1, 4),
                    stop_offset=abjad.Offset(3, 8),
                    )
                f'8:
                abjad.Timespan(
                    start_offset=abjad.Offset(3, 8),
                    stop_offset=abjad.Offset(1, 2),
                    )

        Returns timespan.
        '''
        return self._client._get_timespan(
            in_seconds=in_seconds,
            )

    def get_vertical_moment(self, governor=None):
        r'''Gets vertical moment starting with client.

        ..  container:: example

            ::

            >>> score = abjad.Score()
            >>> tuplet = abjad.Tuplet((4, 3), "d''8 c''8 b'8")
            >>> score.append(abjad.Staff([tuplet]))
            >>> staff_group = abjad.StaffGroup(context_name='PianoStaff')
            >>> staff_group.append(abjad.Staff("a'4 g'4"))
            >>> staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff_group[1][0])
            >>> score.append(staff_group)

        ..  docs::

            >>> f(score)
            \new Score <<
                \new Staff {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/3 {
                        d''8
                        c''8
                        b'8
                    }
                }
                \new PianoStaff <<
                    \new Staff {
                        a'4
                        g'4
                    }
                    \new Staff {
                        \clef "bass"
                        f'8
                        e'8
                        d'8
                        c'8
                    }
                >>
            >>

            >>> agent = abjad.inspect(staff_group[1][0])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("a'4"), Note("f'8")])

        ::

            >>> agent = abjad.inspect(staff_group[1][1])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("a'4"), Note("e'8")])

        ::

            >>> agent = abjad.inspect(staff_group[1][2])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("d'8")])

        ::

            >>> agent = abjad.inspect(staff_group[1][3])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("c'8")])

        Returns vertical moment.
        '''
        return self._client._get_vertical_moment(
            governor=governor,
            )

    def get_vertical_moment_at(self, offset):
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

    def has_spanner(self, prototype=None, in_parentage=False):
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

                >>> staff = abjad.Staff("c'4 d'4 e'4")
                >>> time_signature = abjad.TimeSignature((3, 8))
                >>> abjad.attach(time_signature, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            ::

                >>> for note in staff:
                ...     result = abjad.inspect(note).is_bar_line_crossing()
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

                >>> container = abjad.Container("c'8 d'8 e'8 f'8")
                >>> abjad.override(container).note_head.color = 'red'
                >>> abjad.override(container).note_head.style = 'harmonic'
                >>> show(container) # doctest: +SKIP

            ..  docs::

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

                >>> report = abjad.inspect(container).report_modifications()

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

    def tabulate_well_formedness_violations(
        self,
        allow_percussion_clef=None,
        ):
        r'''Tabulates well-formedness violations in client.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = (1, 4)
                >>> beam = abjad.Beam()
                >>> abjad.attach(beam, staff[:])

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> agent = abjad.inspect(staff)
                >>> result = agent.tabulate_well_formedness_violations()

            ::

                >>> print(result)
                1 /	4 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	1 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	1 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /	0 short hairpins
                0 /	0 tied rests

            Beamed quarter notes are not well formed.

        Returns string.
        '''
        from abjad.tools import systemtools
        manager = systemtools.WellformednessManager(
            allow_percussion_clef=allow_percussion_clef,
            )
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
