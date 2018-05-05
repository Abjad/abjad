import collections
import typing
from abjad.tools import abctools
from abjad.tools.exceptiontools import ExtraSpannerError
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools.inspect import inspect
from .Container import Container


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
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice
                    {
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

    def annotations(self):
        r'''Gets annotation wrappers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.annotate(staff[0], 'default_clef', abjad.Clef('tenor'))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> for wrapper in abjad.inspect(staff[0]).annotations():
            ...     abjad.f(wrapper)
            ...
            abjad.Wrapper(
                annotation='default_instrument',
                indicator=abjad.Cello(
                    name='cello',
                    short_name='vc.',
                    markup=abjad.Markup(
                        contents=['Cello'],
                        ),
                    short_markup=abjad.Markup(
                        contents=['Vc.'],
                        ),
                    allowable_clefs=('bass', 'tenor', 'treble'),
                    context='Staff',
                    default_tuning=abjad.Tuning(
                        pitches=abjad.PitchSegment(
                            (
                                abjad.NamedPitch('c,'),
                                abjad.NamedPitch('g,'),
                                abjad.NamedPitch('d'),
                                abjad.NamedPitch('a'),
                                ),
                            item_class=abjad.NamedPitch,
                            ),
                        ),
                    middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                    pitch_range=abjad.PitchRange('[C2, G5]'),
                    ),
                tag=abjad.Tag(),
                )
            abjad.Wrapper(
                annotation='default_clef',
                indicator=abjad.Clef('tenor'),
                tag=abjad.Tag(),
                )

        Returns list of annotations or list of wrappers.
        '''
        result = []
        for wrapper in getattr(self.client, '_wrappers', []):
            if wrapper.annotation:
                result.append(wrapper)
        return result

    def effective_wrapper(self, prototype=None, n=0):
        r'''Gets effective wrapper.

        ..  container:: example

            Gets effective clef wrapper:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.attach(abjad.AcciaccaturaContainer("fs'16"), staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
            ...     inspection = abjad.inspect(component)
            ...     wrapper = inspection.effective_wrapper(abjad.Clef)
            ...     print(component, wrapper)
            ...
            Staff("c'4 d'4 e'4 f'4") Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            c'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            d'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            e'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            fs'16 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())
            f'4 Wrapper(context='Staff', indicator=Clef('alto'), tag=Tag())

        Returns wrapper or none.
        '''
        return self.get_effective(prototype=prototype, n=n, unwrap=False)

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
                \new Staff
                {
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

    def get_annotation(self, annotation, default=None, unwrap=True):
        r'''Gets annotation.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 e' e' f'")
            >>> abjad.annotate(staff[0], 'default_instrument', abjad.Cello())
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    e'4
                    e'4
                    f'4
                }

            >>> string = 'default_instrument'
            >>> abjad.inspect(staff[0]).get_annotation(string)
            Cello()

            >>> abjad.inspect(staff[1]).get_annotation(string) is None
            True

            >>> abjad.inspect(staff[2]).get_annotation(string) is None
            True

            >>> abjad.inspect(staff[3]).get_annotation(string) is None
            True

            Returns default when no annotation is found:

            >>> abjad.inspect(staff[3]).get_annotation(string, abjad.Violin())
            Violin()

        ..  container:: example

            Regression: annotation is not picked up as effective indicator:

            >>> prototype = abjad.Instrument
            >>> abjad.inspect(staff[0]).get_effective(prototype) is None
            True

            >>> abjad.inspect(staff[1]).get_effective(prototype) is None
            True

            >>> abjad.inspect(staff[2]).get_effective(prototype) is None
            True

            >>> abjad.inspect(staff[3]).get_effective(prototype) is None
            True

        Returns annotation (or default).
        '''
        assert isinstance(annotation, str), repr(annotation)
        for wrapper in self.annotations():
            if wrapper.annotation == annotation:
                if unwrap is True:
                    return wrapper.indicator
                else:
                    return wrapper
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
                \new Staff
                {
                    c'8
                    [
                    d'4
                    e'8
                    f'8
                    ]
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
                \new Staff
                {
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
                \new Staff
                {
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
                \new Staff
                {
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

    def get_effective(self, prototype=None, unwrap=True, n=0, default=None):
        r'''Gets effective indicator.

        ..  container:: example

            Gets effective clef:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Clef('alto'), staff[0])
            >>> abjad.attach(abjad.AcciaccaturaContainer("fs'16"), staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
            ...     clef = abjad.inspect(component).get_effective(abjad.Clef)
            ...     print(component, clef)
            ...
            Staff("c'4 d'4 e'4 f'4") Clef('alto')
            c'4 Clef('alto')
            d'4 Clef('alto')
            e'4 Clef('alto')
            fs'16 Clef('alto')
            f'4 Clef('alto')

        ..  container:: example

            Arbitrary objects (like strings) can be contexted:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.attach('color', staff[1], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> for component in abjad.iterate(staff).components():
            ...     string = abjad.inspect(component).get_effective(str)
            ...     print(component, repr(string))
            ...
            Staff("c'8 d'8 e'8 f'8") None
            c'8 None
            d'8 'color'
            e'8 'color'
            f'8 'color'

        ..  container:: example

            Scans forwards or backwards when `n` is set: 

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8")
            >>> abjad.attach('red', staff[0], context='Staff')
            >>> abjad.attach('blue', staff[2], context='Staff')
            >>> abjad.attach('yellow', staff[4], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                }
                
            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[0]).get_effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[1]).get_effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 None
            0 'red'
            1 'blue'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[2]).get_effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[3]).get_effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'red'
            0 'blue'
            1 'yellow'

            >>> for n in (-1, 0, 1):
            ...     color = abjad.inspect(staff[4]).get_effective(str, n=n)
            ...     print(n, repr(color))
            ...
            -1 'blue'
            0 'yellow'
            1 None

        ..  container:: example

            Synthetic offsets works this way:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> abjad.attach(
            ...     'red',
            ...     staff[-1],
            ...     context='Staff',
            ...     synthetic_offset=-1,
            ...     )
            >>> abjad.attach('blue', staff[0], context='Staff')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }

            Entire staff is effectively blue:

            >>> abjad.inspect(staff).get_effective(str)
            'blue'

            The (synthetic) offset just prior to (start of) staff is red:

            >>> abjad.inspect(staff).get_effective(str, n=-1)
            'red'

        ..  container:: example

            Gets effective time signature:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(abjad.TimeSignature((3, 8)), leaves[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> prototype = abjad.TimeSignature
            >>> for component in abjad.iterate(staff).components():
            ...     inspection = abjad.inspect(component)
            ...     time_signature = inspection.get_effective(prototype)
            ...     print(component, time_signature)
            ...
            Staff("c'4 d'4 e'4 f'4") 3/8
            c'4 3/8
            d'4 3/8
            e'4 3/8
            f'4 3/8

        Returns indicator or none.
        '''
        if hasattr(self.client, '_get_effective'):
            result = self.client._get_effective(
                prototype=prototype,
                unwrap=unwrap,
                n=n,
                )
            if result is None:
                return default
            return result

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
                \new Staff
                {
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
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
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
                \new Staff
                {
                    \new Voice
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Voice
                    {
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
                \new Voice
                {
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
                \new Voice
                {
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

    def get_piecewise(
        self,
        spanner,
        prototype=None,
        default=None,
        unwrap=True,
        ):
        r'''Gets piecewise indicators for ``spanner``.

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
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                }
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                ord.
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            >>> for leaf in staff:
            ...     leaf, abjad.inspect(leaf).get_piecewise(spanner, abjad.Markup)
            ...
            (Note("c'4"), Markup(contents=['pont.']))
            (Note("d'4"), None)
            (Note("e'4"), None)
            (Note("f'4"), Markup(contents=['ord.']))

        Returns indicator or default.
        '''
        import abjad
        assert isinstance(spanner, abjad.Spanner)
        wrappers = self.wrappers(prototype=prototype)
        wrappers = wrappers or []
        wrappers = [_ for _ in wrappers if _.spanner is spanner]
        if not wrappers:
            return default
        if len(wrappers) == 1:
            if unwrap:
                return wrappers[0].indicator
            else:
                return wrappers[0]
        if 1 < len(wrappers):
            name = prototype.__name__
            client = str(self.client)
            raise Exception(f'multiple {name} attached to {client}.')

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
            >>> piccolo = abjad.Piccolo()
            >>> abjad.attach(piccolo, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.instrumentName = \markup { Piccolo }
                    \set Staff.shortInstrumentName = \markup { Picc. }
                    d'8
                    e'8
                    f'8
                    g'8
                }

        Returns named pitch.
        '''
        return self.client._get_sounding_pitch()

    def get_sounding_pitches(self):
        r"""Gets sounding pitches.

        ..  container:: example

            >>> staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = abjad.Glockenspiel()
            >>> abjad.attach(glockenspiel, staff[0])
            >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
        assert isinstance(spanners, list), repr(spanners)
        if not spanners:
            return default
        elif len(spanners) == 1:
            return spanners[0]
        else:
            raise ExtraSpannerError

    def get_spanners(self, prototype=None) -> typing.List[Spanner]:
        r'''Gets spanners.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:2])
            >>> abjad.attach(abjad.Beam(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
                }

            >>> abjad.inspect(staff).get_spanners()
            []

            >>> abjad.inspect(staff[0]).get_spanners()
            [Beam("c'8, d'8")]

            >>> beams = abjad.inspect(staff[:]).get_spanners()
            >>> beams = list(beams)
            >>> beams.sort()
            >>> beams
            [Beam("c'8, d'8"), Beam("e'8, f'8")]

        '''
        if isinstance(self.client, Container):
            return []
        if hasattr(self.client, 'get_spanners'):
            return self.client.get_spanners(prototype=prototype)
        if hasattr(self.client, '_get_spanners'):
            return self.client._get_spanners(prototype=prototype)
        assert isinstance(self.client, collections.Iterable), repr(self.client)
        known_ids: typing.List[int] = []
        result = []
        for item in self.client:
            for spanner in inspect(item).get_spanners(prototype=prototype):
                id_ = id(spanner)
                if id_ not in known_ids:
                    known_ids.append(id_)
                    result.append(spanner)
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
                \new Voice
                {
                    c'8
                    [
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
                    f'8
                    ]
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
                \new Staff
                {
                    c'8
                    [
                    d'8
                    ]
                    e'8
                    [
                    f'8
                    ]
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
                \new Staff
                {
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
            >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
            >>> staff_group.append(abjad.Staff("a'4 g'4"))
            >>> staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff_group[1][0])
            >>> score.append(staff_group)
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            a'4
                            g'4
                        }
                        \new Staff
                        {
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
        return self.client._get_vertical_moment(governor=governor)

    def get_vertical_moment_at(self, offset):
        r'''Gets vertical moment at `offset`.

        Returns vertical moment.
        '''
        return self.client._get_vertical_moment_at(offset)

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
                \new Staff
                {
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

            Reports container modifications:

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

        ..  container:: example

            Reports leaf modifications:

            >>> container = abjad.Container("c'8 d'8 e'8 f'8")
            >>> abjad.attach(abjad.Clef('alto'), container[0])
            >>> abjad.override(container[0]).note_head.color = 'red'
            >>> abjad.override(container[0]).stem.color = 'red'
            >>> abjad.show(container) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(container)
                {
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> report = abjad.inspect(container[0]).report_modifications()
            >>> print(report)
            slot absolute before:
            slot 1:
                grob overrides:
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
            slot 3:
                commands:
                    \clef "alto"
            slot 4:
                leaf body:
                    c'8
            slot 5:
            slot 7:
            slot absolute after:

        Returns string.
        '''
        import abjad
        if isinstance(self.client, abjad.Container):
            bundle = abjad.LilyPondFormatManager.bundle_format_contributions(
                self.client
                )
            result = []
            for slot in ('before', 'open brackets', 'opening'):
                lines = self.client._get_format_contributions_for_slot(
                    slot,
                    bundle,
                    )
                result.extend(lines)
            line = '    %%% {} components omitted %%%'
            line = line.format(len(self.client))
            result.append(line)
            for slot in ('closing', 'close brackets', 'after'):
                lines = self.client._get_format_contributions_for_slot(
                    slot,
                    bundle,
                    )
                result.extend(lines)
            result = '\n'.join(result)
            return result
        elif isinstance(self.client, abjad.Leaf):
            return self.client._report_format_contributions()
        else:
            message = 'only defined for components: {}.'
            message = message.format(self.client)
            return message

    def tabulate_wellformedness(
        self,
        allow_percussion_clef=None,
        check_beamed_long_notes=True,
        check_discontiguous_spanners=True,
        check_duplicate_ids=True,
        check_empty_containers=True,
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
                \new Staff
                {
                    c'8
                    [
                    d'4
                    e'8
                    f'8
                    ]
                }

            >>> agent = abjad.inspect(staff)
            >>> result = agent.tabulate_wellformedness()

            >>> print(result)
            1 /	1 beamed long notes
            0 /	1 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
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
            0 /	0 overlapping trill spanners
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

    def wrapper(self, prototype=None):
        r'''Gets wrapper.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
                }

            >>> abjad.inspect(staff).wrapper(abjad.Articulation) is None
            True

            >>> abjad.inspect(staff[0]).wrapper(abjad.Articulation)
            Wrapper(indicator=Articulation('^'), tag=Tag())

        Raises exception when more than one indicator of `prototype` attach to
        client.

        Returns wrapper or none.
        '''
        return self.get_indicator(prototype=prototype, unwrap=False)

    def wrappers(self, prototype=None):
        r'''Gets wrappers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Articulation('^'), staff[0])
            >>> abjad.attach(abjad.Articulation('^'), staff[1])
            >>> abjad.attach(abjad.Articulation('^'), staff[2])
            >>> abjad.attach(abjad.Articulation('^'), staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    -\marcato
                    d'4
                    -\marcato
                    e'4
                    -\marcato
                    f'4
                    -\marcato
                }

            >>> abjad.inspect(staff).wrappers(abjad.Articulation)
            ()

            >>> abjad.inspect(staff[0]).wrappers(abjad.Articulation)
            (Wrapper(indicator=Articulation('^'), tag=Tag()),)

        Returns tuple of wrappers or none.
        '''
        return self.get_indicators(prototype=prototype, unwrap=False)
