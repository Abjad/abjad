Changes
=======

..

----

Changed in Abjad 3.6
--------------------

Changes to Abjad 3.6 (2022-03-01) since Abjad 3.5 (2022-02-01).

PERFORMANCE INCREASES. Abjad 3.6 runs significantly faster than previous versions of the
system: user code rendering two or more pages of music runs 200% to 800% than before.
Performance increases came from removing inspect-heavy functions, and from optimizing
score updates. Total performance increase depends on the number of context indicators
(like clefs and time signatures) used, and on the amount of looping used to find
indicators in a score.

BREAKING CHANGE: `#1407 <https://github.com/Abjad/abjad/issues/1407>`_. The custom
``abjad.Selection`` class is deprecated will be completely removed in Abjad 3.7.

    CHANGED. In general, remove all ``isinstance(..., abjad.Selection)`` from your code:
    Abjad 3.6 now passes built-in lists of components instead of custom selection
    objects. Container slices now return a list:

    OLD::

        staff = abjad.Staff("c'4 d' e' f'")[:]
        abjad.Selection(items=[Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

    NEW::

        staff = abjad.Staff("c'4 d' e' f'")[:]
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

    CHANGED. ``abjad.select.foo(...)`` and ``abjad.iterate.foo(...)`` now match.

    Selecting components means calling functions; class creation is no longer required:

    OLD::

        abjad.select(...).chord(n)
        abjad.select(...).chords()
        abjad.select(...).components()
        abjad.select(...).exclude([0], 2)
        abjad.select(...).filter(lambda _: len(_) == 2)
        abjad.select(...).get([0], 2)
        abjad.select(...).group_by(lambda _: getattr(_, "foo"))
        abjad.select(...).group_by_contiguity()
        abjad.select(...).group_by_duration()
        abjad.select(...).group_by_length()
        abjad.select(...).group_by_measure()
        abjad.select(...).group_by_pitch()
        abjad.select(...).leaf(n)
        abjad.select(...).leaves()
        abjad.select(...).logical_tie(n)
        abjad.select(...).logical_ties()
        abjad.select(...).nontrivial()
        abjad.select(...).note(n)
        abjad.select(...).notes()
        abjad.select(...).partition_by_counts([4, 4, 2], cyclic=True)
        abjad.select(...).partition_by_ratio((2, 1))
        abjad.select(...).rest(n)
        abjad.select(...).rests()
        abjad.select(...).run(n)
        abjad.select(...).runs()
        abjad.select(...).top()
        abjad.select(...).tuplet(n)
        abjad.select(...).tuplets()
        abjad.select(...).with_next_leaf()
        abjad.select(...).with_previous_leaf()

    NEW::

        abjad.select.chord(..., n)
        abjad.select.chords(..., )
        abjad.select.components(..., )
        abjad.select.exclude(..., [0], 2)
        abjad.select.filter(..., lambda _: len(_) == 2)
        abjad.select.get(..., [0], 2)
        abjad.select.group_by(..., lambda _: getattr(_, "foo"))
        abjad.select.group_by_contiguity(..., )
        abjad.select.group_by_duration(..., )
        abjad.select.group_by_length(..., )
        abjad.select.group_by_measure(..., )
        abjad.select.group_by_pitch(..., )
        abjad.select.leaf(..., n)
        abjad.select.leaves(..., )
        abjad.select.logical_tie(..., n)
        abjad.select.logical_ties(..., )
        abjad.select.nontrivial(..., )
        abjad.select.note(..., n)
        abjad.select.notes(..., )
        abjad.select.partition_by_counts(..., [4, 4, 2], cyclic=True)
        abjad.select.partition_by_ratio(..., (2, 1))
        abjad.select.rest(..., n)
        abjad.select.rests(..., )
        abjad.select.run(..., n)
        abjad.select.runs(..., )
        abjad.select.top(..., )
        abjad.select.tuplet(..., n)
        abjad.select.tuplets(..., )
        abjad.select.with_next_leaf(..., )
        abjad.select.with_previous_leaf(..., )

    Dot-chained syntax continues to be allowed in Abjad 3.6 but will be removed in Abjad
    3.7. Rewrite dot-chained method calls like this:

    Example 1::

        OLD:

            result = abjad.select(...).tuplets()[:4].leaves()

        NEW:

            result = abjad.select.tuplets(...)[:4]
            result = abjad.select.leaves(result)

    Example 2::

        OLD:

            result = abjad.select(...).leaves().group_by_measure().get([0], 2)

        NEW:

            result = abjad.select.leaves(...)
            result = abjad.select.group_by_measure(result)
            result = abjad.select.get(result, [0], 2)

BREAKING CHANGE: `#1415 <https://github.com/Abjad/abjad/issues/1415>`_. Replaced
``abjad.Sequence`` with ``sequence.py`` module:

    OLD::

        abjad.Sequence(...).filter()
        abjad.Sequence(...).flatten()
        abjad.Sequence(...).group_by()
        abjad.Sequence(...).is_decreasing()
        abjad.Sequence(...).is_increasing()
        abjad.Sequence(...).is_permutation()
        abjad.Sequence(...).is_repetition_free()
        abjad.Sequence(...).join()
        abjad.Sequence(...).map()
        abjad.Sequence(...).nwise()
        abjad.Sequence(...).partition_by_counts()
        abjad.Sequence(...).partition_by_ratio_of_lengths()
        abjad.Sequence(...).partition_by_ratio_of_weights()
        abjad.Sequence(...).partition_by_weights()
        abjad.Sequence(...).permute()
        abjad.Sequence(...).remove()
        abjad.Sequence(...).remove_repeats()
        abjad.Sequence(...).repeat()
        abjad.Sequence(...).repeat_to_length()
        abjad.Sequence(...).repeat_to_weight()
        abjad.Sequence(...).replace()
        abjad.Sequence(...).replace_at()
        abjad.Sequence(...).retain()
        abjad.Sequence(...).retain_pattern()
        abjad.Sequence(...).reverse()
        abjad.Sequence(...).rotate()
        abjad.Sequence(...).sort()
        abjad.Sequence(...).split()
        abjad.Sequence(...).sum()
        abjad.Sequence(...).sum_by_sign()
        abjad.Sequence(...).truncate()
        abjad.Sequence(...).weight()
        abjad.Sequence(...).zip()

    NEW::

        abjad.sequence.filter(...)
        abjad.sequence.flatten(...)
        abjad.sequence.group_by(...)
        abjad.sequence.is_decreasing(...)
        abjad.sequence.is_increasing(...)
        abjad.sequence.is_permutation(...)
        abjad.sequence.is_repetition_free(...)
        abjad.sequence.join(...)
        abjad.sequence.map(...)
        abjad.sequence.nwise(...)
        abjad.sequence.partition_by_counts(...)
        abjad.sequence.partition_by_ratio_of_lengths(...)
        abjad.sequence.partition_by_ratio_of_weights(...)
        abjad.sequence.partition_by_weights(...)
        abjad.sequence.permute(...)
        abjad.sequence.remove(...)
        abjad.sequence.remove_repeats(...)
        abjad.sequence.repeat(...)
        abjad.sequence.repeat_to_length(...)
        abjad.sequence.repeat_to_weight(...)
        abjad.sequence.replace(...)
        abjad.sequence.replace_at(...)
        abjad.sequence.retain(...)
        abjad.sequence.retain_pattern(...)
        abjad.sequence.reverse(...)
        abjad.sequence.rotate(...)
        abjad.sequence.sort(...)
        abjad.sequence.split(...)
        abjad.sequence.sum(...)
        abjad.sequence.sum_by_sign(...)
        abjad.sequence.truncate(...)
        abjad.sequence.weight(...)
        abjad.sequence.zip(...)

BREAKING CHANGE: `#1394 <https://github.com/Abjad/abjad/issues/1394>`_. Replaced
``abjad.String`` with ``string.py`` module:

    OLD::

        abjad.String("text").capitalize_start()
        abjad.String("text").delimit_words()
        abjad.String("text").from_roman()
        abjad.String("text").is_lilypond_identifier()
        abjad.String("text").is_roman()
        abjad.String("text").is_shout_case()
        abjad.String("text").pluralize()
        abjad.String("text").strip_roman()
        abjad.String("text").to_shout_case()
        abjad.String("text").to_upper_camel_case()
        abjad.String.normalize("text")
        abjad.String.sort_roman(["PartI", "PartII", "PartIII"])
        abjad.String.to_tridirectional_lilypond_symbol("text")
        abjad.String.to_tridirectional_ordinal_constant("text")

    NEW::

        abjad.string.capitalize_start("text")
        abjad.string.delimit_words("text")
        abjad.string.from_roman("text")
        abjad.string.is_lilypond_identifier("text")
        abjad.string.is_roman("text")
        abjad.string.is_shout_case("text")
        abjad.string.pluralize("text")
        abjad.string.strip_roman("text")
        abjad.string.to_shout_case("text")
        abjad.string.to_upper_camel_case("text")
        abjad.string.normalize("text")
        abjad.string.sort_roman(["PartI", "PartII", "PartIII"])
        abjad.string.to_tridirectional_lilypond_symbol("text")
        abjad.string.to_tridirectional_ordinal_constant("text")

    REMOVED::

        abjad.String("text").base_26()
        abjad.String("text").is_build_directory_name()
        abjad.String("text").is_classfile_name()
        abjad.String("text").is_dash_case()
        abjad.String("text").is_lower_camel_case()
        abjad.String("text").is_lowercase_file_name()
        abjad.String("text").is_module_file_name()
        abjad.String("text").is_package_name()
        abjad.String("text").is_public_python_file_name()
        abjad.String("text").is_rehearsal_mark()
        abjad.String("text").is_snake_case()
        abjad.String("text").is_snake_case_file_name()
        abjad.String("text").is_snake_case_file_name_with_extension()
        abjad.String("text").is_snake_case_package_name()
        abjad.String("text").is_space_delimited_lowercase()
        abjad.String("text").is_string()
        abjad.String("text").is_stylesheet_name()
        abjad.String("text").is_tools_file_name()
        abjad.String("text").is_upper_camel_case()
        abjad.String("text").match_strings()
        abjad.String("text").match_word_starts()
        abjad.String("text").remove_zfill()
        abjad.String("text").segment_letter()
        abjad.String("text").segment_rank()
        abjad.String("text").strip_diacritics()
        abjad.String("text").to_accent_free_snake_case()
        abjad.String("text").to_dash_case()
        abjad.String("text").to_lower_camel_case()
        abjad.String("text").to_segment_lilypond_identifier()
        abjad.String("text").to_snake_case()
        abjad.String("text").to_space_delimited_lowercase()
        abjad.String("text").to_space_delimited_lowercase()
        abjad.String.to_bidirectional_direction_string("text")
        abjad.String.to_bidirectional_lilypond_symbol("text")
        abjad.String.to_tridirectional_direction_string("text")


`#1420 <https://github.com/Abjad/abjad/issues/1420>`_. Cleaned up boolean keywords.

`#1418 <https://github.com/Abjad/abjad/issues/1418>`_. Constrained ``abjad.PitchRange``
to named pitches:

    OLD::

        abjad.PitchRange("[A0, C8]")
        abjad.PitchRange("[-39, 48]")
        "C3" in pitch_range
        -12 in pitch_range

    NEW::

        abjad.PitchRange("[A0, C8]")
        "C3" in pitch_range

`#1405 <https://github.com/Abjad/abjad/issues/1405>`_. Removed pitch vector classes.

`#1403 <https://github.com/Abjad/abjad/issues/1403>`_. Changed pitch collections'
``from_selection()`` to ``from_pitches()``:

    OLD::

        abjad.IntervalClassSegment.from_selection()
        abjad.IntervalSegment.from_selection()
        abjad.PitchClassSegment.from_selection()
        abjad.PitchSegment.from_selection()
        abjad.IntervalClassSet.from_selection()
        abjad.IntervalSet.from_selection()
        abjad.PitchClassSet.from_selection()
        abjad.PitchSet.from_selection()
        abjad.IntervalVector.from_selection()
        abjad.IntervalClassVector.from_selection()
        abjad.PitchClassVector.from_selection()
        abjad.PitchVector.from_selection()

    NEW::

        abjad.IntervalClassSegment.from_pitches()
        abjad.IntervalSegment.from_pitches()
        abjad.PitchClassSegment.from_pitches()
        abjad.PitchSegment.from_pitches()
        abjad.IntervalClassSet.from_pitches()
        abjad.IntervalSet.from_pitches()
        abjad.PitchClassSet.from_pitches()
        abjad.PitchSet.from_pitches()
        abjad.IntervalVector.from_pitches()
        abjad.IntervalClassVector.from_pitches()
        abjad.PitchClassVector.from_pitches()
        abjad.PitchVector.from_pitches()

    You must now call ``abjad.iterate.pitches()`` explicitly before calling
    ``from_pitches()``:

    OLD::

        abjad.PitchSegment.from_selection(staff[:])

    NEW::

        pitches = abjad.iterate.pitches(staff)
        abjad.PitchSegment.from_pitches(pitches)

`#1401 <https://github.com/Abjad/abjad/issues/1401>`_. Made
``abjad.NamedPitch.respell()`` public.

    NEW::

        abjad.NamedPitch("cs").respell(accidental="flats")
        NamedPitch('df')

        abjad.NamedPitch("df").respell(accidental="sharps")
        NamedPitch('cs')

`#1399 <https://github.com/Abjad/abjad/issues/1399>`_. Removed operator classes.

`#1397 <https://github.com/Abjad/abjad/issues/1397>`_. Removed inequality classes.

`#1392 <https://github.com/Abjad/abjad/issues/1392>`_. Remove ``abjad.SegmentMaker``.
Removed score templates.

`#1390 <https://github.com/Abjad/abjad/issues/1390>`_. Optimized score updates.


`#1388 <https://github.com/Abjad/abjad/issues/1388>`_. Removed
``abjad.format.get_repr()``, and related inspect-heavy functions:

    REMOVED::

        abjad.get.get_hash_values()
        abjad.format.get_repr()
        abjad.format.get_template_dict()
        abjad.format.storage()

`#1387 <https://github.com/Abjad/abjad/issues/1387>`_. Refused comparison between named
and numbered pitches.

`#1379 <https://github.com/Abjad/abjad/issues/1379>`_. Removed
``abjad.format.compare_objects()``.

----

Changed in Abjad 3.5
--------------------

Changes to Abjad 3.5 (2022-02-01) since Abjad 3.4 (2021-05-01).

Abjad 3.5 requires Python 3.10.

`#1384 <https://github.com/Abjad/abjad/issues/1384>`_. Moved ``abjad.ily`` from
``abjad/docs/_stylesheets`` to ``abjad/abjad/_stylesheets``.

`#1372 <https://github.com/Abjad/abjad/issues/1372>`_. Refactored all indicators as
dataclasses. Added new ``indicators.py`` module.

`#1370 <https://github.com/Abjad/abjad/issues/1370>`_. Fixed definition of Forte SC 4-25.

`#1368 <https://github.com/Abjad/abjad/issues/1368>`_. Gutted ``abjad.Markup``. Markup is
no longer parsed:

    OLD::

        abjad.Markup('\italic "Allegro moderato"', literal=True)

    NEW::

        abjad.Markup(r'\markup \italic "Allegro moderator"')

    REMOVED::

        * abjad.Postscript; use strings instead
        * abjad.PostscriptOperator; use strings instead
        * abjad.Markup.__add__(), __radd__()
        * abjad.Markup.postscript()
        * abjad.markups.abjad_metronome_mark()

`#1366 <https://github.com/Abjad/abjad/issues/1366>`_. Removed ``abjad.OrderedDict``. Use
``dict()`` instead.

`#1360 <https://github.com/Abjad/abjad/issues/1360>`_. Replaced
``abjad.StorageFormatManager`` with ``format.py`` module.

`#1359 <https://github.com/Abjad/abjad/issues/1359>`_. Changed ``abjad.iterate()`` to
``iterate.py`` module:

    OLD::

        abjad.iterate(argument).components()
        abjad.iterate(argument).leaves()
        abjad.iterate(argument).logical_ties()
        abjad.iterate(argument).pitches()

    NEW::

        abjad.iterate.components(argument)
        abjad.iterate.leaves(argument)
        abjad.iterate.logical_ties(argument)
        abjad.iterate.pitches(argument)

`#1357 <https://github.com/Abjad/abjad/issues/1357>`_. Changed ``abjad.Label`` to
``label.py`` module:

    OLD::

        abjad.Label(argument).by_selector()
        abjad.Label(argument).color_container()
        abjad.Label(argument).color_leaves()
        abjad.Label(argument).color_note_heads()
        abjad.Label(argument).remove_markup()
        abjad.Label(argument).vertical_moments()
        abjad.Label(argument).with_durations()
        abjad.Label(argument).with_indices()
        abjad.Label(argument).with_intervals()
        abjad.Label(argument).with_pitches()
        abjad.Label(argument).with_set_classes()
        abjad.Label(argument).with_start_offsets()

    NEW::

        abjad.label.by_selector(argument)
        abjad.label.color_container(argument)
        abjad.label.color_leaves(argument)
        abjad.label.color_note_heads(argument)
        abjad.label.remove_markup(argument)
        abjad.label.vertical_moments(argument)
        abjad.label.with_durations(argument)
        abjad.label.with_indices(argument)
        abjad.label.with_intervals(argument)
        abjad.label.with_pitches(argument)
        abjad.label.with_set_classes(argument)
        abjad.label.with_start_offsets(argument)

`#1303 <https://github.com/Abjad/abjad/issues/1303>`_. Removed default.ily stylesheet.

`#1293 <https://github.com/Abjad/abjad/issues/1293>`_. Gutted ``abjad.LilyPondFile``:

    Removed abjad.ContextBlock; use abjad.Block instead::

        string = r"""\Staff
            \name FluteStaff
            \type Engraver_group
            \alias Staff
            \remove Forbid_line_break_engraver
            \consists Horizontal_bracket_engraver
            \accepts FluteUpperVoice
            \accepts FluteLowerVoice
            \override Beam.positions = #'(-4 . -4)
            \override Stem.stem-end-position = -6
            autoBeaming = ##f
            tupletFullLength = ##t
            \accidentalStyle dodecaphonic"""
        block = abjad.Block(name="context")
        block.items.append(string)

        string = abjad.lilypond(block)
        print(string)
        \context
        {
            \Staff
            \name FluteStaff
            \type Engraver_group
            \alias Staff
            \remove Forbid_line_break_engraver
            \consists Horizontal_bracket_engraver
            \accepts FluteUpperVoice
            \accepts FluteLowerVoice
            \override Beam.positions = #'(-4 . -4)
            \override Stem.stem-end-position = -6
            autoBeaming = ##f
            tupletFullLength = ##t
            \accidentalStyle dodecaphonic
        }

    Removed ``abjad.Block.__setattr__()``. Use ``abjad.Block.items`` instead.

    REMOVED::

        * abjad.DateTimeToken
        * abjad.LilyPondDimension
        * abjad.LilyPondLanguageToken
        * abjad.LilyPondVersionToken
        * abjad.PackageGitCommitToken
        * abjad.LilyPondFile.comments
        * abjad.LilyPondFile.includes
        * abjad.LilyPondFile.use_relative_includes
        * Removed courtesy blank lines from abjad.LilyPondFile output
        * abjad.LilyPondFile.default_paper_size
        * abjad.LilyPondFile.global_staff_size:

    OLD::

        * abjad.LilyPondFile.default_paper_size = ("a4", "letter")
        * abjad.LilyPondFile.global_staff_size = 16

    NEW::

        preamble = r"""
            #(set-default-paper-size "a4" 'letter)
            #(set-global-staff-size 16)"""

        * abjad.LilyPondFile(items=[preamble, ...])

    OLD::

        * abjad.LilyPondFile.header_block
        * abjad.LilyPondFile.layout_block
        * abjad.LilyPondFile.paper_block

    NEW::

        * abjad.LilyPondFile["header"]
        * abjad.LilyPondFile["layout"]
        * abjad.LilyPondFile["paper"]

    Limited ``abjad.LilyPondFile.__getitem__()`` to strings:

    OLD::

        * lilypond_file["My_Staff"]
        * lilypond_file[abjad.Staff]

    NEW::

        * lilypond_file["My_Staff"]

`#1136 <https://github.com/Abjad/abjad/issues/1136>`_. Collapsed
``abjad.AnnotatedTimespan`` into ``abjad.Timespan``.

CONFIGURATION::

    * Removed abjad.AbjadConfiguration.composer_email
    * Removed abjad.AbjadConfiguration.composer_full_name
    * Removed abjad.AbjadConfiguration.composer_github_username
    * Removed abjad.AbjadConfiguration.composer_last_name
    * Removed abjad.AbjadConfiguration.composer_scores_directory
    * Removed abjad.AbjadConfiguration.composer_uppercase_name
    * Removed abjad.AbjadConfiguration.composer_website
    * Added abjad.AbjadConfiguration.sphinx_stylesheets_directory colon-delimited paths

ENUMERATION: `abjad.enumerate.yield_outer_product()`` previously returned a generator of
``abjad.Sequence`` objects. The function now returns a list of list.

I/O::

    * Taught abjad.persist.as_ly() to write file-terminal newline.
    * Cleaned up abjad.persist.as_midi().
    * Cleaned up abjad.run_lilypond():
        OLD: abjad.run_lilypond() returned true or false.
        NEW: abjad.run_lilypond() returns integer exit code.
    * Cleaned up abjad.io.profile():
        * removed print_to_terminal=True keyword
        * function now always returns a string

LABEL: Taught ``abjad.Label.color_note_heads()`` to color accidentals.

SELECTION: Changed ``abjad.select()`` to a true synonym for ``abjad.Selection()``.

Deprecated ``abjad.SegmentMaker``. Define scores as a linear sequence of function calls
instead.

Deprecated all score templates. Define ``make_empty_score()`` function instead.

Changed in Abjad 3.4
--------------------

Changes to Abjad 3.4 (2021-05-01) since Abjad 3.3 (2021-03-01).

Removed support for IPython.

`#1338 <https://github.com/Abjad/abjad/issues/1338>`_. Cleaned up tuplet formatting and
block formatting. Opening brace now appears on its own line in LilyPond output:

OLD:

    >>> tuplet = abjad.Tuplet("3:2", "c'4 d' e'")
    >>> string = abjad.lilypond(tuplet)
    >>> print(string)
    \times 2/3 {
        c'4
        d'4
        e'4
    }

    >>> staff = abjad.Staff("c'4 d' e' f'")
    >>> block = abjad.Block(name="score")
    >>> block.items.append(staff)
    >>> string = abjad.lilypond(block)
    >>> print(string)
    \score {
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
    }

NEW:

    >>> tuplet = abjad.Tuplet("3:2", "c'4 d' e'")
    >>> string = abjad.lilypond(tuplet)
    >>> print(string)
    \times 2/3
    {
        c'4
        d'4
        e'4
    }

    >>> staff = abjad.Staff("c'4 d' e' f'")
    >>> block = abjad.Block(name="score")
    >>> block.items.append(staff)
    >>> string = abjad.lilypond(block)
    >>> print(string)
    \score
    {
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
    }

`#1299 <https://github.com/Abjad/abjad/issues/1299>`_. Removed deprecated ``stravinsky``
keyword from pitch classes. The function of the keyword was to transpose sets and
segments such that the first element was set equal to 0 (after operations like inversion
or rotation). Transpose sets and segments separately (after inversion or rotation) when
required instead.

----

Changed in Abjad 3.3
--------------------

Changes to Abjad 3.3 (2021-03-01) since Abjad 3.2 (2021-01-19).

`#1328 <https://github.com/Abjad/abjad/issues/1328>`_. Removed ``abjad.WoodwindFingering``. Use LilyPond ``\woodwind-fingering`` instead.

`#1323 <https://github.com/Abjad/abjad/issues/1323>`_. Removed ``abjad.f()``. Use
``abjad.lilypond()`` instead:

::

    OLD:

        >>> abjad.f(score)

    NEW:

        >>> string = abjad.lilypond(score)
        >>> print(string)

`#1293 <https://github.com/Abjad/abjad/issues/1293>`_. Removed ``abjad.LilyPondFile.new()`` constructor. Use ``abjad.LilyPondFile`` initializer instead:

::

    OLD:

        >>> abjad.LilyPondFile.new(score)

    NEW:

        >>> block = abjad.Block(name="score")
        >>> block.items.append(score)
        >>> abjad.LilyPondFile(items=[block])

`#1086 <https://github.com/Abjad/abjad/issues/1086>`_. Gutted markup interface.
Externalize markup in a LilyPond stylesheet and set ``literal=True`` instead:

::

    REMOVED:

        abjad.Markup.bold()
        abjad.Markup.center_column()
        abjad.Markup.hcenter_in()
        abjad.Markup.italic()
        abjad.Markup.with_dimensions()
        ...

    OLD:

        >>> markup = abjad.Markup("Allegro assai")
        >>> markup = markup.bold()

    NEW:

        Create a markup library in an external LilyPond file;
        assign each new piece of markup to a LilyPond variable:

            allegro-assai = \markup \bold { Allegro assai }

        Then initialize in Abjad like this:

            >>> abjad.Markup(r"\allegro-assai", literal=True)

        Markup can still be initialized locally in Abjad;
        type markup exactly as in LilyPond:

        >>> string = r"\markup \bold { Allegro assai }"
        >>> abjad.Markup(string, literal=True)

(The ``literal=True`` keyword will be removed in a future release of Abjad. All markup
will then initialize as though ``literal=True``.)

`#1086 <https://github.com/Abjad/abjad/issues/1086>`_. Removed Scheme proxy classes. Type
Scheme settings as literal LilyPond code instead:

::

    REMOVED:

        abjad.SchemeMoment
        abjad.SchemeAssociativeList
        abjad.SchemeColor
        abjad.SchemePair
        abjad.SpacingVector
        abjad.SchemeSymbol
        abjad.SchemeVector
        abjad.SchemeVectorConstant

    CHANGED:

        >>> scheme_moment = abjad.SchemeMoment((1, 24))
        >>> abjad.override(score).proportional_notation_duration = scheme_moment

        >>> abjad.override(score).proportionalNotationDuration = "#(ly:make-moment 1 24)"

    CHANGED:

        >>> abjad.override(voice).note_head.color = abjad.SchemeColor("red")

        >>> abjad.override(voice).NoteHead.color = "#red"

    CHANGED:

        >>> abjad.override(voice).note_head.style = abjad.SchemeSymbol("harmonic")

        >>> abjad.override(voice).NoteHead.style = "#'harmonic"

    CHANGED:

        >>> spacing_vector = abjad.SpacingVector(0, 10, 10, 0)
        >>> abjad.override(score).staff_grouper.staff_staff_spacing = spacing_vector

        >>> string = "#'((basic-distance . 10) (minimum-distance . 10))
        >>> abjad.override(score).StaffGrouper.staff_staff_spacing = string

    CHANGED:

        >>> string = "tuplet-number::calc-denominator-text"
        >>> abjad.override(score).tuplet_number.text = string
    
        >>> string = "#tuplet-number::calc-denominator-text"
        >>> abjad.override(score).TupletNumber.text = string

----

Fixed in Abjad 3.3
------------------

`#1319 <https://github.com/Abjad/abjad/issues/1319>`_. Taught the auxilliary note in
pitched trills to transpose. (`Tsz Kiu Pang <https://nivlekp.github.io/>`_).

`#1309 <https://github.com/Abjad/abjad/issues/1309>`_. Taught
``abjad.Meter.rewrite_meter()`` more about handling grace notes. (`Tsz Kiu Pang
<https://nivlekp.github.io/>`_).

`#1129 <https://github.com/Abjad/abjad/issues/1129>`_. Taught tweaked note heads to
copy correctly. (`Tsz Kiu Pang <https://nivlekp.github.io/>`_).

`#1174 <https://github.com/Abjad/abjad/issues/1174>`_. Taught
``abjad.Selection.group_by_measure()`` to respect pick-measures created at the beginning
of a score with `abjad.TimeSignature.partial`. (`Tsz Kiu Pang
<https://nivlekp.github.io/>`_).

----

Changed in Abjad 3.2
--------------------

Changes to Abjad 3.2 (2021-01-19) since Abjad 3.1 (2019-12-19).

`#1244 <https://github.com/Abjad/abjad/issues/1244>`_. Taught tuplets to preserve input
ratios without reducing terms of fraction:

::

    NEW. Taught abjad.Tuplet to preserve tuplet ratio without reducing:

        >>> tuplet = abjad.Tuplet("6:4", "c'4 d' e'")
        >>> abjad.f(tuplet)
        \times 4/6 {
            c'4
            d'4
            e'4
        }

        >>> tuplet = abjad.Tuplet((4, 6), "c'4 d' e'")
        >>> abjad.f(tuplet)
        \times 4/6 {
            c'4
            d'4
            e'4
        }

::

    NEW. Taught Abjad about LilyPond \tuplet command:

        >>> voice = abjad.Voice(r"\tuplet 6/4 { c'4 d' e' }")
        >>> string = abjad.lilypond(voice)
        >>> print(string)
        \new Voice
        {
            \times 4/6 {
                c'4
                d'4
                e'4
            }
        }

::

    Tuplet multiplier now returns a nonreduced fraction:

        OLD: abjad.Tuplet.multiplier returns abjad.Multiplier
        NEW: abjad.Tuplet.multiplier returns abjad.NonreducedFraction

::

    Tuplet interpreter representation now shows colon string:

        OLD:

            >>> abjad.Tuplet("6:4", "c'4 d' e'")
            Tuplet(Multiplier(4, 6), "c'4 d'4 e'4")

        NEW:

            >>> abjad.Tuplet("6:4", "c'4 d' e'")
            Tuplet('6:4', "c'4 d'4 e'4")

`#1231 <https://github.com/Abjad/abjad/issues/1231>`_. Changed ``abjad.mathtools`` to
``abjad.math``.

::

    OLD:

        abjad.mathtools.all_are_equal()
        abjad.mathtools.all_are_integer_equivalent()
        abjad.mathtools.all_are_integer_equivalent_numbers()
        abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers()
        abjad.mathtools.all_are_nonnegative_integer_powers_of_two()
        abjad.mathtools.all_are_nonnegative_integers()
        abjad.mathtools.all_are_pairs_of_types()
        abjad.mathtools.all_are_positive_integers()
        abjad.mathtools.are_relatively_prime()
        abjad.mathtools.arithmetic_mean()
        abjad.mathtools.binomial_coefficient()
        abjad.mathtools.cumulative_products()
        abjad.mathtools.cumulative_sums()
        abjad.mathtools.difference_series()
        abjad.mathtools.divisors()
        abjad.mathtools.factors()
        abjad.mathtools.fraction_to_proper_fraction()
        abjad.mathtools.greatest_common_divisor()
        abjad.mathtools.greatest_power_of_two_less_equal()
        abjad.mathtools.integer_equivalent_number_to_integer()
        abjad.mathtools.integer_to_base_k_tuple()
        abjad.mathtools.integer_to_binary_string()
        abjad.mathtools.is_assignable_integer()
        abjad.mathtools.is_integer_equivalent()
        abjad.mathtools.is_integer_equivalent_n_tuple()
        abjad.mathtools.is_integer_equivalent_number()
        abjad.mathtools.is_nonnegative_integer()
        abjad.mathtools.is_nonnegative_integer_equivalent_number()
        abjad.mathtools.is_nonnegative_integer_power_of_two()
        abjad.mathtools.is_positive_integer()
        abjad.mathtools.is_positive_integer_equivalent_number()
        abjad.mathtools.is_positive_integer_power_of_two()
        abjad.mathtools.least_common_multiple()
        abjad.mathtools._least_common_multiple_helper()
        abjad.mathtools.partition_integer_into_canonic_parts()
        abjad.mathtools.sign()
        abjad.mathtools.weight()
        abjad.mathtools.yield_all_compositions_of_integer()

    NEW:

        abjad.math.all_are_equal()
        abjad.math.all_are_integer_equivalent()
        abjad.math.all_are_integer_equivalent_numbers()
        abjad.math.all_are_nonnegative_integer_equivalent_numbers()
        abjad.math.all_are_nonnegative_integer_powers_of_two()
        abjad.math.all_are_nonnegative_integers()
        abjad.math.all_are_pairs_of_types()
        abjad.math.all_are_positive_integers()
        abjad.math.are_relatively_prime()
        abjad.math.arithmetic_mean()
        abjad.math.binomial_coefficient()
        abjad.math.cumulative_products()
        abjad.math.cumulative_sums()
        abjad.math.difference_series()
        abjad.math.divisors()
        abjad.math.factors()
        abjad.math.fraction_to_proper_fraction()
        abjad.math.greatest_common_divisor()
        abjad.math.greatest_power_of_two_less_equal()
        abjad.math.integer_equivalent_number_to_integer()
        abjad.math.integer_to_base_k_tuple()
        abjad.math.integer_to_binary_string()
        abjad.math.is_assignable_integer()
        abjad.math.is_integer_equivalent()
        abjad.math.is_integer_equivalent_n_tuple()
        abjad.math.is_integer_equivalent_number()
        abjad.math.is_nonnegative_integer()
        abjad.math.is_nonnegative_integer_equivalent_number()
        abjad.math.is_nonnegative_integer_power_of_two()
        abjad.math.is_positive_integer()
        abjad.math.is_positive_integer_equivalent_number()
        abjad.math.is_positive_integer_power_of_two()
        abjad.math.least_common_multiple()
        abjad.math._least_common_multiple_helper()
        abjad.math.partition_integer_into_canonic_parts()
        abjad.math.sign()
        abjad.math.weight()
        abjad.math.yield_all_compositions_of_integer()

`#1214 <https://github.com/Abjad/abjad/issues/1214>`_. Changed ``abjad.mutate()``
constructor to ``abjad.mutate`` module:

::

    OLD:

        abjad.mutate(argument).copy()
        abjad.mutate(argument).eject_contents()
        abjad.mutate(argument).extract()
        abjad.mutate(argument).fuse()
        abjad.mutate(argument).logical_tie_to_tuplet()
        abjad.mutate(argument).replace()
        abjad.mutate(argument).scale()
        abjad.mutate(argument).swap()
        abjad.mutate(argument).transpose()
        abjad.mutate(argument).wrap()

    NEW:

        abjad.mutate.copy(argument)
        abjad.mutate.eject_contents(argument)
        abjad.mutate.extract(argument)
        abjad.mutate.fuse(argument)
        abjad.mutate.logical_tie_to_tuplet(argument)
        abjad.mutate.replace(argument)
        abjad.mutate.scale(argument)
        abjad.mutate.swap(argument)
        abjad.mutate.transpose(argument)
        abjad.mutate.wrap(argument)

`#1213 <https://github.com/Abjad/abjad/issues/1213>`_. Changed ``abjad.IOManager`` class
to ``abjad.io`` module:

::

    OLD:

        abjad.IOManager.compare_files()
        abjad.IOManager.execute_file()
        abjad.IOManager.execute_string()
        abjad.IOManager.find_executable()
        abjad.IOManager.make_subprocess()
        abjad.IOManager.open_file()
        abjad.IOManager.open_last_log()
        abjad.IOManager.profile()
        abjad.IOManager.run_command()
        abjad.IOManager.run_lilypond()
        abjad.IOManager.spawn_subprocess()

    NEW:

        abjad.io.compare_files()
        abjad.io.execute_file()
        abjad.io.execute_string()
        abjad.io.find_executable()
        abjad.io.make_subprocess()
        abjad.io.open_file()
        abjad.io.open_last_log()
        abjad.io.profile()
        abjad.io.run_command()
        abjad.io.run_lilypond()
        abjad.io.spawn_subprocess()

`#1212 <https://github.com/Abjad/abjad/issues/1212>`_. Changed ``abjad.persist()``
constructor to ``abjad.persist`` module:

::

    OLD:

        abjad.persist(argument).as_ly()
        abjad.persist(argument).as_midi()
        abjad.persist(argument).as_pdf()
        abjad.persist(argument).as_png()

    NEW:

        abjad.persist.as_ly(argument)
        abjad.persist.as_midi(argument)
        abjad.persist.as_pdf(argument)
        abjad.persist.as_png(argument)

You must now pass an explicit path to the following:

::

    abjad.persist.as_ly(argument)
    abjad.persist.as_midi(argument)
    abjad.persist.as_pdf(argument)
    abjad.persist.as_png(argument)

`#1196 <https://github.com/Abjad/abjad/issues/1196>`_. Changed ``abjad.inspect()``
constructor to ``abjad.get`` module:

::

    OLD:

        abjad.inspect(argument)after_grace_container()
        abjad.inspect(argument)annotation()
        abjad.inspect(argument)annotation_wrappers()
        abjad.inspect(argument)bar_line_crossing()
        abjad.inspect(argument)before_grace_container()
        abjad.inspect(argument)contents()
        abjad.inspect(argument)descendants()
        abjad.inspect(argument)duration()
        abjad.inspect(argument)effective()
        abjad.inspect(argument)effective_staff()
        abjad.inspect(argument)effective_wrapper()
        abjad.inspect(argument)grace()
        abjad.inspect(argument)has_effective_indicator()
        abjad.inspect(argument)has_indicator()
        abjad.inspect(argument)indicator()
        abjad.inspect(argument)indicators()
        abjad.inspect(argument)leaf()
        abjad.inspect(argument)lineage()
        abjad.inspect(argument)logical_tie()
        abjad.inspect(argument)markup()
        abjad.inspect(argument)measure_number()
        abjad.inspect(argument)parentage()
        abjad.inspect(argument)pitches()
        abjad.inspect(argument)report_modifications()
        abjad.inspect(argument)sounding_pitch()
        abjad.inspect(argument)sounding_pitches()
        abjad.inspect(argument)sustained()
        abjad.inspect(argument)timespan()

    NEW:

        abjad.get.after_grace_container(argument)
        abjad.get.annotation(argument)
        abjad.get.annotation_wrappers(argument)
        abjad.get.bar_line_crossing(argument)
        abjad.get.before_grace_container(argument)
        abjad.get.contents(argument)
        abjad.get.descendants(argument)
        abjad.get.duration(argument)
        abjad.get.effective(argument)
        abjad.get.effective_staff(argument)
        abjad.get.effective_wrapper(argument)
        abjad.get.grace(argument)
        abjad.get.has_effective_indicator(argument)
        abjad.get.has_indicator(argument)
        abjad.get.indicator(argument)
        abjad.get.indicators(argument)
        abjad.get.leaf(argument)
        abjad.get.lineage(argument)
        abjad.get.logical_tie(argument)
        abjad.get.markup(argument)
        abjad.get.measure_number(argument)
        abjad.get.parentage(argument)
        abjad.get.pitches(argument)
        abjad.get.report_modifications(argument)
        abjad.get.sounding_pitch(argument)
        abjad.get.sounding_pitches(argument)
        abjad.get.sustained(argument)
        abjad.get.timespan(argument)

`#1191 <https://github.com/Abjad/abjad/issues/1191>`_. Removed ``abjad.Infinity``,
``abjad.NegativeInfinity`` "singletons." Previously ``abjad.Infinity`` was an
instance of the ``abjad.mathtools.Infinity`` class. This was confusing. Because
``abjad.Infinity`` looked like a class but wasn't:

::

    OLD:

        foo is abjad.Infinity
        foo is not abjad.Infinity

    NEW:

        foo == abjad.Infinity()
        foo != abjad.Infinity()

Moved four fancy iteration functions to top-level:

::

    OLD:

        abjad.iterate(argument).leaf_pairs()
        abjad.iterate(argument).pitch_pairs()
        abjad.iterate(argument).vertical_moments()
        abjad.iterate(argument).out_of_range()

    NEW:

        abjad.iterate_leaf_pairs(argument)
        abjad.iterate_pitch_pairs(argument)
        abjad.iterate_vertical_moments(argument)
        abjad.iterate_out_of_range(argument)

Moved rewrite-meter functionality to ``abjad.Meter``:

::

    OLD:

        abjad.mutate(argument).rewrite_meter()

    NEW:

        abjad.Meter.rewrite_meter(argument)

----

**LESS-SIGNIFICANT CHANGES.**

`#1242 <https://github.com/Abjad/abjad/issues/1242>`_. Removed two classes:

::

    OLD:

        abjad.Staccato
        abjad.Staccatissimo

    NEW:

        abjad.Articulation("staccato")
        abjad.Articulation("staccatissimo")

`#1198 <https://github.com/Abjad/abjad/issues/1198>`_. Changed access to the Abjad
configuration class. The old "singleton" pattern wasn't well supported by Python. Now
just instantiate a new configuration object any time one is required:

::

    OLD:

        abjad.configuration

    NEW:

        abjad.Configuration()

`#1195 <https://github.com/Abjad/abjad/issues/1195>`_. Changed ``abjad.Fraction`` alias
from ``fractions.Fraction`` to ``quicktions.Fraction``. All installs of Abjad now depend
on Python's ``quicktions`` package.


`#1168 <https://github.com/Abjad/abjad/issues/1168>`_. Removed unused IO methods:

::

    abjad.IOManager.clear_terminal()
    abjad.IOManager.get_last_output_file_name()
    abjad.IOManager.get_next_output_file_name()
    abjad.IOManager.open_last_ly()
    abjad.IOManager.open_last_pdf()
    abjad.IOManager.save_last_ly_as()
    abjad.IOManager.save_last_pdf_as()

`#1133 <https://github.com/Abjad/abjad/issues/1133>`_. Renamed glissando class:

::

    OLD:

        abjad.GlissandoIndicator

    NEW:

        abjad.Glissando

Changed ``abjad.Clef.from_selection()`` to ``abjad.Clef.from_pitches()``:

::

    OLD:

        leaves = abjad.select(staff).leaves()
        abjad.Clef.from_selection(leaves)

    NEW:

        pitches = abjad.iterate(staff).pitches()
        abjad.Clef.from_pitches(pitches)

Changed ``abjad.Enumerate`` class to ``abjad.enumerate`` module:

::

    OLD:

        abjad.Enumerator.yield_combinations()
        abjad.Enumerator.yield_outer_product()
        abjad.Enumerator.yield_pairs()
        abjad.Enumerator.yield_partitions()
        abjad.Enumerator.yield_permutations()
        abjad.Enumerator.yield_set_partitions()
        abjad.Enumerator.yield_subsequences()

    NEW:
        abjad.enumerate.yield_combinations()
        abjad.enumerate.yield_outer_product()
        abjad.enumerate.yield_pairs()
        abjad.enumerate.yield_partitions()
        abjad.enumerate.yield_permutations()
        abjad.enumerate.yield_set_partitions()
        abjad.enumerate.yield_subsequences()

Changed ``abjad.OrderedDict`` to no longer coerce input.

Changed ``abjad.StaffChange`` to take staff name instead of staff object:

::

    OLD:

        staff = abjad.Staff(name="RH_Staff")
        staff_change = abjad.StaffChange(staff)

    NEW:

        staff_change = abjad.StaffChange("RH_Staff")

Changed containment testing for pitch ranges:

::

    OLD:

        abjad.PitchRange.__contains__()

    NEW:

        abjad.sounding_pitches_are_in_range()

Changed pitch ``from_selection()`` methods to accept only explicit selection:

::

    OLD:

        abjad.PitchSegment.from_selection(staff)

    NEW:

        selection = abjad.select(staff)
        abjad.PitchSegment.from_selection(selection)

Changed ``strict=None`` keyword to ``align_tags=None``:

::

    OLD:

        abjad.f(argument, strict=None)
        abjad.show(argument, strict=None)
        abjad.persist().as_ly(strict=None)
        abjad.persist().as_pdf(strict=None)

    NEW:

        abjad.f(argument, align_tags=None)
        abjad.show(argument, align_tags=None)
        abjad.persist.as_ly(argument, align_tags=None)
        abjad.persist.as_pdf(argument, align_tags=None)

Moved accidental respell functions to new ``iterpitches`` module:

::

    OLD:

        abjad.Accidental.respell_with_flats()
        abjad.Accidental.respell_with_sharps()

    NEW:

        abjad.iterpitches.respell_with_flats()
        abjad.iterpitches.respell_with_sharps()

Moved logical-tie-to-tuplet functionality:

::

    OLD:

        abjad.LogicalTie.to_tuplet()

    NEW:

        abjad.mutate.logical_tie_to_tuplet()

Moved tag functionality:

::

    OLD: abjad.Tag.tag()
    NEW: abjad.tag.tag()

Moved transposition functions to new ``abjad.iterpitches`` module:

::

    OLD:

        abjad.Instrument.transpose_from_sounding_pitch()
        abjad.Instrument.transpose_from_written_pitch()

    NEW:

        abjad.iterpitches.transpose_from_sounding_pitch()
        abjad.iterpitches.transpose_from_written_pitch()

Moved tuplet-maker functionality to new ``abjad.makers`` module:

::

    OLD:

        abjad.Tuplet.from_duration_and_ratio()
        abjad.Tuplet.from_leaf_and_ratio()
        abjad.Tuplet.from_ratio_and_pair()

    NEW:

        abjad.makers.tuplet_from_duration_and_ratio()
        abjad.makers.tuplet_from_leaf_and_ratio()
        abjad.makers.tuplet_from_ratio_and_pair()

Moved wellformedness functionality to new ``abjad.wf`` module:

::

    OLD:

        abjad.inspect(argument).wellformed()
        abjad.inspect(argument).tabulate_wellformedness()

    NEW:

        abjad.wf.wellformed(argument)
        abjad.wf.tabulate_wellformedness(argument)

Refactored overrides, settings, tweaks (first wave):

::

    OLD: abjad.LilyPondGrobOverride
    NEW: abjad.LilyPondOverride

    OLD: abjad.LilyPondContextSetting
    NEW: abjad.LilyPondSetting

    OLD: abjad.LilyPondNameManager
    NEW: abjad.Interface

    OLD: abjad.LilyPondGrobNameManager
    NEW: abjad.OverrideInterface

    OLD: abjad.LilyPondSettingNameManager
    NEW: abjad.SettingInterface

    OLD: abjad.LilyPondTweakManager
    NEW: abjad.TweakInterface

Removed ``abjad.MarkupList``.

Removed ``abjad.Path``.

Removed ``abjad.SortedCollection`` class.

Removed ``abjad.String.is_segment_name()``.

Removed ``abjad.TestManager``:

::

    OLD: abjad.TestManager.compare_files()
    NEW: abjad.io.compare_files()

Removed "abj:" parsing from containers:

::

    OLD:

        string = "abj: | 3/4 c'32 d'8 e'8 fs'4... |"
        staff = abjad.Staff(string)

    NEW:

        string = "| 3/4 c'32 d'8 e'8 fs'4... |"
        container = abjad.parsers.reduced.parse_reduced_ly_syntax(string)
        staff = abjad.Staff()
        staff.append(container)

Removed component multiplication:

::

    OLD:

        3 * abjad.Note("c'4")

    NEW:

        note = abjad.Note("c'4")
        abjad.mutate.copy(note, 3)

Removed RTM parsing from containers:

::

    OLD:

        abjad.Container("rtm: (1 (1 1 1)) (2 (2 (1 (1 1 1)) 2))")

    NEW:

        abjad.rhythmtrees.parser_rtm_syntax("(1 (1 1 1)) (2 (2 (1 (1 1 1)) 2))")

----

Deprecated in Abjad 3.2
-----------------------

``format()`` and ``abjad.f()`` are both deprecated. Removed ``__format__()``
definitions and corresponding use of ``format()`` from Abjad in this release. Removal of
``abjad.f()`` will follow in a later release:

::

    OLD:

        format(item, "lilypond")
        format(item, "storage")

    NEW:

        abjad.lilypond(item)
        abjad.storage(item)

::

    OLD:

        abjad.f(item)

    NEW:

        string = abjad.lilypond(item)
        print(string)

``add_final_barline()`` and ``add_final_markup()`` are both deprecated. These two
functions are still available in the new ``abjad.deprecated`` module. Users should
instead move to making and attaching bar line or markup objects by hand, just like usual
in a score:

::

    OLD:

        abjad.Score.add_final_barline()
        abjad.Score.add_final_markup()

    NEW:

        abjad.deprecated.add_final_barline()
        abjad.deprecated.add_final_markup()

----

Fixes in Abjad 3.2
------------------

`#1245 <https://github.com/Abjad/abjad/issues/1245>`_, `#1247
<https://github.com/Abjad/abjad/pull/1247>`_. Removed duplicate indicators when
fusing leaves. (`Tsz Kiu Pang <https://nivlekp.github.io/>`_).

`#1201 <https://github.com/Abjad/abjad/issues/1201>`_. Fixed multipart tuplet split.

----

Cleanup in Abjad 3.2
--------------------

* Activated Sphinx's ``sphinx.ext.viewcode`` extension in the docs
  as suggested by `jgarte <https://github.com/jgarte>`_
* `#1225 <https://github.com/Abjad/abjad/issues/1225>`_.
  Adjusted ``collections.abc`` imports to mollify mypy
  (`Oberholtzer <https://github.com/josiah-wolf-oberholtzer>`_)
* Added private ``_iterate.py`` module
* Added private ``_update.py`` module
* Added ``attach.py`` module
* Added ``bundle.py`` module
* Added ``configuration.py`` module
* Added ``contextmanagers.py`` module
* Added ``cyclictuple.py`` module
* Added ``duration.py`` module
* Added ``expression.py`` module
* Added ``format.py`` module
* Added ``label.py`` module
* Added ``lilypondfile.py`` module
* Added ``lyconst.py``, ``lyenv.py``, ``lyproxy.py`` modules
* Added ``new.py`` module
* Added ``overrides.py`` module
* Added ``parsers/`` directory
* Added ``ratio.py`` module
* Added ``score.py`` module
* Added ``segmentmaker.py`` module
* Added ``select.py`` module
* Added ``sequence.py`` module
* Added ``storage.py`` module
* Added ``typedcollections.py`` module
* Added ``verticalmoment.py`` module
* Added ``pitch/operators.py`` module
* Added ``pitch/pitches.py`` module
* Added ``pitch/segments.py`` module
* Added ``pitch/sets.py`` module
* Added ``pitch/pitchclasses.py`` module
* Added ``pitch/intervalclasses.py`` module
* Alphabetized Abjad initializer
* Changed single backticks to double backticks in Sphinx docstring markup
* Cleaned up ``abjad.Configuration._make_missing_directories()``
* Cleaned up exception messaging
* Cleaned up f-strings
* Defined ``abjad.Duration.__ne()__`` explicitly
* Emptied subpackage initializers
* Moved LilyPond scrape scripts to ``ly/`` in wrapper directory
* Moved ``yield_all_modules()`` to ``configuration.py`` module
* Reformatted with black 20.8b1
* Removed ``__illustrate__()`` method from pitches
* Removed abstract decorators from pitch and interval classes
* `#1218 <https://github.com/Abjad/abjad/issues/1218>`_.
  Removed ``abjad/etc/`` directory
* Removed ``const.py`` module
* Removed ``import *`` statements
* Removed ``scr/devel/`` directory; use ``scr/`` instead
* Removed ``tags.py`` module
* Removed ``top.py`` module
* Removed ties from ``abjad.Note``, ``abjad.Chord`` reprs
* `#1210 <https://github.com/Abjad/abjad/issues/1210>`_.
  Reran LilyPond scrape scripts with LilyPond 2.19.84

:author:`[Bača (3.2-3)]`
