# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import iterate


class MutationAgent(abctools.AbjadObject):
    r'''Mutation agent.

    ..  container:: example

        **Example 1.** Creates mutation agent for last two notes in staff:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> mutate(staff[2:])
            MutationAgent(client=Selection([Note("d'4"), Note("f'4")]))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### PUBLIC METHODS ###

    def copy(self, n=1, include_enclosing_containers=False):
        r'''Copies component and fractures crossing spanners.

        ..  todo:: Add examples.

        Returns new component.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(self._client, scoretools.Component):
            selection = selectiontools.Selection(self._client)
        else:
            selection = self._client
        result = selection._copy(
            n=n,
            include_enclosing_containers=include_enclosing_containers,
            )
        if isinstance(self._client, scoretools.Component):
            if len(result) == 1:
                result = result[0]
        return result

    def eject_contents(self):
        r'''Ejects contents from outside-of-score container.

        ..  container:: example

            **Example 1.** Ejects leaves from container:

            ::

                >>> container = Container("c'4 ~ c'4 d'4 ~ d'4")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    c'4 ~
                    c'4
                    d'4 ~
                    d'4
                }

            Returns container contents as a selection with spanners preserved:

            ::

                >>> contents = mutate(container).eject_contents()
                >>> contents
                Selection([Note("c'4"), Note("c'4"), Note("d'4"), Note("d'4")])

            Container contents can be safely added to a new container:

            ::

                >>> staff = Staff(contents, context_name='RhythmicStaff')
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new RhythmicStaff {
                    c'4 ~
                    c'4
                    d'4 ~
                    d'4
                }

            New container is well formed:

            ::

                >>> inspect_(staff).is_well_formed()
                True

            Old container is empty:

            ::

                >>> container
                Container()

        Returns container contents as selection.
        '''
        return self._client._eject_contents()

    def extract(self, scale_contents=False):
        r'''Extracts mutation client from score.

        Leaves children of mutation client in score.

        ..  container:: example

            **Example 1.** Extract tuplet:

            ::

                >>> staff = Staff()
                >>> time_signature = TimeSignature((3, 4))
                >>> attach(time_signature, staff)
                >>> staff.append(Tuplet((3, 2), "c'4 e'4"))
                >>> staff.append(Tuplet((3, 2), "d'4 f'4"))
                >>> hairpin = spannertools.Hairpin('p < f')
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> attach(hairpin, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        c'4 \< \p
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        d'4
                        f'4 \f
                    }
                }

            ::

                >>> empty_tuplet = mutate(staff[-1]).extract()
                >>> empty_tuplet = mutate(staff[0]).extract()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/4
                    c'4 \< \p
                    e'4
                    d'4
                    f'4 \f
                }

        ..  container:: example

            **Example 2.** Scale tuplet contents and then extract tuplet:

            ::

                >>> staff = Staff()
                >>> time_signature = TimeSignature((3, 4))
                >>> attach(time_signature, staff)
                >>> staff.append(Tuplet((3, 2), "c'4 e'4"))
                >>> staff.append(Tuplet((3, 2), "d'4 f'4"))
                >>> hairpin = spannertools.Hairpin('p < f')
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> attach(hairpin, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        c'4 \< \p
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/2 {
                        d'4
                        f'4 \f
                    }
                }

            ::

                >>> empty_tuplet = mutate(staff[-1]).extract(
                ...     scale_contents=True)
                >>> empty_tuplet = mutate(staff[0]).extract(
                ...     scale_contents=True)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/4
                    c'4. \< \p
                    e'4.
                    d'4.
                    f'4. \f
                }

        Returns mutation client.
        '''
        return self._client._extract(scale_contents=scale_contents)

    def fuse(self):
        r'''Fuses mutation client.

        ..  container:: example

            **Example 1.** Fuse in-score leaves:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> mutate(staff[1:]).fuse()
                [Note("d'4.")]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    d'4.
                }

        ..  container:: example

            **Example 2.** Fuse parent-contiguous fixed-duration tuplets
            in selection:

            ::

                >>> tuplet_1 = scoretools.FixedDurationTuplet(
                ...     Duration(2, 8), [])
                >>> tuplet_1.extend("c'8 d'8 e'8")
                >>> beam = spannertools.Beam()
                >>> attach(beam, tuplet_1[:])
                >>> duration = Duration(2, 16)
                >>> tuplet_2 = scoretools.FixedDurationTuplet(duration, [])
                >>> tuplet_2.extend("c'16 d'16 e'16")
                >>> slur = spannertools.Slur()
                >>> attach(slur, tuplet_2[:])
                >>> staff = Staff([tuplet_1, tuplet_2])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                    }
                    \times 2/3 {
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            ::

                >>> tuplets = staff[:]
                >>> mutate(tuplets).fuse()
                FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8 c'16 d'16 e'16")
                >>> show(staff) #doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            Returns new tuplet.

            Fuses zero or more parent-contiguous `tuplets`.

            Allows in-score `tuplets`.

            Allows outside-of-score `tuplets`.

            All `tuplets` must carry the same multiplier.

            All `tuplets` must be of the same type.

        ..  container:: example

            **Example 3.** Fuse in-score measures:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((1, 4), "c'8 d'8"))
                >>> staff.append(Measure((2, 8), "e'8 f'8"))
                >>> slur = spannertools.Slur()
                >>> leaves = select(staff).by_leaf()
                >>> attach(slur, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 1/4
                        c'8 (
                        d'8
                    }
                    {
                        \time 2/8
                        e'8
                        f'8 )
                    }
                }

            ::

                >>> measures = staff[:]
                >>> mutate(measures).fuse()
                Measure((2, 4), "c'8 d'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 2/4
                        c'8 (
                        d'8
                        e'8
                        f'8 )
                    }
                }

        Returns fused mutation client.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(self._client, scoretools.Component):
            selection = selectiontools.Selection(self._client)
            return selection._fuse()
        elif isinstance(self._client, selectiontools.Selection) and \
            self._client._all_are_contiguous_components_in_same_logical_voice(
            self._client):
            selection = selectiontools.Selection(self._client)
            return selection._fuse()

    def replace(self, recipients):
        r'''Replaces mutation client (and contents of mutation client)
        with `recipients`.

        ..  container:: example

            **Example 1.** Replace in-score tuplet (and children of tuplet)
            with notes. Functions exactly the same as container setitem:

                >>> tuplet_1 = Tuplet((2, 3), "c'4 d'4 e'4")
                >>> tuplet_2 = Tuplet((2, 3), "d'4 e'4 f'4")
                >>> staff = Staff([tuplet_1, tuplet_2])
                >>> hairpin = spannertools.Hairpin('p < f')
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> attach(hairpin, leaves)
                >>> slur = spannertools.Slur()
                >>> attach(slur, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 2/3 {
                        c'4 \< \p (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4 \f )
                    }
                }

            ::

                >>> notes = scoretools.make_notes(
                ...     "c' d' e' f' c' d' e' f'",
                ...     Duration(1, 16),
                ...     )
                >>> mutate([tuplet_1]).replace(notes)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'16 \< \p (
                    d'16
                    e'16
                    f'16
                    c'16
                    d'16
                    e'16
                    f'16
                    \times 2/3 {
                        d'4
                        e'4
                        f'4 \f )
                    }
                }

            Preserves both hairpin and slur.

        Returns none.
        '''
        from abjad.tools import selectiontools
        if isinstance(self._client, selectiontools.Selection):
            donors = self._client
        else:
            donors = selectiontools.Selection(self._client)
        assert donors._all_are_contiguous_components_in_same_parent(donors)
        if not isinstance(recipients, selectiontools.Selection):
            recipients = selectiontools.Selection(recipients)
        assert recipients._all_are_contiguous_components_in_same_parent(
            recipients)
        if donors:
            parent, start, stop = \
                donors._get_parent_and_start_stop_indices()
            assert parent is not None, repr(donors)
            parent.__setitem__(slice(start, stop + 1), recipients)

    # TODO: fix bug in function that causes tied notes to become untied
    def replace_measure_contents(self, new_contents):
        r'''Replaces contents of measures in client with `new_contents`.

        ..  container:: example

            **Example 1.** Replaces skip-filled measures with notes:

            ::

                >>> pairs = [(1, 8), (3, 16)]
                >>> measures = scoretools.make_spacer_skip_measures(pairs)
                >>> staff = Staff(measures)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 1/8
                        s1 * 1/8
                    }
                    {
                        \time 3/16
                        s1 * 3/16
                    }
                }

            ::

                >>> notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
                >>> mutate(staff).replace_measure_contents(notes)
                [Measure((1, 8), "c'16 d'16"), Measure((3, 16), "e'16 f'16 s1 * 1/16")]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 1/8
                        c'16
                        d'16
                    }
                    {
                        \time 3/16
                        e'16
                        f'16
                        s1 * 1/16
                    }
                }

        Preserves duration of all measures.

        Skips measures that are too small.

        Pads extra space at end of measures with spacer skip.

        Raises stop iteration if not enough measures.

        Returns measures iterated.
        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import detach
        # init return list
        result = []
        # get first measure and first time signature
        current_measure = scoretools.get_next_measure_from_component(
            self._client)
        result.append(current_measure)
        current_time_signature = current_measure.time_signature
        # to avoide pychecker slice assignment error
        #del(current_measure[:])
        current_measure.__delitem__(slice(0, len(current_measure)))
        # iterate new contents
        while new_contents:
            # find candidate duration of new element plus current measure
            current_element = new_contents[0]
            multiplier = current_time_signature.implied_prolation
            preprolated_duration = current_element._preprolated_duration
            duration = multiplier * preprolated_duration
            candidate_duration = current_measure._get_duration() + duration
            # if new element fits in current measure
            if candidate_duration <= current_time_signature.duration:
                current_element = new_contents.pop(0)
                current_measure._append_without_withdrawing_from_crossing_spanners(
                    current_element)
            # otherwise restore current measure and advance to next measure
            else:
                current_time_signature = \
                    indicatortools.TimeSignature(current_time_signature)
                detach(indicatortools.TimeSignature, current_measure)
                attach(current_time_signature, current_measure)
                scoretools.append_spacer_skips_to_underfull_measures_in_expr(
                    [current_measure])
                current_measure = scoretools.get_next_measure_from_component(
                    current_measure)
                if current_measure is None:
                    raise StopIteration
                result.append(current_measure)
                current_time_signature = current_measure.time_signature
                # to avoid pychecker slice assignment error
                #del(current_measure[:])
                current_measure.__delitem__(slice(0, len(current_measure)))
        # restore last iterated measure
        current_time_signature = \
            indicatortools.TimeSignature(current_time_signature)
        detach(indicatortools.TimeSignature, current_measure)
        attach(current_time_signature, current_measure)
        scoretools.append_spacer_skips_to_underfull_measures_in_expr(
            current_measure)
        # return iterated measures
        return result

    def respell_with_flats(self):
        r'''Respell named pitches in mutation client with flats:

        ..  container:: example

            **Example 1.** Respells notes in staff:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

            ::

                >>> mutate(staff).respell_with_flats()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    df'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        for leaf in iterate(self._client).by_class(scoretools.Leaf):
            if isinstance(leaf, scoretools.Chord):
                for note_head in leaf.note_heads:
                    note_head.written_pitch = \
                        note_head.written_pitch.respell_with_flats()
            elif hasattr(leaf, 'written_pitch'):
                leaf.written_pitch = leaf.written_pitch.respell_with_flats()

    def respell_with_sharps(self):
        r'''Respell named pitches in mutation client with sharps:

        ..  container:: example

            **Example 1.** Respells notes in staff:

            ::

                >>> staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ef'8
                    e'8
                    f'8
                }

            ::

                >>> mutate(staff).respell_with_sharps()
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8
                    cs'8
                    d'8
                    ds'8
                    e'8
                    f'8
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        for leaf in iterate(self._client).by_class(scoretools.Leaf):
            if isinstance(leaf, scoretools.Chord):
                for note_head in leaf.note_heads:
                    note_head.written_pitch = \
                        note_head.written_pitch.respell_with_sharps()
            elif hasattr(leaf, 'written_pitch'):
                leaf.written_pitch = leaf.written_pitch.respell_with_sharps()

    def rewrite_meter(
        self,
        meter,
        boundary_depth=None,
        initial_offset=None,
        maximum_dot_count=None,
        rewrite_tuplets=True,
        use_messiaen_style_ties=False,
        ):
        r'''Rewrite the contents of logical ties in an expression to match
        a meter.

        ..  container:: example

            **Example 1.** Rewrite the contents of a measure in a staff
            using the default meter for that measure's time signature:

            ::

                >>> parseable = "abj: | 2/4 c'2 ~ |"
                >>> parseable += "| 4/4 c'32 d'2.. ~ d'16 e'32 ~ |"
                >>> parseable += "| 2/4 e'2 |"
                >>> staff = Staff(parseable)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 2/4
                        c'2 ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2.. ~
                        d'16
                        e'32 ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            ::

                >>> meter = metertools.Meter((4, 4))
                >>> print(meter.pretty_rtm_format)
                (4/4 (
                    1/4
                    1/4
                    1/4
                    1/4))

            ::

                >>> mutate(staff[1][:]).rewrite_meter(meter)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 2/4
                        c'2 ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'8.. ~
                        d'2 ~
                        d'8..
                        e'32 ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            **Example 2.** Rewrite the contents of a measure in a staff
            using a custom meter:

            ::

                >>> staff = Staff(parseable)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 2/4
                        c'2 ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2.. ~
                        d'16
                        e'32 ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            ::

                >>> rtm = '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
                >>> meter = metertools.Meter(rtm)
                >>> print(meter.pretty_rtm_format) # doctest: +SKIP
                (4/4 (
                    (2/4 (
                        1/4
                        1/4))
                    (2/4 (
                        1/4
                        1/4))))

            ::

                >>> mutate(staff[1][:]).rewrite_meter(meter)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 2/4
                        c'2 ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'4... ~
                        d'4...
                        e'32 ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            **Example 3.** Limit the maximum number of dots per leaf using
            `maximum_dot_count`:

            ::

                >>> parseable = "abj: | 3/4 c'32 d'8 e'8 fs'4... |"
                >>> measure = parse(parseable)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 3/4
                    c'32
                    d'8
                    e'8
                    fs'4...
                }

            Without constraining the `maximum_dot_count`:

            ::

                >>> mutate(measure[:]).rewrite_meter(measure)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 3/4
                    c'32
                    d'16. ~
                    d'32
                    e'16. ~
                    e'32
                    fs'4...
                }

            Constraining the `maximum_dot_count` to `2`:

            ::

                >>> measure = parse(parseable)
                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     maximum_dot_count=2,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 3/4
                    c'32
                    d'16. ~
                    d'32
                    e'16. ~
                    e'32
                    fs'8.. ~
                    fs'4
                }

            Constraining the `maximum_dot_count` to `1`:

            ::

                >>> measure = parse(parseable)
                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     maximum_dot_count=1,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 3/4
                    c'32
                    d'16. ~
                    d'32
                    e'16. ~
                    e'32
                    fs'16. ~
                    fs'8 ~
                    fs'4
                }

            Constraining the `maximum_dot_count` to `0`:

            ::

                >>> measure = parse(parseable)
                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     maximum_dot_count=0,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 3/4
                    c'32
                    d'16 ~
                    d'32 ~
                    d'32
                    e'16 ~
                    e'32 ~
                    e'32
                    fs'16 ~
                    fs'32 ~
                    fs'8 ~
                    fs'4
                }

        ..  container:: example

            **Example 4.** Split logical ties at different depths of the
            `Meter`, if those logical ties cross any offsets at that
            depth, but do not also both begin and end at any of those offsets.

            Consider the default meter for `9/8`:

            ::

                >>> meter = metertools.Meter((9, 8))
                >>> print(meter.pretty_rtm_format)
                (9/8 (
                    (3/8 (
                        1/8
                        1/8
                        1/8))
                    (3/8 (
                        1/8
                        1/8
                        1/8))
                    (3/8 (
                        1/8
                        1/8
                        1/8))))

            We can establish that meter without specifying
            a `boundary_depth`:

            ::

                >>> parseable = "abj: | 9/8 c'2 d'2 e'8 |"
                >>> measure = parse(parseable)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 9/8
                    c'2
                    d'2
                    e'8
                }

            ::

                >>> mutate(measure[:]).rewrite_meter(measure)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 9/8
                    c'2
                    d'4 ~
                    d'4
                    e'8
                }

            With a `boundary_depth` of `1`, logical ties which cross any offsets
            created by nodes with a depth of `1` in this Meter's rhythm
            tree - i.e.  `0/8`, `3/8`, `6/8` and `9/8` - which do not also
            begin and end at any of those offsets, will be split:

            ::

                >>> measure = parse(parseable)
                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     boundary_depth=1,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 9/8
                    c'4. ~
                    c'8
                    d'4 ~
                    d'4
                    e'8
                }

            For this `9/8` meter, and this input notation, A `boundary_depth`
            of `2` causes no change, as all logical ties already align to
            multiples of `1/8`:

            ::

                >>> measure = parse(parseable)
                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     boundary_depth=2,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 9/8
                    c'2
                    d'4 ~
                    d'4
                    e'8
                }

        ..  container:: example

            **Example 5.** Comparison of `3/4` and `6/8`, at `boundary_depths`
            of 0 and 1:

            ::

                >>> triple = "abj: | 3/4 2 4 || 3/4 4 2 || 3/4 4. 4. |"
                >>> triple += "| 3/4 2 ~ 8 8 || 3/4 8 8 ~ 2 |"
                >>> duples = "abj: | 6/8 2 4 || 6/8 4 2 || 6/8 4. 4. |"
                >>> duples += "| 6/8 2 ~ 8 8 || 6/8 8 8 ~ 2 |"
                >>> score = Score([Staff(triple), Staff(duples)])

            In order to see the different time signatures on each staff,
            we need to move some engravers from the Score context to the
            Staff context:

            ::

                >>> engravers = [
                ...     'Timing_translator',
                ...     'Time_signature_engraver',
                ...     'Default_bar_line_engraver',
                ...     ]
                >>> score.remove_commands.extend(engravers)
                >>> score[0].consists_commands.extend(engravers)
                >>> score[1].consists_commands.extend(engravers)
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                } <<
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            c'4
                            c'2
                        }
                        {
                            c'4.
                            c'4.
                        }
                        {
                            c'2 ~
                            c'8
                            c'8
                        }
                        {
                            c'8
                            c'8 ~
                            c'2
                        }
                    }
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            c'4
                            c'2
                        }
                        {
                            c'4.
                            c'4.
                        }
                        {
                            c'2 ~
                            c'8
                            c'8
                        }
                        {
                            c'8
                            c'8 ~
                            c'2
                        }
                    }
                >>

            Here we establish a meter without specifying any boundary
            depth:

            ::

                >>> for measure in iterate(score).by_class(scoretools.Measure):
                ...     mutate(measure[:]).rewrite_meter(measure)
                ...
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                } <<
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            c'4
                            c'2
                        }
                        {
                            c'4.
                            c'4.
                        }
                        {
                            c'2 ~
                            c'8
                            c'8
                        }
                        {
                            c'8
                            c'8 ~
                            c'2
                        }
                    }
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            c'4
                            c'2
                        }
                        {
                            c'4.
                            c'4.
                        }
                        {
                            c'4. ~
                            c'4
                            c'8
                        }
                        {
                            c'8
                            c'4 ~
                            c'4.
                        }
                    }
                >>

            Here we re-establish meter at a boundary depth of `1`:

            ::

                >>> for measure in iterate(score).by_class(scoretools.Measure):
                ...     mutate(measure[:]).rewrite_meter(
                ...         measure,
                ...         boundary_depth=1,
                ...         )
                ...
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> print(format(score))
                \new Score \with {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                } <<
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            c'4
                            c'2
                        }
                        {
                            c'4 ~
                            c'8
                            c'8 ~
                            c'4
                        }
                        {
                            c'2 ~
                            c'8
                            c'8
                        }
                        {
                            c'8
                            c'8 ~
                            c'2
                        }
                    }
                    \new Staff \with {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    } {
                        {
                            \time 6/8
                            c'4. ~
                            c'8
                            c'4
                        }
                        {
                            c'4
                            c'8 ~
                            c'4.
                        }
                        {
                            c'4.
                            c'4.
                        }
                        {
                            c'4. ~
                            c'4
                            c'8
                        }
                        {
                            c'8
                            c'4 ~
                            c'4.
                        }
                    }
                >>

            Note that the two time signatures are much more clearly
            disambiguated above.

        ..  container:: example

            **Example 6.** Establishing meter recursively in measures
            with nested tuplets:

            ::

                >>> parseable = "abj: | 4/4 c'16 ~ c'4 d'8. ~ "
                >>> parseable += "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } "
                >>> parseable += "f'4 |"
                >>> measure = parse(parseable)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 4/4
                    c'16 ~
                    c'4
                    d'8. ~
                    \times 2/3 {
                        d'8. ~
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            d'16
                            e'8.
                            f'16 ~
                        }
                    }
                    f'4
                }

            When establishing a meter on a selection of components
            which contain containers, like `Tuplets` or `Containers`,
            `metertools.rewrite_meter()` will recurse into
            those containers, treating them as measures whose time
            signature is derived from the preprolated preprolated_duration
            of the container's contents:

            ::

                >>> mutate(measure[:]).rewrite_meter(
                ...     measure,
                ...     boundary_depth=1,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 4/4
                    c'4 ~
                    c'16
                    d'8. ~
                    \times 2/3 {
                        d'8 ~
                        d'16 ~
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            d'16
                            e'8 ~
                            e'16
                            f'16 ~
                        }
                    }
                    f'4
                }

        ..  container:: example

            **Example 7a.** Default rewrite behavior doesn't subdivide the
            first note in this measure because the first note in the measure
            starts at the beginning of a level-0 beat in meter:

            ::

                >>> measure = Measure((6, 8), "c'4.. c'16 ~ c'4")
                >>> meter = metertools.Meter((6, 8))
                >>> mutate(measure[:]).rewrite_meter(meter)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/8
                    c'4..
                    c'16 ~
                    c'4
                }

            **Example 7b.** Setting boundary depth to 1 subdivides the first
            note in this measure:

            ::

                >>> measure = Measure((6, 8), "c'4.. c'16 ~ c'4")
                >>> meter = metertools.Meter((6, 8))
                >>> mutate(measure[:]).rewrite_meter(meter, boundary_depth=1)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/8
                    c'4. ~
                    c'16
                    c'16 ~
                    c'4
                }

            **Example 7c.** Another way of doing this is by setting preferred
            boundary depth on the meter itself:

            ::

                >>> measure = Measure((6, 8), "c'4.. c'16 ~ c'4")
                >>> meter = metertools.Meter(
                ...     (6, 8),
                ...     preferred_boundary_depth=1,
                ...     )
                >>> mutate(measure[:]).rewrite_meter(meter)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/8
                    c'4. ~
                    c'16
                    c'16 ~
                    c'4
                }

            This makes it possible to divide different meters in different
            ways.

        ..  container:: example

            **Example 8.** Uses Messiaen-style ties:

            ::

                >>> measure = Measure((4, 4), "c'4. c'4. c'4")
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 4/4
                    c'4.
                    c'4.
                    c'4
                }

            ::

                >>> meter = metertools.Meter((4, 4))
                >>> mutate(measure[:]).rewrite_meter(
                ...     meter,
                ...     boundary_depth=1,
                ...     use_messiaen_style_ties=True,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 4/4
                    c'4
                    c'8 \repeatTie
                    c'8
                    c'4 \repeatTie
                    c'4
                }

        ..  container:: example

            **Example 9a.** Rewrites notes and tuplets:

            ::

                >>> measure = Measure((6, 4), [
                ...     Note("c'4."),
                ...     Tuplet((6, 7), "c'4. r16"),
                ...     Tuplet((6, 7), "r16 c'4."),
                ...     Note("c'4."),
                ...     ])
                >>> string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
                >>> string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
                >>> measure = Measure((6, 4), string)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/4
                    c'8 ~
                    c'8 ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8 ~
                    c'8 ~
                    c'8
                }

            ::

                >>> meter = metertools.Meter((6, 4))
                >>> mutate(measure[:]).rewrite_meter(
                ...     meter,
                ...     boundary_depth=1,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'8. ~
                        c'8 ~
                        c'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'8 ~
                        c'4
                    }
                    c'4.
                }

            The tied note rewriting is good while the tuplet rewriting
            could use some adjustment.

            **Example 9b.** Rewrites notes but not tuplets:

            ::

                >>> measure = Measure((6, 4), [
                ...     Note("c'4."),
                ...     Tuplet((6, 7), "c'4. r16"),
                ...     Tuplet((6, 7), "r16 c'4."),
                ...     Note("c'4."),
                ...     ])
                >>> string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
                >>> string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
                >>> measure = Measure((6, 4), string)
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/4
                    c'8 ~
                    c'8 ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8 ~
                    c'8 ~
                    c'8
                }

            ::

                >>> meter = metertools.Meter((6, 4))
                >>> mutate(measure[:]).rewrite_meter(
                ...     meter,
                ...     boundary_depth=1,
                ...     rewrite_tuplets=False,
                ...     )
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> print(format(measure))
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'4.
                }

        Operates in place and returns none.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools.metertools._rewrite_meter import _rewrite_meter
        selection = self._client
        if isinstance(selection, scoretools.Container):
            selection = selection[:]
        assert isinstance(selection, selectiontools.Selection)
        result = _rewrite_meter(
            selection,
            meter,
            boundary_depth=boundary_depth,
            initial_offset=initial_offset,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        return result

    def scale(self, multiplier):
        r'''Scales mutation client by `multiplier`.

        ..  container:: example

            **Example 1a.** Scale note duration by dot-generating multiplier:

            ::

                >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> mutate(staff[1]).scale(Multiplier(3, 2))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 (
                    d'8.
                    e'8
                    f'8 )
                }

        ..  container:: example

            **Example 1b.** Scale nontrivial logical tie
            by dot-generating `multiplier`:

            ::

                >>> staff = Staff(r"c'8 \accent ~ c'8 d'8")
                >>> time_signature = TimeSignature((3, 8))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/8
                    c'8 -\accent ~
                    c'8
                    d'8
                }

            ::

                >>> logical_tie = inspect_(staff[0]).get_logical_tie()
                >>> logical_tie = mutate(logical_tie).scale(Multiplier(3, 2))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 3/8
                    c'4. -\accent
                    d'8
                }

        ..  container:: example

            **Example 1c.** Scale container by dot-generating multiplier:

            ::

                >>> container = Container(r"c'8 ( d'8 e'8 f'8 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                }

            ::

                >>> mutate(container).scale(Multiplier(3, 2))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'8. (
                    d'8.
                    e'8.
                    f'8. )
                }

        ..  container:: example

            **Example 2a.** Scale note by tie-generating multiplier:

            ::

                >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> mutate(staff[1]).scale(Multiplier(5, 4))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 (
                    d'8 ~
                    d'32
                    e'8
                    f'8 )
                }

        ..  container:: example

            **Example 2b.** Scale nontrivial logical tie
            by tie-generating `multiplier`:

            ::

                >>> staff = Staff(r"c'8 \accent ~ c'8 d'16")
                >>> time_signature = TimeSignature((5, 16))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 5/16
                    c'8 -\accent ~
                    c'8
                    d'16
                }

            ::

                >>> logical_tie = inspect_(staff[0]).get_logical_tie()
                >>> logical_tie = mutate(logical_tie).scale(Multiplier(5, 4))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 5/16
                    c'4 -\accent ~
                    c'16
                    d'16
                }

        ..  container:: example

            **Example 2c.** Scale container by tie-generating multiplier:

            ::

                >>> container = Container(r"c'8 ( d'8 e'8 f'8 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                }

            ::

                >>> mutate(container).scale(Multiplier(5, 4))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'8 ~ (
                    c'32
                    d'8 ~
                    d'32
                    e'8 ~
                    e'32
                    f'8 ~
                    f'32 )
                }

        ..  container:: example

            **Example 3a.** Scale note by tuplet-generating multiplier:

            ::

                >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> mutate(staff[1]).scale(Multiplier(2, 3))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 (
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'8
                    }
                    e'8
                    f'8 )
                }

        ..  container:: example

            **Example 3b.** Scale trivial logical tie
            by tuplet-generating multiplier:

            ::

                >>> staff = Staff(r"c'8 \accent")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 -\accent
                }

            ::

                >>> logical_tie = inspect_(staff[0]).get_logical_tie()
                >>> logical_tie = mutate(logical_tie).scale(Multiplier(4, 3))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        c'4 -\accent
                    }
                }

        ..  container:: example

            **Example 3c.** Scale container by tuplet-generating multiplier:

            ::

                >>> container = Container(r"c'8 ( d'8 e'8 f'8 )")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                }

            ::

                >>> mutate(container).scale(Multiplier(4, 3))
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> print(format(container))
                {
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        c'4 (
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'4
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        e'4
                    }
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        f'4 )
                    }
                }

        ..  container:: example

            **Example 4.** Scale note by tie- and tuplet-generating
            multiplier:

            ::

                >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")
                >>> show(staff) # doctest: +SKIP

            ::

                >>> mutate(staff[1]).scale(Multiplier(5, 6))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    c'8 (
                    \tweak edge-height #'(0.7 . 0)
                    \times 2/3 {
                        d'8 ~
                        d'32
                    }
                    e'8
                    f'8 )
                }

        ..  container:: example

            **Example 5.** Scale note carrying LilyPond multiplier:

            ::

                >>> note = Note("c'8")
                >>> attach(Multiplier(1, 2), note)
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print(format(note))
                c'8 * 1/2

            ::

                >>> mutate(note).scale(Multiplier(5, 3))
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print(format(note))
                c'8 * 5/6

        ..  container:: example

            **Example 6.** Scale tuplet:

            ::

                >>> staff = Staff()
                >>> time_signature = TimeSignature((4, 8))
                >>> attach(time_signature, staff)
                >>> tuplet = scoretools.Tuplet((4, 5), [])
                >>> tuplet.extend("c'8 d'8 e'8 f'8 g'8")
                >>> staff.append(tuplet)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 4/8
                    \times 4/5 {
                        c'8
                        d'8
                        e'8
                        f'8
                        g'8
                    }
                }

            ::

                >>> mutate(tuplet).scale(Multiplier(2))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 4/8
                    \times 4/5 {
                        c'4
                        d'4
                        e'4
                        f'4
                        g'4
                    }
                }

        ..  container:: example

            **Example 7.** Scale fixed-duration tuplet:

            ::

                >>> staff = Staff()
                >>> time_signature = TimeSignature((4, 8))
                >>> attach(time_signature, staff)
                >>> tuplet = scoretools.FixedDurationTuplet((4, 8), [])
                >>> tuplet.extend("c'8 d'8 e'8 f'8 g'8")
                >>> staff.append(tuplet)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 4/8
                    \times 4/5 {
                        c'8
                        d'8
                        e'8
                        f'8
                        g'8
                    }
                }

            ::

                >>> mutate(tuplet).scale(Multiplier(2))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \time 4/8
                    \times 4/5 {
                        c'4
                        d'4
                        e'4
                        f'4
                        g'4
                    }
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if hasattr(self._client, '_scale'):
            self._client._scale(multiplier)
        else:
            assert isinstance(self._client, selectiontools.Selection)
            for component in self._client:
                component._scale(multiplier)

    def splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        r'''Splices `components` to the right or left of selection.

        ..  todo:: Add examples.

        Returns list of components.
        '''
        return self._client._splice(
            components,
            direction=direction,
            grow_spanners=grow_spanners,
            )

    # TODO: fix bug that unintentionally fractures ties.
    # TODO: add tests of tupletted notes and rests.
    # TODO: add examples that show indicator handling.
    # TODO: add example showing grace and after grace handling.
    def split(
        self,
        durations,
        fracture_spanners=False,
        cyclic=False,
        tie_split_notes=True,
        use_messiaen_style_ties=False,
        ):
        r'''Splits component or selection by `durations`.

        ..  container:: example

            **Example 1.** Split leaves:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff[:]
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, leaves)
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'16
                    e'16
                    d'8
                    f'32
                    f'16.
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

        ..  container:: example

            **Example 2.** Split leaves and fracture crossing spanners:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> leaves = staff[:]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     fracture_spanners=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 \f
                    e'16 \< \p
                    d'8
                    f'32 \f
                    f'16. \< \p
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

        ..  container:: example

            **Example 3.** Split leaves cyclically:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff[:]
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, leaves)
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     cyclic=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'16
                    e'16
                    d'8
                    f'32
                    f'16.
                    c'16.
                    c'32
                    e'8
                    d'16
                    d'16
                    f'8 \f
                }

        ..  container:: example

            **Example 4.** Split leaves cyclically and fracture spanners:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff[:]
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, leaves)
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     cyclic=True,
                ...     fracture_spanners=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 \f
                    e'16 \< \p
                    d'8
                    f'32 \f
                    f'16. \< \p
                    c'16. \f
                    c'32 \< \p
                    e'8
                    d'16 \f
                    d'16 \< \p
                    f'8 \f
                }

        ..  container:: example

            **Example 5.** Split tupletted leaves and fracture crossing
            spanners:

            ::

                >>> staff = Staff()
                >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
                >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> slur = spannertools.Slur()
                >>> attach(slur, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 2/3 {
                        c'4 (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4 )
                    }
                }

            ::

                >>> durations = [Duration(1, 4)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     fracture_spanners=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 2/3 {
                        c'4 (
                        d'8 )
                        d'8 (
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4 )
                    }
                }

        ..  container:: example

            **Example 6a.** Splits leaves cyclically and ties split notes:

            ::

                >>> staff = Staff("c'1 d'1")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
                >>> override(staff).dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'1 \< \p
                    d'1 \f
                }

            ::

                >>> durations = [Duration(3, 4)]
                >>> result = mutate(staff[:]).split(
                ...     durations,
                ...     cyclic=True,
                ...     fracture_spanners=False,
                ...     tie_split_notes=True,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'2. ~ \< \p
                    c'4
                    d'2 ~
                    d'2 \f
                }

            **Example 6b.** As above but with Messiaen-style ties:

            ::

                >>> staff = Staff("c'1 d'1")
                >>> hairpin = spannertools.Hairpin(descriptor='p < f')
                >>> attach(hairpin, staff[:])
                >>> override(staff).dynamic_line_spanner.staff_padding = 3

            ::

                >>> durations = [Duration(3, 4)]
                >>> result = mutate(staff[:]).split(
                ...     durations,
                ...     cyclic=True,
                ...     fracture_spanners=False,
                ...     tie_split_notes=True,
                ...     use_messiaen_style_ties=True,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff \with {
                    \override DynamicLineSpanner.staff-padding = #3
                } {
                    c'2. \< \p
                    c'4 \repeatTie
                    d'2
                    d'2 \repeatTie \f
                }

        Returns list of selections.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # check input
        components = self._client
        single_component_input = False
        if isinstance(components, scoretools.Component):
            single_component_input = True
            components = selectiontools.Selection(components)
        assert all(isinstance(x, scoretools.Component) for x in components)
        if not isinstance(components, selectiontools.Selection):
            components = selectiontools.Selection(components)
        durations = [durationtools.Duration(x) for x in durations]
        # return if no split to be done
        if not durations:
            if single_component_input:
                return components
            else:
                return [], components
        # calculate total component duration
        total_component_duration = components.get_duration()
        total_split_duration = sum(durations)
        # calculate durations
        if cyclic:
            durations = sequencetools.repeat_sequence_to_weight(
                durations, total_component_duration)
        elif total_split_duration < total_component_duration:
            final_offset = total_component_duration - sum(durations)
            durations.append(final_offset)
        elif total_component_duration < total_split_duration:
            durations = sequencetools.truncate_sequence(
                durations,
                weight=total_component_duration,
                )
        # keep copy of durations to partition result components
        durations_copy = durations[:]
        # calculate total split duration
        total_split_duration = sum(durations)
        assert total_split_duration == total_component_duration
        # initialize loop variables
        result, shard = [], []
        offset_index, offset_count = 0, len(durations)
        current_shard_duration = durationtools.Duration(0)
        remaining_components = list(components[:])
        advance_to_next_offset = True
        # loop and build shards by grabbing next component
        # and next duration each time through loop
        while True:
            # grab next split point
            if advance_to_next_offset:
                if durations:
                    next_split_point = durations.pop(0)
                else:
                    break
            advance_to_next_offset = True
            # grab next component from input stack of components
            if remaining_components:
                current_component = remaining_components.pop(0)
            else:
                break
            # find where current component endpoint will position us
            candidate_shard_duration = current_shard_duration + \
                current_component._get_duration()
            # if current component would fill current shard exactly
            if candidate_shard_duration == next_split_point:
                shard.append(current_component)
                result.append(shard)
                shard = []
                current_shard_duration = durationtools.Duration(0)
                offset_index += 1
            # if current component would exceed current shard
            elif next_split_point < candidate_shard_duration:
                local_split_duration = \
                    next_split_point - current_shard_duration
                if isinstance(current_component, scoretools.Leaf):
                    leaf_split_durations = [local_split_duration]
                    current_duration = current_component._get_duration()
                    additional_required_duration = \
                        current_duration - local_split_duration
                    split_durations = sequencetools.split_sequence(
                        durations,
                        [additional_required_duration],
                        cyclic=False,
                        overhang=True,
                        )
                    additional_durations = split_durations[0]
                    leaf_split_durations.extend(additional_durations)
                    durations = split_durations[-1]
                    leaf_shards = current_component._split(
                        leaf_split_durations,
                        cyclic=False,
                        fracture_spanners=fracture_spanners,
                        tie_split_notes=tie_split_notes,
                        use_messiaen_style_ties=use_messiaen_style_ties,
                        )
                    shard.extend(leaf_shards)
                    result.append(shard)
                    offset_index += len(additional_durations)
                else:
                    left_list, right_list = \
                        current_component._split_by_duration(
                        local_split_duration,
                        fracture_spanners=fracture_spanners,
                        tie_split_notes=tie_split_notes,
                        use_messiaen_style_ties=use_messiaen_style_ties,
                        )
                    shard.extend(left_list)
                    result.append(shard)
                    remaining_components.__setitem__(slice(0, 0), right_list)
                shard = []
                offset_index += 1
                current_shard_duration = durationtools.Duration(0)
            # if current component would not fill current shard
            elif candidate_shard_duration < next_split_point:
                shard.append(current_component)
                current_shard_duration += current_component._get_duration()
                advance_to_next_offset = False
            else:
                raise ValueError
        # append any stub shard
        if len(shard):
            result.append(shard)
        # append any unexamined components
        if len(remaining_components):
            result.append(remaining_components)
        # partition split components according to input durations
        result = sequencetools.flatten_sequence(result)
        result = selectiontools.Selection(result)
        result = result.partition_by_durations(durations_copy, fill=Exact)
        # return list of shards
        result = [selectiontools.Selection(x) for x in result]
        return result

    def swap(self, container):
        r'''Swaps mutation client for empty `container`.

        ..  container:: example

            **Example 1.** Swap measures for tuplet:

                >>> staff = Staff()
                >>> staff.append(Measure((3, 4), "c'4 d'4 e'4"))
                >>> staff.append(Measure((3, 4), "d'4 e'4 f'4"))
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(staff)
                >>> hairpin = spannertools.Hairpin('p < f')
                >>> attach(hairpin, leaves)
                >>> measures = staff[:]
                >>> slur = spannertools.Slur()
                >>> attach(slur, leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 3/4
                        c'4 \< \p (
                        d'4
                        e'4
                    }
                    {
                        d'4
                        e'4
                        f'4 \f )
                    }
                }

            ::

                >>> measures = staff[:]
                >>> tuplet = Tuplet(Multiplier(2, 3), [])
                >>> tuplet.preferred_denominator = 4
                >>> mutate(measures).swap(tuplet)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \times 4/6 {
                        c'4 \< \p (
                        d'4
                        e'4
                        d'4
                        e'4
                        f'4 \f )
                    }
                }

        Returns none.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection
        if isinstance(self._client, selectiontools.Selection):
            donors = self._client
        else:
            donors = selectiontools.Selection(self._client)
        assert donors._all_are_contiguous_components_in_same_parent(donors)
        assert isinstance(container, scoretools.Container)
        assert not container, repr(container)
        donors._give_music_to_empty_container(container)
        donors._give_dominant_spanners([container])
        donors._give_position_in_parent_to_container(container)

    def transpose(self, expr):
        r'''Transposes notes and chords in mutation client by `expr`.

        ..  container:: example

            **Example 1.** Transposes notes and chords in staff:

            ::

                >>> staff = Staff()
                >>> staff.append(Measure((4, 4), "c'4 d'4 e'4 r4"))
                >>> staff.append(Measure((3, 4), "d'4 e'4 <f' a' c''>4"))
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                    >>> print(format(staff))
                    \new Staff {
                        {
                            \time 4/4
                            c'4
                            d'4
                            e'4
                            r4
                        }
                        {
                            \time 3/4
                            d'4
                            e'4
                            <f' a' c''>4
                        }
                    }

            ::

                >>> mutate(staff).transpose("+m3")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    {
                        \time 4/4
                        ef'4
                        f'4
                        g'4
                        r4
                    }
                    {
                        \time 3/4
                        f'4
                        g'4
                        <af' c'' ef''>4
                    }
                }

        Returns none.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        named_interval = pitchtools.NamedInterval(expr)
        for x in iterate(self._client).by_class(
            (scoretools.Note, scoretools.Chord)):
            if isinstance(x, scoretools.Note):
                old_written_pitch = x.note_head.written_pitch
                new_written_pitch = old_written_pitch.transpose(named_interval)
                x.note_head.written_pitch = new_written_pitch
            else:
                for note_head in x.note_heads:
                    old_written_pitch = note_head.written_pitch
                    new_written_pitch = old_written_pitch.transpose(
                        named_interval)
                    note_head.written_pitch = new_written_pitch

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'''Returns client of mutation agent.

        Returns selection or component.
        '''
        return self._client
