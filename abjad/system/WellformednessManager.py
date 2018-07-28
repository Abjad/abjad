from abjad.system.AbjadObject import AbjadObject


class WellformednessManager(AbjadObject):
    """
    Wellformedness manager.

    ..  container:: example

        >>> abjad.WellformednessManager()
        WellformednessManager()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    __slots__ = (
        '_allow_percussion_clef',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, allow_percussion_clef=None):
        self._allow_percussion_clef = allow_percussion_clef

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls all wellformedness checks on ``argument``.

        Returns triples.
        """
        if argument is None:
            return
        check_names = [_ for _ in dir(self) if _.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(argument=argument)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PRIVATE METHODS ###

    def _check_overlapping_spanners(self, argument, prototype=None):
        import abjad
        violators, spanners = set(), set()
        for leaf in abjad.iterate(argument).leaves():
            spanners_ = list(abjad.inspect(leaf).spanners(prototype))
            spanners.update(spanners_)
            if 1 < len(spanners_):
                if len(spanners_) == 2:
                    common_leaves = set(spanners_[0].leaves)
                    common_leaves &= set(spanners_[1].leaves)
                    if len(common_leaves) == 1:
                        leaf = list(common_leaves)[0]
                        if ((spanners_[0].leaves[0] is leaf and
                            spanners_[1].leaves[-1] is leaf) or
                            (spanners_[1].leaves[0] is leaf and
                            spanners_[0].leaves[-1] is leaf)):
                            break
                violators.update(spanners_)
        return violators, len(spanners)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_percussion_clef(self):
        """
        Is true when manager allows percussion clef.

        Returns true, false or none.
        """
        return self._allow_percussion_clef

    ### PUBLIC METHODS ###

    def check_discontiguous_spanners(self, argument=None):
        """
        Checks discontiguous spanners.

        There are now two different types of spanner. Most spanners demand that
        spanner components be logical-voice-contiguous. But a few special
        spanners (like MetronomeMark) do not make such a demand. The check here
        consults the experimental `_contiguity_constraint`.

        Returns list of discontiguous spanners and nonnegative integer count of
        all spanners in ``argument``.
        """
        import abjad
        violators = []
        descendants = abjad.inspect(argument).descendants()
        spanners = abjad.inspect(descendants).spanners()
        for spanner in spanners:
            if spanner._contiguity_constraint == 'logical voice':
                if not spanner[:].are_contiguous_logical_voice():
                    violators.append(spanner)
        return violators, len(spanners)

    def check_duplicate_ids(self, argument=None):
        """
        Checks duplicate IDs.

        Returns violators and total.
        """
        import abjad
        violators = []
        components = abjad.iterate(argument).components()
        total_ids = [id(_) for _ in components]
        unique_ids = abjad.sequence(total_ids).remove_repeats()
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([_ for _ in components
                        if id(_) == current_id])
        return violators, len(total_ids)

    def check_empty_containers(self, argument=None):
        r"""
        Checks empty containers.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> staff.append(abjad.Container())

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                {
                }
            }

            >>> manager = abjad.WellformednessManager()
            >>> violators, total = manager.check_empty_containers(staff)
            >>> violators
            [Container()]

        Returns list of empty containers and count of all containers in
        ``argument``.
        """
        import abjad
        violators, containers = [], set()
        for container in abjad.iterate(argument).components(abjad.Container):
            containers.add(container)
            if len(container) == 0:
                violators.append(container)
        return violators, len(containers)

    def check_misdurated_measures(self, argument=None):
        """
        Checks misdurated measures.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for measure in abjad.iterate(argument).components(abjad.Measure):
            total.add(measure)
            time_signature = measure.time_signature
            if time_signature is not None:
                duration = measure._get_preprolated_duration()
                if duration != time_signature.duration:
                    violators.append(measure)
        return violators, len(total)

    def check_misfilled_measures(self, argument=None):
        """
        Checks misfilled measures.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for measure in abjad.iterate(argument).components(abjad.Measure):
            total.add(measure)
            if measure.is_misfilled:
                violators.append(measure)
        return violators, len(total)

    def check_mismatched_enchained_hairpins(self, argument=None):
        r"""
        Checks mismatched enchained hairpins.

        ..  container:: example

            Checks mismatched enchained hairpins:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Hairpin('p < f'), staff[:2])
            >>> abjad.attach(abjad.Hairpin('p > pp'), staff[1:])

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	2 discontiguous spanners
            0 /	5 duplicate ids
            0 / 1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            2 /	2 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 / 4 notes on wrong clef
            0 / 4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	2 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners 
            0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves():
            hairpins = abjad.inspect(leaf).spanners(abjad.Hairpin)
            hairpins = list(hairpins)
            total.update(hairpins)
            if len(hairpins) <= 1:
                continue
            if 2 < len(hairpins):
                raise Exception('too many hairpins')
            assert len(hairpins) == 2
            hairpins_are_enchained = False
            if leaf is hairpins[0][-1] and leaf is hairpins[-1][0]:
                hairpins_are_enchained = True
            if leaf is hairpins[-1][-1] and leaf is hairpins[0][0]:
                hairpins_are_enchained = True
            if not hairpins_are_enchained:
                continue
            if leaf is hairpins[0][0]:
                first_hairpin = hairpins[-1]
                second_hairpin = hairpins[0]
            else:
                first_hairpin = hairpins[0]
                second_hairpin = hairpins[-1]
            if first_hairpin.stop_dynamic == second_hairpin.start_dynamic:
                continue
            else:
                violators.append(first_hairpin)
                violators.append(second_hairpin)
        return violators, len(total)

    def check_mispitched_ties(self, argument=None):
        r"""
        Checks mispitched notes.

        ..  container:: example

            Checks for mispitched ties attached to notes:

            >>> staff = abjad.Staff("c'4 ~ c'")
            >>> staff[1].written_pitch = abjad.NamedPitch("d'")

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	1 discontiguous spanners
            0 /	3 duplicate ids
            0 / 1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            1 /	1 mispitched ties
            0 /	2 misrepresented flags
            0 /	3 missing parents
            0 /	0 nested measures
            0 / 2 notes on wrong clef
            0 / 2 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	1 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        ..  container:: example

            Checks for mispitched ties attached to chords:

            >>> staff = abjad.Staff("<c' d' bf'>4 ~ <c' d' bf'>")
            >>> staff[1].written_pitches = [6, 9]

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	1 discontiguous spanners
            0 /	3 duplicate ids
            0 / 1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            1 /	1 mispitched ties
            0 /	2 misrepresented flags
            0 /	3 missing parents
            0 /	0 nested measures
            0 / 2 notes on wrong clef
            0 / 2 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	1 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        Returns violator ties together with total number of ties.
        """
        import abjad
        violators, ties = [], set()
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            ties_ = abjad.inspect(leaf).spanners(abjad.Tie)
            ties.update(ties_)
        for tie in ties:
            for first_leaf, second_leaf in abjad.sequence(tie).nwise():
                first_pitches = abjad.inspect(first_leaf).pitches()
                first_pitches = set([_.number for _ in first_pitches])
                second_pitches = abjad.inspect(second_leaf).pitches()
                second_pitches = set([_.number for _ in second_pitches])
                if not (first_pitches & second_pitches):
                    violators.append(tie)
                    break
        return violators, len(ties)

    def check_misrepresented_flags(self, argument=None):
        """
        Checks misrepresented flags.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves():
            total.add(leaf)
            flags = leaf.written_duration.flag_count
            left = getattr(abjad.setting(leaf), 'stem_left_beam_count', None)
            right = getattr(abjad.setting(leaf), 'stem_right_beam_count', None)
            if left is not None:
                if (flags < left or
                    (left < flags and right not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if (flags < right or
                    (right < flags and left not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, len(total)

    def check_missing_parents(self, argument=None):
        """
        Checks missing parents.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        components = abjad.iterate(argument).components()
        for i, component in enumerate(components):
            total.add(component)
            if 0 < i:
                if abjad.inspect(component).parentage().parent is None:
                    violators.append(component)
        return violators, len(total)

    def check_nested_measures(self, argument=None):
        """
        Checks nested measures.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for measure in abjad.iterate(argument).components(abjad.Measure):
            total.add(measure)
            parentage = abjad.inspect(measure).parentage(
                include_self=False,
                )
            if parentage.get_first(abjad.Measure):
                violators.append(measure)
        return violators, len(total)

    def check_notes_on_wrong_clef(self, argument=None):
        r"""
        Checks notes and chords on wrong clef.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef('alto')
            >>> abjad.attach(clef, staff[0])
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            4 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        ..  container:: example

            Allows percussion clef:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> clef = abjad.Clef('percussion')
            >>> abjad.attach(clef, staff[0])
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \clef "percussion"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness(
            ...     allow_percussion_clef=True,
            ...     ))
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        ..  container:: example

            Forbids percussion clef:

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness(
            ...     allow_percussion_clef=False,
            ...     ))
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            4 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        Returns true or false.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves():
            total.add(leaf)
            instrument = abjad.inspect(leaf).effective(abjad.Instrument)
            if instrument is None:
                continue
            clef = abjad.inspect(leaf).effective(abjad.Clef)
            if clef is None:
                continue
            allowable_clefs = [
                abjad.Clef(_) for _ in instrument.allowable_clefs
                ]
            if self.allow_percussion_clef:
                allowable_clefs.append(abjad.Clef('percussion'))
            if clef not in allowable_clefs:
                violators.append(leaf)
        return violators, len(total)

    def check_out_of_range_notes(self, argument=None):
        r"""
        Checks out-of-range notes.

        ..  container:: example

            Out of range:

            >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
            >>> violin = abjad.Violin()
            >>> abjad.attach(violin, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	0 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            1 /	2 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	2 tied rests

        Returns true or false.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            total.add(leaf)
            instrument = abjad.inspect(leaf).effective(abjad.Instrument)
            if instrument is None:
                continue
            if leaf not in instrument.pitch_range:
                violators.append(leaf)
        return violators, len(total)

    def check_overlapping_beams(self, argument=None):
        r"""
        Checks overlapping beams.

        ..  container:: example

            Overlapping beams are well-formed:

            >>> staff = abjad.Staff("c'8 d' e' f'")
            >>> abjad.attach(abjad.Beam(), staff[:3])
            >>> abjad.attach(abjad.Beam(), staff[2:])

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                ]
                [
                f'8
                ]
            }

            >>> manager = abjad.WellformednessManager()
            >>> violators, total = manager.check_overlapping_beams(staff)
            >>> for beam in sorted(violators):
            ...     beam
            ...
            Beam("c'8, d'8, e'8", durations=(), span_beam_count=1)
            Beam("e'8, f'8", durations=(), span_beam_count=1)

            (Enchained beams are not well-formed either.)

        Returns list of overlapping beams and nonnegative integer count of
        total beams in score.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves():
            beams = abjad.inspect(leaf).spanners(abjad.Beam)
            total.update(beams)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        return violators, len(total)

    def check_overlapping_glissandi(self, argument=None):
        """
        Checks overlapping glissandi.

        Returns violators and total.
        """
        import abjad
        return self._check_overlapping_spanners(argument, abjad.Glissando)

    def check_overlapping_hairpins(self, argument=None):
        r"""
        Checks overlapping hairpins.

        ..  container:: example

            Checks overlapping hairpins:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Hairpin('<'), staff[:])
            >>> abjad.attach(abjad.Hairpin('>'), staff[:])

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	2 discontiguous spanners
            0 /	5 duplicate ids
            0 / 1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	2 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            2 /	2 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        """
        import abjad
        return self._check_overlapping_spanners(argument, abjad.Hairpin)

    def check_overlapping_octavation_spanners(self, argument=None):
        """
        Checks overlapping octavation spanners.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        prototype = abjad.OctavationSpanner
        for leaf in abjad.iterate(argument).leaves():
            spanners = abjad.inspect(leaf).spanners(prototype)
            total.update(spanners)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        return violators, len(total)

    def check_overlapping_ties(self, argument=None):
        r"""
        Checks overlapping ties.

        ..  container:: example

            Checks overlapping ties:

            >>> staff = abjad.Staff("c'4 c' c' c''")
            >>> abjad.attach(abjad.Tie(), staff[:2])
            >>> tie = abjad.Tie()
            >>> tie._ignore_attachment_test = True
            >>> tie._ignore_before_attach = True
            >>> abjad.attach(tie, staff[1:3])

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	2 discontiguous spanners
            0 /	5 duplicate ids
            0 / 1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 2 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            2 /	2 overlapping ties
            0 / 0 overlapping trill spanners
            0 /	0 tied rests

        Returns violators and count of total ties.
        """
        import abjad
        violators, total = [], set()
        for leaf in abjad.iterate(argument).leaves():
            spanners = abjad.inspect(leaf).spanners(abjad.Tie)
            total.update(spanners)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        return violators, len(total)

    def check_overlapping_trill_spanners(self, argument=None):
        r"""
        Checks overlapping trill spanners.

        ..  container:: example

            Enchained trill spanners are ok:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.TrillSpanner(), staff[:3])
            >>> abjad.attach(abjad.TrillSpanner(), staff[2:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \startTrillSpan
                    d'4
                    e'4
                    \stopTrillSpan
                    \startTrillSpan
                    f'4
                    \stopTrillSpan
                }

            >>> abjad.inspect(staff).is_well_formed()
            True

        ..  container:: example

            Overlapping trill spanners are not well-formed:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.TrillSpanner(), staff[:])
            >>> abjad.attach(abjad.TrillSpanner(), staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \startTrillSpan
                    \startTrillSpan
                    d'4
                    e'4
                    f'4
                    \stopTrillSpan
                    \stopTrillSpan
                }

            >>> agent = abjad.inspect(staff)
            >>> print(agent.tabulate_wellformedness())
            0 /	2 discontiguous spanners
            0 /	5 duplicate ids
            0 /	1 empty containers
            0 /	0 misdurated measures
            0 /	0 misfilled measures
            0 /	0 mismatched enchained hairpins
            0 / 0 mispitched ties
            0 /	4 misrepresented flags
            0 /	5 missing parents
            0 /	0 nested measures
            0 /	4 notes on wrong clef
            0 /	4 out of range notes
            0 /	0 overlapping beams
            0 /	0 overlapping glissandi
            0 /	0 overlapping hairpins
            0 /	0 overlapping octavation spanners
            0 /	0 overlapping ties
            2 /	2 overlapping trill spanners
            0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        """
        import abjad
        return self._check_overlapping_spanners(argument, abjad.TrillSpanner)

    def check_tied_rests(self, argument=None):
        """
        Checks tied rests.

        Returns violators and total.
        """
        import abjad
        violators, total = [], set()
        for rest in abjad.iterate(argument).leaves(abjad.Rest):
            total.add(rest)
            if abjad.inspect(rest).has_spanner(abjad.Tie):
                violators.append(rest)
        return violators, len(total)
