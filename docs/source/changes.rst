Changes (3.2)
=============

Changes from Abjad 3.1 (2019-12-18) to Abjad 3.2 (2020-12-12).

----

**DOCS.**

Activated Sphinx's ``sphinx.ext.viewcode`` extension in the docs.
As suggested by `jgarte <https://github.com/jgarte>`_.

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

`#1214 <https://github.com/Abjad/abjad/issues/1214>`_. Replaced ``abjad.mutate()``
constructor with ``abjad.mutate`` module:

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

`#1213 <https://github.com/Abjad/abjad/issues/1213>`_. Replaced ``abjad.IOManager`` class
with ``abjad.io`` module:

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

`#1212 <https://github.com/Abjad/abjad/issues/1212>`_. Replaced ``abjad.persist()``
constructor with ``abjad.persist`` module:

::

    OLD:

        abjad.persist(argument).as_ly()
        abjad.persist(argument).as_midi()
        abjad.persist(argument).as_pdf()

    NEW:

        abjad.persist.as_ly(argument)
        abjad.persist.as_midi(argument)
        abjad.persist.as_pdf(argument)

`#1196 <https://github.com/Abjad/abjad/issues/1196>`_. Replaced ``abjad.inspect()``
constructor with ``abjad.get`` module:

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

Replaced ``abjad.Enumerate`` class with ``abjad.enumerate`` module:

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

Replaced ``abjad.Wellformedness`` class with ``abjad.wf`` module:

::

    OLD: abjad.wellformedness(argument)
    OLD: abjad.Wellformedness.tabulate_wellformedness(argument)

    NEW: abjad.wf.wellformedness(argument)
    NEW: abjad.wf.tabulate_wellformedness(argument)

Moved transposition functions to new ``abjad.iterpitches`` module:

::

    OLD:

        abjad.Instrument.transpose_from_sounding_pitch()
        abjad.Instrument.transpose_from_written_pitch()

    NEW:

        abjad.iterpitches.transpose_from_sounding_pitch()
        abjad.iterpitches.transpose_from_written_pitch()

Changed ``abjad.Clef.from_selection()`` to ``abjad.Clef.from_pitches()``:

::

    OLD:

        leaves = abjad.select(staff).leaves()
        abjad.Clef.from_selection(leaves)

    NEW:

        pitches = abjad.iterate(staff).pitches()
        abjad.Clef.from_pitches(pitches)

Moved ``tag()`` function:

::

    OLD: abjad.Tag.tag()
    NEW: abjad.tag.tag()

Renamed ``strict=None`` keyword to ``align_tags=None``:

::

    OLD:

        abjad.f(..., strict=None)
        abjad.show(..., strict=None)
        abjad.persist().as_ly(strict=None)
        abjad.persist().as_pdf(strict=None)

    NEW:

        abjad.f(..., align_tags=None)
        abjad.show(..., align_tags=None)
        abjad.persist.as_ly(..., align_tags=None)
        abjad.persist.as_pdf(..., align_tags=None)

Removed ``abjad.MarkupList``.

Removed ``abjad.String.is_segment_name()``.

Removed ``abjad.TestManager``:

::

    OLD: abjad.TestManager.compare_files()
    NEW: abjad.IOManager.compare_files()

Refactored ``abjad.StaffChange`` to take staff name instead of staff object.

::

    OLD:

        staff = abjad.Staff(name="RH_Staff")
        staff_change = abjad.StaffChange(staff)

    NEW:

        staff_change = abjad.StaffChange("RH_Staff")

----

**DEPRECATED.**

Use of ``format()`` and ``abjad.f()`` are both deprecated. Removed ``__format__()``
definitions and corresponding use of ``format()`` from Abjad in this release. Removal of
``abjad.f()`` will follow in Abjad 3.3:

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

----

**NEW.**

----

**FIXES.**

`#1245 <https://github.com/Abjad/abjad/issues/1245>`_, `#1247
<https://github.com/Abjad/abjad/pull/1247>`_. Removed duplicate indicators when
fusing leaves. (`Tsz Kiu Pang <https://nivlekp.github.io/>`_).

----

**CLEANUP.**

* `#1225 <https://github.com/Abjad/abjad/issues/1225>`_.
  Adjusted ``collections.abc`` imports to mollify mypy.
  (`Oberholtzer <https://github.com/josiah-wolf-oberholtzer>`_).

* `#1218 <https://github.com/Abjad/abjad/issues/1218>`_.
  Removed ``abjad/dotfiles/`` directory.

* `#1210 <https://github.com/Abjad/abjad/issues/1210>`_.
  Reran LilyPond scrape scripts with LilyPond 2.19.84.

* `#1201 <https://github.com/Abjad/abjad/issues/1201>`_.
  Fixed multipart tuplet split.

* Alphabetized Abjad initializer.

* Cleaned up ``abjad.Configuration._make_missing_directories()``.

* Cleaned up markup.

* Moved LilyPond scrape scripts to ``ly/`` in wrapper directory.

* Moved ``yield_all_modules()`` to ``configuration.py`` module.

* Reformatted with black 20.8b1.

* Removed ``const.py`` module.

* Removed ``tags.py`` module.

* Replaced ``ly/`` with ``lyconst.py``, ``lyenv.py``, ``lyproxy.py`` modules.

Package cleanup:

* Moved inspectx.py, update.py, wellformedness.py to top level
* Changed OnBeatGraceContainer.py to obgc.py
* Changed select.py to selectx.py
* Added attach.py module
* Added typedcollections.py module
* Added cyclictuple.py module
* Added sequence.py module
* Added expression.py module
* Added score.py module
* Added segmentmaker.py module
* Added path.py module
