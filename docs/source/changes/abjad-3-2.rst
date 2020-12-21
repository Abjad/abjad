3.2
===

Changes from Abjad 3.1 (2019-12-19) to Abjad 3.2 (2020-12-13).

----

**CHANGES.**

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

Moved accidental respell functions to top level:

::

    OLD:

        abjad.Accidental.respell_with_flats()
        abjad.Accidental.respell_with_sharps()

    NEW:

        abjad.respell_with_flats()
        abjad.respell_with_sharps()

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

**DEPRECATED.**

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

**FIXES.**

`#1245 <https://github.com/Abjad/abjad/issues/1245>`_, `#1247
<https://github.com/Abjad/abjad/pull/1247>`_. Removed duplicate indicators when
fusing leaves. (`Tsz Kiu Pang <https://nivlekp.github.io/>`_).

`#1201 <https://github.com/Abjad/abjad/issues/1201>`_. Fixed multipart tuplet split.

----

**PACKAGE CLEANUP.**

* Alphabetized Abjad initializer
* Emptied subpackage initializers
* Removed ``import *`` statements

----

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
* Removed ``tags.py`` module
* Removed ``top.py`` module

----

* Added ``pitch/operators.py`` module
* Added ``pitch/pitches.py`` module
* Added ``pitch/segments.py`` module
* Added ``pitch/sets.py`` module
* Added ``pitch/pitchclasses.py`` module
* Added ``pitch/intervalclasses.py`` module
* Removed ``__illustrate__()`` method from pitches
* Removed abstract decorators from pitch and interval classes

----

**OTHER CLEANUP.**

* `#1225 <https://github.com/Abjad/abjad/issues/1225>`_.
  Adjusted ``collections.abc`` imports to mollify mypy.
  (`Oberholtzer <https://github.com/josiah-wolf-oberholtzer>`_)

* `#1218 <https://github.com/Abjad/abjad/issues/1218>`_.
  Removed ``abjad/etc/`` directory

* `#1210 <https://github.com/Abjad/abjad/issues/1210>`_.
  Reran LilyPond scrape scripts with LilyPond 2.19.84

* Cleaned up ``abjad.Configuration._make_missing_directories()``

* Cleaned up exception messaging

* Cleaned up f-strings

* Defined ``abjad.Duration.__ne()__`` explicitly

* Moved LilyPond scrape scripts to ``ly/`` in wrapper directory

* Moved ``yield_all_modules()`` to ``configuration.py`` module

* Reformatted with black 20.8b1

* Removed ``const.py`` module

* Removed ``scr/devel/`` directory. Use ``scr/`` instead

* Removed ties from ``abjad.Note``, ``abjad.Chord`` reprs

----

**DOCS.**

Activated Sphinx's ``sphinx.ext.viewcode`` extension in the docs.
As suggested by `jgarte <https://github.com/jgarte>`_.

Changed single backticks to double backticks in Sphinx docstring markup.

----

*Authored: Bača (3.2).*
