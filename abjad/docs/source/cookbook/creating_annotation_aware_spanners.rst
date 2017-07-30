Creating annotation-aware spanners
==================================

..  abjad::

    import abjad

Key points:

#. Investigate the internals of Abjad's ``Spanner`` class.
#. Create a simple annotative indicator.
#. Build up a complex class, then refactor it.
#. Learn about Abjad's ``LilyPondGrobOverride`` and ``Enumeration`` classes.
#. Use rhythm-makers and selectors to help audition the custom spanner.

..  abjad::
    :hide:
    :reveal-label: OscillationSpanner
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        class Size(abjad.Enumeration):
            NONE = 0
            SMALL = 1
            MEDIUM = 2
            LARGE = 3

        def _apply_annotation_overrides(self, leaf, lilypond_format_bundle):
            annotation = self._get_annotation(leaf)
            zigzag_width = int(annotation)
            if zigzag_width:
                zigzag_width_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    is_once=True,
                    property_path='zigzag-width',
                    value=zigzag_width,
                    )
                override_string = zigzag_width_override.override_string
            else:
                zigzag_off_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    is_once=True,
                    property_path='style',
                    value=abjad.SchemeSymbol('line'),
                    )
                override_string = zigzag_off_override.override_string
            lilypond_format_bundle.grob_overrides.append(override_string)

        def _apply_spanner_start_overrides(self, lilypond_format_bundle):
            grob_override = abjad.LilyPondGrobOverride(
                grob_name='Glissando',
                property_path='style',
                value=abjad.SchemeSymbol('zigzag'),
                )
            override_string = grob_override.override_string
            lilypond_format_bundle.grob_overrides.append(override_string)

        def _apply_spanner_stop_overrides(self, lilypond_format_bundle):
            grob_override = abjad.LilyPondGrobOverride(
                grob_name='Glissando',
                property_path='style',
                )
            revert_string = grob_override.revert_string
            lilypond_format_bundle.grob_reverts.append(revert_string)

        def _get_annotation(self, leaf):
            annotations = abjad.inspect(leaf).get_indicators(self.Size)
            if not annotations:
                annotations = [self.Size.SMALL]
            return annotations[0]

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            if self._is_my_only_leaf(leaf):
                return lilypond_format_bundle
            if self._is_my_first_leaf(leaf):
                self._apply_spanner_start_overrides(lilypond_format_bundle)
            if self._is_my_last_leaf(leaf):
                self._apply_spanner_stop_overrides(lilypond_format_bundle)
                return lilypond_format_bundle
            prototype = (abjad.Chord, abjad.Note)
            next_leaf = abjad.inspect(leaf).get_leaf(1)
            if isinstance(leaf, prototype) and isinstance(next_leaf, prototype):
                lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
                self._apply_annotation_overrides(leaf, lilypond_format_bundle)
            return lilypond_format_bundle

..  abjad::
    :hide:

    def make_annotated_staff():
        staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
        abjad.attach(OscillationSpanner.Size.LARGE, staff[0])
        abjad.attach(OscillationSpanner.Size.MEDIUM, staff[1])
        abjad.attach(OscillationSpanner.Size.SMALL, staff[2])
        abjad.attach(OscillationSpanner.Size.NONE, staff[5])
        abjad.attach(OscillationSpanner.Size.LARGE, staff[6])
        return staff

..  abjad::
    :hide:

    staff = make_annotated_staff()
    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])
    show(staff)

Basic glissando functionality
-----------------------------

..  abjad::

    staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
    show(staff)

..  abjad::

    f(staff)

..  abjad::
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            return lilypond_format_bundle

..  abjad::

    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])
    show(staff)

..  abjad::

    f(staff)

Avoiding orphan and final leaves
--------------------------------

..  abjad::

    for leaf in staff:
        is_first = spanner._is_my_first_leaf(leaf)
        is_last = spanner._is_my_last_leaf(leaf)
        print(repr(leaf), is_first, is_last)

..  abjad::
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            if self._is_my_last_leaf(leaf) or self._is_my_only_leaf(leaf):
                return lilypond_format_bundle
            lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            return lilypond_format_bundle

..  abjad::

    staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])

..  abjad::

    show(staff)

..  abjad::

    f(staff)

Avoiding silences
-----------------

..  abjad::
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            if self._is_my_last_leaf(leaf) or self._is_my_only_leaf(leaf):
                return lilypond_format_bundle
            prototype = (abjad.Chord, abjad.Note)
            next_leaf = abjad.inspect(leaf).get_leaf(1)
            if isinstance(leaf, prototype) and isinstance(next_leaf, prototype):
                lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            return lilypond_format_bundle

..  abjad::

    staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])

