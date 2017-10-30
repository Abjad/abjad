import collections
from abjad.tools import abctools


class Inspection(abctools.AbjadObject):
    r'''Inspection.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collaborators'

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        import abjad
        assert not isinstance(client, str), repr(client)
        prototype = (abjad.Component, collections.Iterable, type(None))
        if not isinstance(client, prototype):
            message = 'must be component, nonstring iterable or none: {!r}.'
            message = message.format(client)
            raise TypeError(message)
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Gets client of inspection.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
            >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

            >>> abjad.inspect(staff).client
            <Staff{2}>

        Returns component.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def get_after_grace_container(self):
        r'''Gets after grace containers attached to leaf.

        ..  container:: example

            Get after grace container attached to note:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> note = abjad.Note("ds'16")
            >>> container = abjad.AfterGraceContainer([note])
            >>> abjad.attach(container, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

            >>> abjad.inspect(staff[1]).get_after_grace_container()
            AfterGraceContainer("ds'16")

        Returns after grace container or none.
        '''
        return getattr(self.client, '_after_grace_container', None)

    def get_annotation(self, name, default=None):
        r'''Gets annotation.

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> abjad.annotate(note, 'bow_direction', abjad.Down)
            >>> abjad.inspect(note).get_annotation('bow_direction')
            Down

            Returns none when no annotation is found:

            >>> abjad.inspect(note).get_annotation('bow_fraction') is None
            True

            Returns default when no annotation is found:

            >>> abjad.inspect(note).get_annotation('bow_fraction', 2)
            2

        Returns annotation or default.
        '''
        if hasattr(self.client, '_get_annotation'):
            annotation = self.client._get_annotation(name)
            if annotation is not None:
                return annotation
        return default

    def get_badly_formed_components(self):
        r'''Gets badly formed components.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = (1, 4)
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:])

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            >>> abjad.inspect(staff).get_badly_formed_components()
            [Note("d'4")]

            Beamed long notes are not well-formed.

        Returns list.
        '''
        import abjad
        manager, violators = abjad.WellformednessManager(), []
        for violators_, total, check_name in manager(self.client):
            violators.extend(violators_)
        return violators

    def get_contents(self, include_self=True):
        r'''Gets contents.

        ..  container:: example

            >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 e'8 } f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    f'4
                }

            >>> for component in abjad.inspect(staff).get_contents():
            ...     component
            ...
            <Staff{2}>
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff).get_contents(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("f'4")

        Returns selection.
        '''
        if hasattr(self.client, '_get_contents'):
            return self.client._get_contents(include_self=include_self)

    def get_descendants(self, include_self=True):
        r'''Gets descendants.

        ..  container:: example

            >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 e'8 } f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    f'4
                }

            >>> for component in abjad.inspect(staff).get_descendants():
            ...     component
            ...
            <Staff{2}>
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff).get_descendants(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'4")

            >>> for component in abjad.inspect(staff[:1]).get_descendants(
            ...     include_self=False,
            ...     ):
            ...     component
            ...
            Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            Note("c'8")
            Note("d'8")
            Note("e'8")

        Returns selection.
        '''
        import abjad
        if hasattr(self.client, '_get_descendants'):
            descendants = self.client._get_descendants(
                include_self=include_self,
                )
        else:
            descendants = []
            for argument in self.client:
                descendants_ = abjad.inspect(argument).get_descendants()
                for descendant_ in descendants_:
                    if descendant_ not in descendants:
                        descendants.append(descendant_)
            descendants = abjad.select(descendants)
        return descendants

    def get_duration(self, in_seconds=False):
        r'''Gets duration.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> selection = staff[:3]
            >>> abjad.inspect(selection).get_duration()
            Duration(3, 4)

        Returns duration.
        '''
        import abjad
        if hasattr(self.client, 'get_duration'):
            return self.client.get_duration(in_seconds=in_seconds)
        if hasattr(self.client, '_get_duration'):
            return self.client._get_duration(in_seconds=in_seconds)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        return sum([
            abjad.inspect(_).get_duration(in_seconds=in_seconds)
            for _ in self.client
            ])

    def get_effective(self, prototype=None, unwrap=True, n=0):
        r'''Gets effective indicator.

        ..  container:: example

            Gets effective clef:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, staff[0])
            >>> note = abjad.Note("fs'16")
            >>> container = abjad.AcciaccaturaContainer([note])
            >>> abjad.attach(container, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

            >>> for component in abjad.iterate(staff).components():
            ...     agent = abjad.inspect(component)
            ...     clef = agent.get_effective(abjad.Clef)
            ...     print(component, clef)
            ...
            Staff("c'4 d'4 e'4 f'4") Clef('alto')
            c'4 Clef('alto')
            d'4 Clef('alto')
            e'4 Clef('alto')
            fs'16 Clef('alto')
            f'4 Clef('alto')

        Returns indicator or none.
        '''
        if hasattr(self.client, '_get_effective'):
            return self.client._get_effective(
                prototype=prototype,
                unwrap=unwrap,
                n=n,
                )

    def get_effective_staff(self):
        r'''Gets effective staff.

        Returns staff or none.
        '''
        if hasattr(self.client, '_get_effective_staff'):
            return self.client._get_effective_staff()

    def get_grace_container(self):
        r'''Gets grace container attached to leaf.

        ..  container:: example

            Get acciaccatura container attached to note:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> note = abjad.Note("cs'16")
            >>> container = abjad.AcciaccaturaContainer([note])
            >>> abjad.attach(container, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    \acciaccatura {
                        cs'16
                    }
                    d'8
                    e'8
                    f'8
                }

            >>> abjad.inspect(staff[1]).get_grace_container()
            AcciaccaturaContainer("cs'16")

        Returns grace container, acciaccatura container, appoggiatura container
        or none.
        '''
        if hasattr(self.client, '_grace_container'):
            return self.client._grace_container

    def get_indicator(
        self,
        prototype=None,
        default=None,
        unwrap=True,
        ):
        r'''Gets indicator.

        Raises exception when more than one indicator of `prototype` attach to
        client.

        Returns default when no indicator of `prototype` attaches to client.

        Returns indicator or default.
        '''
        indicators = self.client._get_indicators(
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

    def get_indicators(self, prototype=None, unwrap=True):
        r'''Get indicators.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4 -\marcato
                    d'4 -\marcato
                    e'4 -\marcato
                    f'4 -\marcato
                }

            >>> abjad.inspect(staff).get_indicators(abjad.Articulation)
            ()

            >>> abjad.inspect(staff[0]).get_indicators(abjad.Articulation)
            (Articulation('^'),)

        Returns tuple.
        '''
        if hasattr(self.client, '_get_indicators'):
            return self.client._get_indicators(
                prototype=prototype,
                unwrap=unwrap,
                )

    def get_leaf(self, n=0):
        r'''Gets leaf `n`.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Voice("c'8 d'8 e'8 f'8"))
            >>> staff.append(abjad.Voice("g'8 a'8 b'8 c''8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

            Gets leaf `n` **from** client when client is a leaf.

            With positive indices:

            >>> first_leaf = staff[0][0]
            >>> first_leaf
            Note("c'8")

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

            >>> last_leaf = staff[0][-1]
            >>> last_leaf
            Note("f'8")

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

            Gets leaf `n` **in** client when client is a container.

            With positive indices:

            >>> first_voice = staff[0]
            >>> first_voice
            Voice("c'8 d'8 e'8 f'8")

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

            >>> first_voice = staff[0]
            >>> first_voice
            Voice("c'8 d'8 e'8 f'8")

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
        if isinstance(self.client, abjad.Leaf):
            return self.client._get_leaf(n)
        if 0 <= n:
            reverse = False
        else:
            reverse = True
            n = abs(n) - 1
        leaves = abjad.iterate(self.client).leaves(reverse=reverse)
        for i, leaf in enumerate(leaves):
            if i == n:
                return leaf

    def get_lineage(self):
        r'''Gets lineage.

        Returns lineage.
        '''
        if hasattr(self.client, '_get_lineage'):
            return self.client._get_lineage()

    def get_logical_tie(self):
        r'''Gets logical tie.

        Returns logical tie.
        '''
        if hasattr(self.client, '_get_logical_tie'):
            return self.client._get_logical_tie()

    def get_markup(self, direction=None):
        r'''Gets markup.

        Returns tuple.
        '''
        if hasattr(self.client, '_get_markup'):
            return self.client._get_markup(
                direction=direction,
                )

    def get_parentage(self, include_self=True, grace_notes=False):
        r'''Gets parentage.

        .. container:: example

            Gets parentage without grace notes:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.GraceContainer("c'16 d'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
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

            >>> abjad.inspect(container[0]).get_parentage()
            Parentage(component=Note("c'16"))

        .. container:: example

            Gets parentage with grace notes:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.GraceContainer("c'16 d'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
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

            >>> agent = abjad.inspect(container[0])
            >>> parentage = agent.get_parentage(grace_notes=True)
            >>> for component in parentage:
            ...     component
            ...
            Note("c'16")
            GraceContainer("c'16 d'16")
            Note("d'4")
            Voice("c'4 d'4 e'4 f'4")

        Returns parentage.
        '''
        return self.client._get_parentage(
            include_self=include_self,
            grace_notes=grace_notes,
            )

    def get_piecewise(self, prototype=None, default=None):
        r'''Gets piecewise indicators.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> spanner.attach(abjad.Markup('pont.'), staff[0])
            >>> spanner.attach(abjad.Markup('ord.'), staff[-1])
            >>> spanner.attach(abjad.ArrowLineSegment(), staff[0])
            >>> abjad.override(staff).text_script.staff_padding = 1.25
            >>> abjad.override(staff).text_spanner.staff_padding = 2
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

    def get_pitches(self):
        r'''Gets pitches.

        Returns pitch set.
        '''
        import abjad
        if not self.client:
            return
        return abjad.PitchSet.from_selection(abjad.select(self.client))

    def get_sounding_pitch(self):
        r'''Gets sounding pitch.

        ..  container:: example

            >>> staff = abjad.Staff("d''8 e''8 f''8 g''8")
            >>> piccolo = abjad.instrumenttools.Piccolo()
            >>> abjad.attach(piccolo, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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
        return self.client._get_sounding_pitch()

    def get_sounding_pitches(self):
        r"""Gets sounding pitches.

        ..  container:: example

            >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = abjad.instrumenttools.Glockenspiel()
            >>> abjad.attach(glockenspiel, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Glockenspiel }
                    \set Staff.shortInstrumentName = \markup { Gkspl. }
                    <c' e'>4
                    <d' fs'>4
                }

            >>> abjad.inspect(staff[0]).get_sounding_pitches()
            (NamedPitch("c'''"), NamedPitch("e'''"))

        Returns tuple.
        """
        return self.client._get_sounding_pitches()

    def get_spanner(self, prototype=None, default=None):
        r'''Gets spanner.

        Raises exception when more than one spanner of `prototype` attaches to
        client.

        Returns `default` when no spanner of `prototype` attaches to client.

        Returns spanner or default.
        '''
        spanners = self.client._get_spanners(prototype=prototype)
        if not spanners:
            return default
        elif len(spanners) == 1:
            return list(spanners)[0]
        else:
            message = 'multiple spanners attached to client.'
            raise Exception(message)

    def get_spanners(self, prototype=None):
        r'''Gets spanners.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:2])
            >>> abjad.attach(abjad.Beam(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8 [
                    d'8 ]
                    e'8 [
                    f'8 ]
                }

            >>> abjad.inspect(staff).get_spanners()
            set()

            >>> abjad.inspect(staff[0]).get_spanners()
            {Beam("c'8, d'8")}

            >>> beams = abjad.inspect(staff[:]).get_spanners()
            >>> beams = list(beams)
            >>> beams.sort()
            >>> beams
            [Beam("c'8, d'8"), Beam("e'8, f'8")]

        Returns set.
        '''
        import abjad
        if hasattr(self.client, 'get_spanners'):
            return self.client.get_spanners(prototype=prototype)
        if hasattr(self.client, '_get_spanners'):
            return self.client._get_spanners(prototype=prototype)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        result = set()
        for item in self.client:
            spanners_ = abjad.inspect(item).get_spanners(prototype=prototype)
            result.update(spanners_)
        return result

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan.

        ..  container:: example

            Gets timespan of grace notes:

            >>> voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
            >>> grace_notes = [abjad.Note("c'16"), abjad.Note("d'16")]
            >>> container = abjad.GraceContainer(grace_notes)
            >>> abjad.attach(container, voice[1])
            >>> container = abjad.AfterGraceContainer("e'16 f'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
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

            >>> for leaf in abjad.iterate(voice).leaves():
            ...     timespan = abjad.inspect(leaf).get_timespan()
            ...     print(str(leaf) + ':')
            ...     abjad.f(timespan)
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

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:2])
            >>> abjad.attach(abjad.Beam(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8 [
                    d'8 ]
                    e'8 [
                    f'8 ]
                }

            >>> abjad.inspect(staff).get_timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 2))

            >>> abjad.inspect(staff[0]).get_timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 8))

            >>> abjad.inspect(staff[:3]).get_timespan()
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 8))

        Returns timespan.
        '''
        import abjad
        if hasattr(self.client, 'get_timespan'):
            return self.client.get_timespan(in_seconds=in_seconds)
        if hasattr(self.client, '_get_timespan'):
            return self.client._get_timespan(in_seconds=in_seconds)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        timespan = abjad.inspect(self.client[0]).get_timespan(
            in_seconds=in_seconds,
            )
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for item in self.client[1:]:
            timespan = abjad.inspect(item).get_timespan(in_seconds=in_seconds)
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
        return abjad.Timespan(start_offset, stop_offset)

    def get_tuplet(self, n=0):
        r'''Gets tuplet `n`.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'8 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "d'8 e' f'"))
            >>> staff.append(abjad.Tuplet((2, 3), "e'8 f' g'"))
            >>> staff.append(abjad.Tuplet((2, 3), "f'8 g' a'"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \times 2/3 {
                        d'8
                        e'8
                        f'8
                    }
                    \times 2/3 {
                        e'8
                        f'8
                        g'8
                    }
                    \times 2/3 {
                        f'8
                        g'8
                        a'8
                    }
                }

        ..  container:: example

            >>> for n in range(4):
            ...     tuplet = abjad.inspect(staff).get_tuplet(n)
            ...     print(n, tuplet)
            ...
            0 Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
            1 Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")
            2 Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
            3 Tuplet(Multiplier(2, 3), "f'8 g'8 a'8")

            >>> for n in range(-1, -5, -1):
            ...     tuplet = abjad.inspect(staff).get_tuplet(n)
            ...     print(n, tuplet)
            ...
            -1 Tuplet(Multiplier(2, 3), "f'8 g'8 a'8")
            -2 Tuplet(Multiplier(2, 3), "e'8 f'8 g'8")
            -3 Tuplet(Multiplier(2, 3), "d'8 e'8 f'8")
            -4 Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")

        Returns tuplet or none.
        '''
        import abjad
        if 0 <= n:
            reverse = False
        else:
            reverse = True
            n = abs(n) - 1
        tuplets = abjad.iterate(self.client).components(
            abjad.Tuplet,
            reverse=reverse,
            )
        for i, tuplet in enumerate(tuplets):
            if i == n:
                return tuplet

    def get_vertical_moment(self, governor=None):
        r'''Gets vertical moment.

        ..  container:: example

            >>> score = abjad.Score()
            >>> tuplet = abjad.Tuplet((4, 3), "d''8 c''8 b'8")
            >>> score.append(abjad.Staff([tuplet]))
            >>> staff_group = abjad.StaffGroup(context_name='PianoStaff')
            >>> staff_group.append(abjad.Staff("a'4 g'4"))
            >>> staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff_group[1][0])
            >>> score.append(staff_group)
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
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

            >>> agent = abjad.inspect(staff_group[1][1])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("a'4"), Note("e'8")])

            >>> agent = abjad.inspect(staff_group[1][2])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("d'8")])

            >>> agent = abjad.inspect(staff_group[1][3])
            >>> moment = agent.get_vertical_moment(governor=staff_group)
            >>> moment.leaves
            Selection([Note("g'4"), Note("c'8")])

        Returns vertical moment.
        '''
        return self.client._get_vertical_moment(
            governor=governor,
            )

    def get_vertical_moment_at(self, offset):
        r'''Gets vertical moment at `offset`.

        Returns vertical moment.
        '''
        return self.client._get_vertical_moment_at(
            offset,
            )

    def has_effective_indicator(self, prototype=None):
        r'''Is true when client has effective indicator. Otherwise false.

        Returns true or false.
        '''
        return self.client._has_effective_indicator(prototype=prototype)

    def has_indicator(self, prototype=None):
        r'''Is true when client has one or more indicators. Otherwise false.

        Returns true or false.
        '''
        return self.client._has_indicator(prototype=prototype)

    def has_spanner(self, prototype=None):
        r'''Is true when client has one or more spanners. Otherwise false.

        Returns true or false.
        '''
        return self.client._has_spanner(prototype=prototype)

    def is_bar_line_crossing(self):
        r'''Is true when client crosses bar line. Otherwise false.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4")
            >>> time_signature = abjad.TimeSignature((3, 8))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            >>> for note in staff:
            ...     result = abjad.inspect(note).is_bar_line_crossing()
            ...     print(note, result)
            ...
            c'4 False
            d'4 True
            e'4 False

        Returns true or false.
        '''
        import abjad
        time_signature = self.client._get_effective(abjad.TimeSignature)
        if time_signature is None:
            time_signature_duration = abjad.Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, 'partial', 0)
        partial = partial or 0
        start_offset = abjad.inspect(self.client).get_timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self.client._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def is_grace_note(self):
        r'''Is true when client is grace note.

        Returns true or false.
        '''
        import abjad
        if not isinstance(self.client, abjad.Leaf):
            return False
        prototype = (abjad.AfterGraceContainer, abjad.GraceContainer)
        for component in abjad.inspect(self.client).get_parentage():
            if isinstance(component, prototype):
                return True
        return False

    def is_well_formed(
        self,
        check_beamed_long_notes=True,
        check_discontiguous_spanners=True,
        check_duplicate_ids=True,
        check_empty_containers=True,
        check_intermarked_hairpins=True,
        check_misdurated_measures=True,
        check_misfilled_measures=True,
        check_mismatched_enchained_hairpins=True,
        check_mispitched_ties=True,
        check_misrepresented_flags=True,
        check_missing_parents=True,
        check_nested_measures=True,
        check_notes_on_wrong_clef=True,
        check_out_of_range_notes=True,
        check_overlapping_beams=True,
        check_overlapping_glissandi=True,
        check_overlapping_hairpins=True,
        check_overlapping_octavation_spanners=True,
        check_overlapping_ties=True,
        check_overlapping_trill_spanners=True,
        check_tied_rests=True,
        ):
        r'''Is true when client is well-formed. Otherwise false.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 [ d' e' f'4. ]")

            >>> abjad.inspect(staff[:3]).is_well_formed()
            True

            >>> abjad.inspect(staff[-1]).is_well_formed()
            False

            >>> abjad.inspect(staff).is_well_formed()
            False

        ..  container:: example

            Checks can be turned off:

            >>> staff = abjad.Staff("c'8 [ d' e' f'4. ]")

            >>> abjad.inspect(staff[:3]).is_well_formed(
            ...     check_beamed_long_notes=False,
            ...     )
            True

            >>> abjad.inspect(staff[-1]).is_well_formed(
            ...     check_beamed_long_notes=False,
            ...     )
            True

            >>> abjad.inspect(staff).is_well_formed(
            ...     check_beamed_long_notes=False,
            ...     )
            True

        Returns false.
        '''
        import abjad
        manager = abjad.WellformednessManager()
        for violators, total, check_name in manager(self.client):
            if eval(check_name) is not True:
                continue
            if violators:
                return False
        return True

    def report_modifications(self):
        r'''Reports modifications.

        ..  container:: example

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.override(container).note_head.color = 'red'
            >>> abjad.override(container).note_head.style = 'harmonic'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
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

            >>> report = abjad.inspect(container).report_modifications()
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
        import abjad
        manager = abjad.LilyPondFormatManager
        client = self.client
        bundle = manager.bundle_format_contributions(client)
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

    def tabulate_wellformedness(
        self,
        allow_percussion_clef=None,
        check_beamed_long_notes=True,
        check_discontiguous_spanners=True,
        check_duplicate_ids=True,
        check_empty_containers=True,
        check_intermarked_hairpins=True,
        check_misdurated_measures=True,
        check_misfilled_measures=True,
        check_mismatched_enchained_hairpins=True,
        check_mispitched_ties=True,
        check_misrepresented_flags=True,
        check_missing_parents=True,
        check_nested_measures=True,
        check_notes_on_wrong_clef=True,
        check_out_of_range_notes=True,
        check_overlapping_beams=True,
        check_overlapping_glissandi=True,
        check_overlapping_hairpins=True,
        check_overlapping_octavation_spanners=True,
        check_overlapping_ties=True,
        check_overlapping_trill_spanners=True,
        check_tied_rests=True,
        ):
        r'''Tabulates well-formedness.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = (1, 4)
            >>> beam = abjad.Beam()
            >>> abjad.attach(beam, staff[:])

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            >>> agent = abjad.inspect(staff)
            >>> result = agent.tabulate_wellformedness()

            >>> print(result)
            1 /	1 beamed long notes
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
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

            Beamed long notes are not well-formed.

        ..  container:: example

            Checks can be turned off:

            >>> agent = abjad.inspect(staff)
            >>> result = agent.tabulate_wellformedness(
            ...     check_overlapping_beams=False, 
            ...     check_overlapping_glissandi=False, 
            ...     check_overlapping_hairpins=False, 
            ...     check_overlapping_octavation_spanners=False, 
            ...     check_overlapping_ties=False, 
            ...     check_overlapping_trill_spanners=False, 
            ...     )

            >>> print(result)
            1 /	1 beamed long notes
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
            0 /	0 tied rests

        Returns string.
        '''
        import abjad
        manager = abjad.WellformednessManager(
            allow_percussion_clef=allow_percussion_clef,
            )
        triples = manager(self.client)
        strings = []
        for violators, total, check_name in triples:
            if eval(check_name) is not True:
                continue
            violator_count = len(violators)
            string = '{} /\t{} {}'
            check_name = check_name.replace('check_', '')
            check_name = check_name.replace('_', ' ')
            string = string.format(violator_count, total, check_name)
            strings.append(string)
        return '\n'.join(strings)
