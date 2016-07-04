# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class WellformednessManager(AbjadObject):
    r'''Wellformedness manager.

    ..  container:: example

        **Example.**

        ::

            >>> systemtools.WellformednessManager()
            WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    ### SPECIAL METHODS ###

    def __call__(self, expr=None):
        r'''Calls all wellformedness checks on `expr`.

        Returns triples.
        '''
        if expr is None:
            return
        check_names = [x for x in dir(self) if x.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(expr=expr)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PUBLIC METHODS ###

    @staticmethod
    def check_beamed_quarter_notes(expr=None):
        r'''Checks to make sure there are no beamed quarter notes.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        smart_beams = (
            spannertools.DuratedComplexBeam,
            spannertools.MultipartBeam,
            )
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            total += 1
            parentage = leaf._get_parentage(include_self=True)
            beams = parentage._get_spanners(spannertools.Beam)
            for beam in beams:
                if not isinstance(beam, smart_beams):
                    flag_count = leaf.written_duration.flag_count
                    if flag_count < 1:
                        violators.append(leaf)
                        break
        return violators, total

    @staticmethod
    def check_conflicting_clefs(expr=None):
        r'''Checks for conflicting clefs.

        Conflicting clefs defined equal to the situation in which a first clef
        is attached to a container and a second clef is attached to a child of
        the container that starts at the same time as the container.

        Situation does not usually arise because an exception raises on attempt
        to attach a clef to any component that starts at the same time as some
        other component in the score tree.

        But advanced users can stumble into this situation as described in
        the following examples.

        ..  container:: example

            **Example 1.** Conflicting clefs result from attaching clefs to
            separate containers and then appending one container to the other:

            ::

                >>> staff = Staff()
                >>> attach(Clef('bass'), staff)
                >>> voice = Voice()
                >>> attach(Clef('treble'), voice)
                >>> staff.append(voice)

            ::

                >>> f(staff)
                \new Staff {
                    \clef "bass"
                    \new Voice {
                        \clef "treble"
                    }
                }

            ::

                >>> inspect_(staff).is_well_formed()
                False

            This is bad.

        ..  container:: example

            **Example 2.** Conflicting clefs result from attaching clefs to
            free-standing leaves, then to a container and then extending the
            cleffed-container with the cleffed-leaves:

            ::

                >>> staff = Staff()
                >>> attach(Clef('bass'), staff)
                >>> leaves = scoretools.make_leaves([0, 2, 4, 5], [(1, 4)])
                >>> attach(Clef('treble'), leaves[0])
                >>> staff.extend(leaves)

            ::

                >>> f(staff)
                \new Staff {
                    \clef "bass"
                    \clef "treble"
                    c'4
                    d'4
                    e'4
                    f'4
                }

            ::

                >>> inspect_(staff).is_well_formed()
                False

            This is also bad.

        ..  todo:: Raise an exception on append or extend to prohibit these
            cases.

        Returns violators and total.
        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import inspect_
        from abjad.tools.topleveltools import iterate
        violators = []
        containers = iterate(expr).by_class(scoretools.Container)
        total_containers = 0
        for container in containers:
            total_containers += 1
            if not inspect_(container).has_indicator(indicatortools.Clef):
                continue
            current_component = container
            while (isinstance(current_component, scoretools.Container) and
                0 < len(current_component)):
                first_child = current_component[0]
                if inspect_(first_child).has_indicator(indicatortools.Clef):
                    violators.append(container)
                    break
                current_component = first_child
        return violators, total_containers

    @staticmethod
    def check_discontiguous_spanners(expr=None):
        r'''Checks for discontiguous spanners.

        There are now two different types of spanner.
        Most spanners demand that spanner components be
        logical-voice-contiguous. But a few special spanners (like Tempo)
        do not make such a demand. The check here consults the experimental
        `_contiguity_constraint`.

        Returns violators and total.
        '''
        from abjad.tools.selectiontools import Selection
        violators = []
        total = 0
        for spanner in expr._get_descendants()._get_spanners():
            if spanner._contiguity_constraint == 'logical voice':
                if not Selection._all_are_contiguous_components_in_same_logical_voice(
                    spanner[:]):
                    violators.append(spanner)
            total += 1
        return violators, total

    @staticmethod
    def check_duplicate_ids(expr=None):
        r'''Checks to make sure there are no components with duplicated IDs.

        Returns violators and total.
        '''
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import iterate
        violators = []
        components = iterate(expr).by_class()
        total_ids = [id(x) for x in components]
        unique_ids = sequencetools.remove_repeated_elements(total_ids)
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([x for x in components
                        if id(x) == current_id])
        return violators, len(total_ids)

    @staticmethod
    def check_empty_containers(expr=None):
        r'''Checks to make sure there are no empty containers in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        bad, total = 0, 0
        for component in iterate(expr).by_class(scoretools.Container):
            if len(component) == 0:
                violators.append(component)
                bad += 1
            total += 1
        return violators, total

    @staticmethod
    def check_intermarked_hairpins(expr=None):
        r'''Checks to make sure there are no hairpins in score with intervening
        dynamic marks.

        Returns violators and total.
        '''
        from abjad.tools import indicatortools
        from abjad.tools import spannertools
        violators = []
        total, bad = 0, 0
        prototype = (spannertools.Hairpin,)
        hairpins = expr._get_descendants()._get_spanners(prototype)
        for hairpin in hairpins:
            if 2 < len(hairpin._get_leaves()):
                for leaf in hairpin._get_leaves()[1:-1]:
                    if leaf._get_indicators(indicatortools.Dynamic):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total

    @staticmethod
    def check_misdurated_measures(expr=None):
        r'''Checks to make sure there are no misdurated measures in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total, bad = 0, 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            time_signature = measure.time_signature
            if time_signature is not None:
                if measure._preprolated_duration != time_signature.duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total

    @staticmethod
    def check_misfilled_measures(expr=None):
        r'''Checks that time signature duration equals measure contents
        duration for every measure.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total, bad = 0, 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total

    @staticmethod
    def check_mismatched_enchained_hairpins(expr=None):
        r'''Checks mismatched enchained hairpins.

        ..  container:: example

            **Example 1.** Checks mismatched enchained hairpins:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> attach(Hairpin('p < f'), staff[:2])
                >>> attach(Hairpin('p > pp'), staff[1:])

            ::

                >>> print(inspect_(staff).tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	2 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                2 /	2 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	2 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /	2 short hairpins
                0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        all_hairpins = set()
        prototype = spannertools.Hairpin
        for leaf in iterate(expr).by_leaf():
            hairpins = leaf._get_spanners(prototype)
            hairpins = list(hairpins)
            all_hairpins.update(hairpins)
            if len(hairpins) <= 1:
                continue
            if 2 < len(hairpins):
                raise Exception('too many hairpins')
            assert len(hairpins) == 2
            hairpins_are_enchained = False
            if (hairpins[0]._is_my_last_leaf(leaf) and 
                hairpins[-1]._is_my_first_leaf(leaf)):
                hairpins_are_enchained = True
            if (hairpins[-1]._is_my_last_leaf(leaf) and 
                hairpins[0]._is_my_first_leaf(leaf)):
                hairpins_are_enchained = True
            if not hairpins_are_enchained:
                continue
            if hairpins[0]._is_my_first_leaf(leaf):
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
        total = len(all_hairpins)
        return violators, total

    @staticmethod
    def check_mispitched_ties(expr=None):
        r'''Checks for mispitched notes.

        ..  container:: example

            **Example 1.** Checks for mispitched ties attached to notes:

            ::

                >>> staff = Staff("c'4 ~ c'")
                >>> staff[1].written_pitch = NamedPitch("d'")

            ::

                >>> inspector = inspect_(staff)
                >>> print(inspector.tabulate_well_formedness_violations())
                0 /	2 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	1 discontiguous spanners
                0 /	3 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                1 /	1 mispitched ties
                0 /	2 misrepresented flags
                0 /	3 missing parents
                0 /	0 nested measures
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	1 overlapping ties
                0 /	0 short hairpins
                0 /	0 tied rests

        ..  container:: example

            **Example 2.** Checks for mispitched ties attached to chords:

            ::

                >>> staff = Staff("<c' d' bf'>4 ~ <c' d' bf'>")
                >>> staff[1].written_pitches = [6, 9, 10]

            ::

                >>> inspector = inspect_(staff)
                >>> print(inspector.tabulate_well_formedness_violations())
                0 /	2 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	1 discontiguous spanners
                0 /	3 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                1 /	1 mispitched ties
                0 /	2 misrepresented flags
                0 /	3 missing parents
                0 /	0 nested measures
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	1 overlapping ties
                0 /	0 short hairpins
                0 /	0 tied rests
        
        Does not check tied rests, chords or skips.

        Returns violator ties together with total number of ties.
        '''
        from abjad.tools import mathtools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = set()
        all_spanners = set()
        pitched_prototype = (scoretools.Note, scoretools.Chord)
        for leaf in iterate(expr).by_class(pitched_prototype):
            spanners = leaf._get_spanners(spannertools.Tie)
            if not spanners:
                continue
            all_spanners.update(spanners)
            spanner = spanners.pop()
            written_pitches = []
            for leaf in spanner:
                if isinstance(leaf, scoretools.Note):
                    written_pitches.append(leaf.written_pitch)
                elif isinstance(leaf, scoretools.Chord):
                    written_pitches.append(leaf.written_pitches)
                else:
                    raise TypeError(leaf)
            if not mathtools.all_are_equal(written_pitches):
                violators.add(spanner)
        violators = list(violators)
        total = len(all_spanners)
        return violators, total

    @staticmethod
    def check_misrepresented_flags(expr=None):
        r'''Checks to make sure there are no misrepresented flags in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        from abjad.tools.topleveltools import set_
        violators = []
        total = 0
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            total += 1
            flags = leaf.written_duration.flag_count
            left = getattr(set_(leaf), 'stem_left_beam_count', None)
            right = getattr(set_(leaf), 'stem_right_beam_count', None)
            if left is not None:
                if flags < left or \
                    (left < flags and right not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if flags < right or \
                    (right < flags and left not in (flags, None)):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, total

    @staticmethod
    def check_missing_parents(expr=None):
        r'''Checks to make sure there are no components in score with missing
        parent.

        Returns violators and total.
        '''
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        components = iterate(expr).by_class()
        for i, component in enumerate(components):
            if 0 < i:
                if component._parent is None:
                    violators.append(component)
        total = i + 1
        return violators, total

    @staticmethod
    def check_nested_measures(expr=None):
        r'''Checks to make sure there are no nested measures in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            parentage = measure._get_parentage(include_self=False)
            if parentage.get_first(scoretools.Measure):
                violators.append(measure)
            total += 1
        return violators, total

    @staticmethod
    def check_overlapping_beams(expr=None):
        r'''Checks to make sure there are no overlapping beams in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.Beam,)
        all_beams = set()
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            beams = leaf._get_spanners(prototype)
            all_beams.update(beams)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        total = len(all_beams)
        return violators, total

    @staticmethod
    def check_overlapping_glissandi(expr=None):
        r'''Checks to make sure there are no overlapping glissandi in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.Glissando,)
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            glissandi = leaf._get_spanners(prototype)
            glissandi = list(glissandi)
            if 1 < len(glissandi):
                if len(glissandi) == 2:
                    common_leaves = set(glissandi[0]._get_leaves())
                    common_leaves &= set(glissandi[1]._get_leaves())
                    if len(common_leaves) == 1:
                        x = list(common_leaves)[0]
                        if (
                            (glissandi[0]._is_my_first_leaf(x) and
                            glissandi[1]._is_my_last_leaf(x))
                            or
                            (glissandi[1]._is_my_first_leaf(x) and
                            glissandi[0]._is_my_last_leaf(x))
                            ):
                            break
                for glissando in glissandi:
                    if glissando not in violators:
                        violators.append(glissando)
        total = expr._get_descendants()._get_spanners(prototype)
        total = len(total)
        return violators, total

    @staticmethod
    def check_overlapping_hairpins(expr=None):
        r'''Checks to make sure there are no overlapping hairpins in score.

        ..  container:: example

            **Example 1.** Checks overlapping hairpins:

            ::

                >>> staff = Staff("c'4 d' e' f'")
                >>> attach(Crescendo(), staff[:])
                >>> attach(Decrescendo(), staff[:])

            ::

                >>> print(inspect_(staff).tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	2 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	2 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                2 /	2 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /	2 short hairpins
                0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = spannertools.Hairpin
        for leaf in iterate(expr).by_leaf():
            hairpins = leaf._get_spanners(prototype)
            hairpins = list(hairpins)
            if 1 < len(hairpins):
                if len(hairpins) == 2:
                    common_leaves = set(hairpins[0]._get_leaves())
                    common_leaves &= set(hairpins[1]._get_leaves())
                    if len(common_leaves) == 1:
                        x = list(common_leaves)[0]
                        if (
                            (hairpins[0]._is_my_first_leaf(x) and
                            hairpins[1]._is_my_last_leaf(x))
                            or
                            (hairpins[1]._is_my_first_leaf(x) and
                            hairpins[0]._is_my_last_leaf(x))
                            ):
                            break
                for hairpin in hairpins:
                    if hairpin not in violators:
                        violators.append(hairpin)
        total = expr._get_descendants()._get_spanners(prototype)
        total = len(total)
        return violators, total

    @staticmethod
    def check_overlapping_octavation_spanners(expr=None):
        r'''Checks to make sure there are no overlapping octavation spanners in
        score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.OctavationSpanner, )
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            spanners = leaf._get_descendants()._get_spanners(prototype)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        total = expr._get_descendants()._get_spanners(prototype)
        return violators, len(total)

    @staticmethod
    def check_overlapping_ties(expr=None):
        r'''Checks to make sure there are no overlapping ties in score.

        ..  container:: example

            **Example 1.** Checks overlapping ties:

            ::

                >>> staff = Staff("c'4 c' c' c''")
                >>> attach(Tie(), staff[:2])
                >>> attach(Tie(), staff[1:3])

            ::

                >>> print(inspect_(staff).tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	1 conflicting clefs
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	2 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                2 /	2 overlapping ties
                0 /	0 short hairpins
                0 /	0 tied rests

        Returns violators and count of total ties.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        total = set()
        violators = set()
        for leaf in iterate(expr).by_leaf():
            spanners = leaf._get_spanners(spannertools.Tie)
            total.update(spanners)
            if 1 < len(spanners):
                violators.update(spanners)
        return violators, len(total)

    @staticmethod
    def check_short_hairpins(expr=None):
        r'''Checks to make sure that hairpins span at least two leaves.

        Returns violators and total.
        '''
        from abjad.tools import spannertools
        violators = []
        total = 0
        prototype = (spannertools.Hairpin,)
        hairpins = expr._get_descendants()._get_spanners(prototype)
        for hairpin in hairpins:
            if len(hairpin._get_leaves()) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total

    @staticmethod
    def check_tied_rests(expr=None):
        r'''Checks to make sure there are no tied rests.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import inspect_
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        for rest in iterate(expr).by_class(scoretools.Rest):
            if inspect_(rest).has_spanner(spannertools.Tie):
                violators.append(rest)
            total += 1
        return violators, total