..  abjad::

    show(staff)

..  abjad::

    f(staff)

Making object-oriented typographic overrides
--------------------------------------------

..  abjad::

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.override(staff[1]).note_head.style = 'cross'
    show(staff)
    f(staff)

..  abjad::

    grob_override = abjad.LilyPondGrobOverride(
        grob_name='NoteHead',
        is_once=True,
        property_path='style',
        value=abjad.SchemeSymbol('cross'),
        )
    abjad.attach(grob_override, staff[2])
    show(staff)
    f(staff)

..  abjad::

    zigzag_override = abjad.LilyPondGrobOverride(
        grob_name='Glissando',
        property_path='style',
        value=abjad.SchemeSymbol('zigzag'),
        )
    zigzag_override.override_string
    zigzag_override.revert_string

Integrating overrides during formatting
---------------------------------------

..  abjad::
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            if self._is_my_only_leaf(leaf):
                return lilypond_format_bundle
            if self._is_my_first_leaf(leaf):
                grob_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    property_path='style',
                    value=abjad.SchemeSymbol('zigzag'),
                    )
                override_string = grob_override.override_string
                lilypond_format_bundle.grob_overrides.append(override_string)
            if self._is_my_last_leaf(leaf):
                grob_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    property_path='style',
                    )
                revert_string = grob_override.revert_string
                lilypond_format_bundle.grob_reverts.append(revert_string)
                return lilypond_format_bundle
            prototype = (abjad.Chord, abjad.Note)
            next_leaf = abjad.inspect(leaf).get_leaf(1)
            if isinstance(leaf, prototype) and isinstance(next_leaf, prototype):
                lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            return lilypond_format_bundle

..  abjad::

    staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])
    show(staff)

..  abjad::

    f(staff)

A simple non-formatting annotation class
----------------------------------------

..  abjad::
    :strip-prompt:

    class OscillationSize(abjad.Enumeration):
        NONE = 0
        SMALL = 1
        MEDIUM = 2
        LARGE = 3

..  abjad::
    :strip-prompt:

    def make_annotated_staff():
        staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")
        abjad.attach(OscillationSize.LARGE, staff[0])
        abjad.attach(OscillationSize.MEDIUM, staff[1])
        abjad.attach(OscillationSize.SMALL, staff[2])
        abjad.attach(OscillationSize.NONE, staff[5])
        abjad.attach(OscillationSize.MEDIUM, staff[6])
        return staff

..  abjad::

    staff = make_annotated_staff()
    show(staff)

..  abjad::

    f(staff)

Making the spanner annotation-aware
-----------------------------------

..  abjad::
    :strip-prompt:

    class OscillationSpanner(abjad.Spanner):

        def _get_lilypond_format_bundle(self, leaf):
            lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
            if self._is_my_only_leaf(leaf):
                return lilypond_format_bundle
            if self._is_my_first_leaf(leaf):
                grob_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    property_path='style',
                    value=abjad.SchemeSymbol('zigzag'),
                    )
                override_string = grob_override.override_string
                lilypond_format_bundle.grob_overrides.append(override_string)
            if self._is_my_last_leaf(leaf):
                grob_override = abjad.LilyPondGrobOverride(
                    grob_name='Glissando',
                    property_path='style',
                    )
                revert_string = grob_override.revert_string
                lilypond_format_bundle.grob_reverts.append(revert_string)
                return lilypond_format_bundle
            prototype = (abjad.Chord, abjad.Note)
            next_leaf = abjad.inspect(leaf).get_leaf(1)
            if isinstance(leaf, prototype) and isinstance(next_leaf, prototype):
                lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
                annotations = abjad.inspect(leaf).get_indicators(OscillationSize)
                if not annotations:
                    annotations = [OscillationSize.SMALL]
                annotation = annotations[0]
                zigzag_width = int(annotation)
                if zigzag_width:
                    zigzag_width_override = abjad.LilyPondGrobOverride(
                        grob_name='Glissando',
                        is_once=True,
                        property_path='zigzag-width',
                        value=zigzag_width,
                        )
                    override_string = zigzag_width_override.override_string
                else:
                    zigzag_off_override = abjad.LilyPondGrobOverride(
                        grob_name='Glissando',
                        is_once=True,
                        property_path='style',
                        value=abjad.SchemeSymbol('line'),
                        )
                    override_string = zigzag_off_override.override_string
                lilypond_format_bundle.grob_overrides.append(override_string)
            return lilypond_format_bundle

..  abjad::

    staff = make_annotated_staff()
    spanner = OscillationSpanner()
    abjad.attach(spanner, staff[:])
    show(staff)

..  abjad::

    f(staff)

