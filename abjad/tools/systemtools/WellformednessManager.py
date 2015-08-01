# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class WellformednessManager(AbjadObject):
    r'''Wellformedness manager.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    ### INITIALIZER ###

    def __init__(self, expr=None, allow_empty_containers=True):
        self.expr = expr
        self.allow_empty_containers = allow_empty_containers

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls all wellformedness checks on `expr`.

        Returns something.
        '''
        if self.expr is None:
            return
        check_names = [x for x in dir(self) if x.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            if self.allow_empty_containers:
                if current_check_name == 'check_empty_containers':
                    continue
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check()
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PUBLIC METHODS ###

    def check_beamed_quarter_notes(self):
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
        for leaf in iterate(self.expr).by_class(scoretools.Leaf):
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

    def check_conflicting_clefs(self):
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
        containers = iterate(self.expr).by_class(scoretools.Container)
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

    def check_discontiguous_spanners(self):
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
        for spanner in self.expr._get_descendants()._get_spanners():
            if spanner._contiguity_constraint == 'logical voice':
                if not Selection._all_are_contiguous_components_in_same_logical_voice(
                    spanner[:]):
                    violators.append(spanner)
            total += 1
        return violators, total

    def check_duplicate_ids(self):
        r'''Checks to make sure there are no components with duplicated IDs.

        Returns violators and total.
        '''
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import iterate
        violators = []
        components = iterate(self.expr).by_class()
        total_ids = [id(x) for x in components]
        unique_ids = sequencetools.remove_repeated_elements(total_ids)
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([x for x in components
                        if id(x) == current_id])
        return violators, len(total_ids)

    def check_empty_containers(self):
        r'''Checks to make sure there are no empty containers in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        bad, total = 0, 0
        for component in iterate(self.expr).by_class(scoretools.Container):
            if len(component) == 0:
                violators.append(component)
                bad += 1
            total += 1
        return violators, total

    def check_intermarked_hairpins(self):
        r'''Checks to make sure there are no hairpins in score with intervening
        dynamic marks.

        Returns violators and total.
        '''
        from abjad.tools import indicatortools
        from abjad.tools import spannertools
        violators = []
        total, bad = 0, 0
        prototype = (spannertools.Hairpin,)
        hairpins = self.expr._get_descendants()._get_spanners(prototype)
        for hairpin in hairpins:
            if 2 < len(hairpin._get_leaves()):
                for leaf in hairpin._get_leaves()[1:-1]:
                    if leaf._get_indicators(indicatortools.Dynamic):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total

    def check_misdurated_measures(self):
        r'''Checks to make sure there are no misdurated measures in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total, bad = 0, 0
        for measure in iterate(self.expr).by_class(scoretools.Measure):
            time_signature = measure.time_signature
            if time_signature is not None:
                if measure._preprolated_duration != time_signature.duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total

    def check_misfilled_measures(self):
        r'''Checks that time signature duration equals measure contents
        duration for every measure.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total, bad = 0, 0
        for measure in iterate(self.expr).by_class(scoretools.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total

    def check_mispitched_ties(self):
        r'''Checks for mispitched notes. Does not check tied rests or skips.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        prototype = (spannertools.Tie,)
        for leaf in iterate(self.expr).by_class(scoretools.Note):
            total += 1
            spanners = leaf._get_spanners(prototype)
            if spanners:
                spanner = spanners.pop()
                if not spanner._is_my_last_leaf(leaf):
                    next_leaf = leaf._get_leaf(1)
                    if next_leaf:
                        if leaf.written_pitch != next_leaf.written_pitch:
                            violators.append(leaf)
        return violators, total

    def check_misrepresented_flags(self):
        r'''Checks to make sure there are no misrepresented flags in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        from abjad.tools.topleveltools import set_
        violators = []
        total = 0
        for leaf in iterate(self.expr).by_class(scoretools.Leaf):
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

    def check_missing_parents(self):
        r'''Checks to make sure there are no components in score with missing
        parent.

        Returns violators and total.
        '''
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        components = iterate(self.expr).by_class()
        for i, component in enumerate(components):
            if 0 < i:
                if component._parent is None:
                    violators.append(component)
        total = i + 1
        return violators, total

    def check_nested_measures(self):
        r'''Checks to make sure there are no nested measures in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        violators = []
        total = 0
        for measure in iterate(self.expr).by_class(scoretools.Measure):
            parentage = measure._get_parentage(include_self=False)
            if parentage.get_first(scoretools.Measure):
                violators.append(measure)
            total += 1
        return violators, total

    def check_overlapping_beams(self):
        r'''Checks to make sure there are no overlapping beams in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.Beam,)
        all_beams = set()
        for leaf in iterate(self.expr).by_class(scoretools.Leaf):
            beams = leaf._get_spanners(prototype)
            all_beams.update(beams)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        total = len(all_beams)
        return violators, total

    def check_overlapping_glissandi(self):
        r'''Checks to make sure there are no overlapping glissandi in score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.Glissando,)
        for leaf in iterate(self.expr).by_class(scoretools.Leaf):
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
        total = self.expr._get_descendants()._get_spanners(prototype)
        total = len(total)
        return violators, total

    def check_overlapping_octavation_spanners(self):
        r'''Checks to make sure there are no overlapping octavation spanners in
        score.

        Returns violators and total.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import iterate
        violators = []
        prototype = (spannertools.OctavationSpanner, )
        for leaf in iterate(self.expr).by_class(scoretools.Leaf):
            spanners = leaf._get_descendants()._get_spanners(prototype)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        total = self.expr._get_descendants()._get_spanners(prototype)
        return violators, len(total)

    def check_short_hairpins(self):
        r'''Checks to make sure that hairpins span at least two leaves.

        Returns violators and total.
        '''
        from abjad.tools import spannertools
        violators = []
        total = 0
        prototype = (spannertools.Hairpin,)
        hairpins = self.expr._get_descendants()._get_spanners(prototype)
        for hairpin in hairpins:
            if len(hairpin._get_leaves()) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total