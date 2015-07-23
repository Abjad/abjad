:orphan:

Abjad 2.7
---------

Released 2012-02-27. Built from r5100. 
Implements 221 public classes and 1029 functions totalling 168,000 lines of code.

- Added ``lilypondparsertools.LilyPondParser`` class, which arses a subset of LilyPond input syntax::

    >>> from abjad.tools.lilypondparsertools import LilyPondParser
    >>> parser = LilyPondParser( )
    >>> input = r"\new Staff { c'4 ( d'8 e' fs'2) \fermata }"
    >>> result = parser(input)
    >>> f(result)
    \new Staff {
        c'4 (
        d'8
        e'8
        fs'2 -\fermata )
    }

  LilyPondParser defaults to English note names, but any of the other
  languages supported by LilyPond may be used::

    >>> parser = LilyPondParser('nederlands')
    >>> input = '{ c des e fis }'
    >>> result = parser(input)
    >>> f(result)
    {
        c4
        df4
        e4
        fs4
    }

  Briefly, LilyPondParser understands theses aspects of LilyPond syntax:

  - Notes, chords, rests, skips and multi-measure rests
  - Durations, dots, and multipliers
  - All pitchnames, and octave ticks
  - Simple markup (i.e. ``c'4 ^ "hello!"``)
  - Most articulations
  - Most spanners, including beams, slurs, phrasing slurs, ties, and glissandi
  - Most context types via ``\new`` and ``\context``, as well as context ids (i.e. ``\new Staff = "foo" { }``)
  - Variable assignment (i.e. ``global = { \time 3/4 } \new Staff { \global }``)
  - Many music functions:
    - ``\acciaccatura``
    - ``\appoggiatura``
    - ``\bar``
    - ``\breathe``
    - ``\clef``
    - ``\grace``
    - ``\key``
    - ``\transpose``
    - ``\language``
    - ``\makeClusters``
    - ``\mark``
    - ``\oneVoice``
    - ``\relative``
    - ``\skip``
    - ``\slashedGrace``
    - ``\time``
    - ``\times``
    - ``\transpose``
    - ``\voiceOne``, ``\voiceTwo``, ``\voiceThree``, ``\voiceFour``

  LilyPondParser currently **DOES NOT** understand many other aspects of LilyPond syntax:

  - ``\markup``
  - ``\book``, ``\bookpart``, ``\header``, ``\layout``, ``\midi`` and ``\paper``
  - ``\repeat`` and ``\alternative``
  - Lyrics
  - ``\chordmode``, ``\drummode`` or ``\figuremode``
  - Property operations, such as ``\override``, ``\revert``, ``\set``, ``\unset``, and ``\once``
  - Music functions which generate or extensively mutate musical structures
  - Embedded Scheme statements (anything beginning with ``#``)


- Added ``systemtools.p( )``, for conveniently parsing LilyPond syntax::

    >>> result = p(r"\new Staff { c'4 d e f }")
    >>> f(result)
    \new Staff {
        c'4
        d4
        e4
        f4
    }


- Added ``schemetools.Scheme``, as a more robust replacement for nearly all other ``schemetools``
  classes::

    >>> from abjad.tools.schemetools import Scheme
    >>> print Scheme(True).format
    ##t
    >>> print Scheme('a', 'list', 'of', 'strings').format
    #(a list of strings)
    >>> print Scheme(('simulate', 'a', 'vector'), quoting="'#").format
    #'#(simulate a vector)
    >>> print Scheme('a', ('nested', ('data', 'structure'))).format
    #(a (nested (data structure))

- Removed deprecated ``schemetools`` classes:

  * ``SchemeBoolean``
  * ``SchemeFunction``
  * ``SchemeNumber``
  * ``SchemeString``
  * ``SchemeVariable``

  In all cases, simply use ``schemetools.Scheme`` instead.


- Reimplemented MarkupCommand.

  The new implementation is initialized from a command-name, and a variable-size
  list of arguments.  Arguments which are lists or tuples will be enclosed in
  curly-braces::

    >>> from abjad.tools.markuptools import MarkupCommand
    >>> bold = MarkupCommand('bold', ['two', 'words'])
    >>> rotate = MarkupCommand('rotate', 60, bold)
    >>> triangle = MarkupCommand('triangle', False)
    >>> concat = MarkupCommand('concat', ['one word', rotate, triangle])
    >>> print concat.format
    \concat { #"one word" \rotate #60 \bold { two words } \triangle ##f }


- Added ``indicatortools.TempoInventory``, which models an ordered list of tempos::

    >>> indicatortools.TempoInventory([('Andante', Duration(1, 8), 72), ('Allegro', Duration(1, 8), 84)])
    TempoInventory([Tempo('Andante', Duration(1, 8), 72), Tempo('Allegro', Duration(1, 8), 84)])

  Inherits from list. Allows initialization, append and extent on tempo tokens.


- Added new ``pitchtools.PitchRangeInventory`` class.

  The class acts as an ordered list of PitchRange objects.

  The purpose of the class is to model something like palettes of different pitches
  available in all part of a score::

    >>> pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])
    PitchRangeInventory([PitchRange('[C3, C6]'), PitchRange('[C4, C6]')])

  The class inherits from list.

- Added ``mathtools.all_are_pairs()`` predicate::

    >>> from abjad.tools.sequencetools import all_are_pairs
    >>> all_are_pairs([(1, 2), (3, 4), (5, 6)])
    True

- Added ``mathtools.all_are_pairs_of_types()`` predicate::

    >>> from abjad.tools.sequencetools import all_are_pairs_of_types
    >>> all_are_pairs_of_types([('a', 1.4), ('b', 2.3), ('c', 1.5)], str, float)
    True

- Added ``stringtools.is_snake_case_file_name_with_extension()`` string predicate::

    >>> stringtools.is_snake_case_file_name_with_extension('foo_bar.blah')
    True

- Added ``systemtools.is_underscore_delimited_file_name()`` string predicate.

  Returns true on any underscore-delimited lowercase string.

  Also returns trun on an underscore-delimtied lowercase string terminated with an extension.

  ::

    >>> stringtools.is_snake_case_file_name('foo_bar.py')
    True

    >>> stringtools.is_snake_case_file_name('foo_bar')
    True


- Added ``ImpreciseTempoError`` to exceptions.

- Added ``LilyPondParserError`` to exceptions.

- Added ``scr/devel/fix-test-cases``.  The script is a two-line wrapper around the following other two scripts:

  * ``scr/devel/fix-test-case-names``
  * ``scr/devel/fix-test-case-numbers``


- Extended ``Container`` to use ``LilyPondParser`` to parse input strings.

- Extended ``indicatortools.InstrumentMark``, ``scoretools.Performer`` and 
  ``markuptools.Markup`` with ``__hash__`` equality.

  Now, if two instances compare equally (via ==), their hashes also compare equally,
  allowing for more intuitive use of these classes as dictionary keys.

- Extended ``indicatortools.Tempo`` with textual indications and tempo ranges
  You may instantiate as normal, or in some new combinations::

    >>> from abjad.tools.indicatortools import Tempo
    >>> t = Tempo('Langsam', Duration(1, 4), (52, 57))
    >>> t = Tempo('Langsam')
    >>> t = Tempo((1, 4), (52, 57))

  In addition to its new read/write "textual_indication" attribute, Tempo
  now also exposes a read-only "is_imprecise" property, which returns True if
  the mark can not be expressed simply as duration=units_per_minute.  Arithmetic
  operations on TempoMarks will now raise ImpreciseTempoErrors if any mark
  involved is imprecise.

- Extended tempos to be able to initialize from 'tempo tokens'.
  A tempo token is a length-2 or length-3 tuple of tempo arguments.

- Extended tempo with ``is_tempo_token()`` method::

    >>> tempo = indicatortools.Tempo(Duration(1, 4), 72)
    >>> tempo.is_tempo_token((Duration(1, 4), 84))
    True

- Extended case-testing ``systemtools`` string predicates to allow digits.

  Functions changed:

  * ``stringtools.is_space_delimited_lowercase_string``
  * ``stringtools.is_snake_case_file_name``
  * ``stringtools.is_lower_camel_case_string``
  * ``stringtools.is_upper_camel_case_string``
  * ``stringtools.is_snake_case_string``
  * ``stringtools.is_snake_case_file_name_with_extension``

- Extended ``lilypondfiletools.NonattributedBlock`` with ``is_formatted_when_empty`` read-write property.
  ``lilypondfiletools.ScoreBlock`` no longer formats when empty, by default.

- Extended ``indicatortools.BarLine`` with ``format_slot`` keyword.

- Extended ``pitchtools.PitchRange`` class with read-only ``pitch_range_name`` and ``pitch_range_name_markup`` attributes.

- Extended ``scoretools.InstrumentationSpecifier`` with read-only ``performer_name_string`` attribute.

- Extended all ``beamtools.Beam-``, ``Slur-`` and ``Hairpin-``related spanner classes, as well as
  ``spannertools.Tie` with an optional ``direction`` keyword::

    >>> c = Container("c'4 d'4 e'4 f'4")
    >>> spanner = spannertools.Slur(c[:], 'up')
    >>> f(c)
    {
        c'4 ^ (
        d'4
        e'4
        f'4 )
    }

  The direction options are exactly the same as for ``Articulation`` and ``Markup``: 
  ``'up'``, ``'^'``, ``'down'``, ``'_'``, ``'neutral'``, ``'-'`` and ``None``.

- Extended ``tonalanalysistools.Scale`` with ``create_named_pitch_set_in_pitch_range()`` method.


- Changed ``scoretools.FixedDurationTuplet.multiplier`` to return fraction instead of duration.


- Renamed attributes, methods and functions throughout ``intervaltreetools``:

  * ``centroid`` => ``center`` (except where a weighted mean is actually used)
  * ``high`` => stop``
  * ``high_min`` => earliest_stop``
  * ``high_max`` => latest_stop``
  * ``low`` => ``start``
  * ``low_min`` => ``earliest_start``
  * ``low_max`` => ``latest_start``
  * ``magnitude`` => ``duration``

  This both clarifies the API, and prevents shadowing of Python's builtin ``min()`` and ``max()``.

- Renamed ``indicatortools.Articulation.direction_string`` => ``indicatortools.Articulation.direction``.

- Renamed ``markuptools.Markup.direction_string` => ``markuptools.Markup.direction``.

- Renamed ``scoretools.Tuplet.ratio`` to ``scoretools.Tuplet.ratio_string``.

- Renamed ``scr/devel/find-nonalphabetized-method-names`` to ``scr/devel/find-nonalphabetized-class-attributes``.


- Improved ``scr/devel/find-nonalphabetzied-methods``.

- Updated literature examples to match API changes.

- Removed ancient ``scoretools.make_invisible_staff()``.

- Added ``text_editor`` key to user config dictionary (in ``~/.abjad/config.py``).

- Improved ``__repr__`` strings of ``tonalanalysistools.Mode`` and ``tonalanalysistools.Scale``.

- ``indicatortools.Tempo`` ``__repr__`` now shows ``__repr__`` version of duration
  instead of string version of duration.

- ``scr/devel/abj-grp`` no longer excludes lines of code that include the string ``'svn'``.