Refactoring the custom spanner class
------------------------------------

..  reveal:: OscillationSpanner

Preparing for deployment
------------------------

..  abjad::

    staff = abjad.Staff("g'4. d''8 b'2 b'8 r8 f''4. d'8. f'16 r8")

..  abjad::

    selector = abjad.Selector().by_leaf().by_run(abjad.Note)[:-1].flatten()

..  abjad::

    selector = abjad.Selector()
    for x in selector(staff):
        x

..  abjad::

    selector = selector.by_leaf()
    for x in selector(staff):
        x

..  abjad::

    selector = selector.by_run(Note)
    for x in selector(staff):
        x

..  abjad::

    selector = selector[:-1]
    for x in selector(staff):
        x

..  abjad::

    selector = selector.flatten()
    for x in selector(staff):
        x

..  abjad::

    annotations = abjad.CyclicTuple([
        OscillationSpanner.Size.LARGE,
        OscillationSpanner.Size.MEDIUM,
        OscillationSpanner.Size.SMALL,
        OscillationSpanner.Size.NONE,
        ])

..  abjad::

    annotations[0]
    annotations[23]
    annotations[973]

..  abjad::

    abjad.attach(OscillationSpanner(), staff)
    for i, leaf in enumerate(selector(staff)):
        abjad.attach(annotations[i], leaf)

    show(staff)

Deploying the spanner
---------------------

..  abjad::

    talea_rhythm_maker = rhythmmakertools.TaleaRhythmMaker(
        burnish_specifier=rhythmmakertools.BurnishSpecifier(
            left_classes=[abjad.Rest],
            left_counts=[0, 1],
            right_classes=[abjad.Rest],
            right_counts=[0, 0, 1],
            ),
        extra_counts_per_division=[1, 0, 0],
        talea=rhythmmakertools.Talea(
            counts=[2, 3, 1, 3, 1, 4, 2, 2],
            denominator=8,
            ),
        tie_split_notes=False,
        )

..  abjad::

    divisions = [(5, 8), (7, 8), (4, 8), (6, 8), (5, 4), (4, 4), (3, 4)]
    selections = talea_rhythm_maker(divisions)
    measures = abjad.Measure.from_selections(selections, time_signatures=divisions)
    staff = abjad.Staff(measures)
    show(staff)

All of the notes' pitches are middle-C, so we'll apply some pitches cyclically
to each logical tie:

..  abjad::

    pitches = abjad.CyclicTuple(
        ["b'", "d''", "g'", "f''", "b'", "g'", "c'", "e'", "g'"],
        )
    for i, logical_tie in enumerate(iterate(staff).by_logical_tie(pitched=True)):
        for note in logical_tie:
            note.written_pitch = pitches[i]

Now we apply the ``OscillationSpanner`` and the cyclic sequence of
``OscillationSpanner.Size`` annotations:

..  abjad::

    abjad.attach(OscillationSpanner(), staff)
    for i, leaf in enumerate(selector(staff)):
        abjad.attach(annotations[i], leaf)

The result?

..  abjad::

    show(staff)

Now that we know the ingredients required, we can package the entire
staff-creation process into a function and run it with different variations,
via rotation:

..  abjad::
    :strip-prompt:

    def make_fancy_staff(rotation=0):
        annotations = abjad.CyclicTuple(sequence([
            OscillationSpanner.Size.LARGE,
            OscillationSpanner.Size.MEDIUM,
            OscillationSpanner.Size.SMALL,
            OscillationSpanner.Size.NONE,
            ]).rotate(rotation))
        divisions = [(5, 8), (7, 8), (4, 8), (6, 8), (5, 4), (4, 4), (3, 4)]
        divisions = abjad.sequence(divisions).rotate(rotation)
        pitches = abjad.CyclicTuple(sequence(
            ["b'", "d''", "g'", "f''", "b'", "g'", "c'", "e'", "g'"],
            ).rotate(rotation))
        selections = talea_rhythm_maker(divisions, rotation=rotation)
        measures = abjad.Measure.from_selections(selections, time_signatures=divisions)
        staff = abjad.Staff(measures)
        for i, logical_tie in enumerate(iterate(staff).by_logical_tie(pitched=True)):
            for note in logical_tie:
                note.written_pitch = pitches[i]
        selector = abjad.Selector().by_leaf().by_run(abjad.Note)[:-1].flatten()
        for i, leaf in enumerate(selector(staff)):
            abjad.attach(annotations[i], leaf)
        abjad.attach(OscillationSpanner(), staff)
        return staff

..  abjad::

    staff = make_fancy_staff(rotation=2)
    show(staff)
    staff = make_fancy_staff(rotation=5)
    show(staff)
