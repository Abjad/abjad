:orphan:

Abjad 2.6
---------

Released 2012-01-29. Built from r4979. 
Implements 197 public classes and 941 public functions totalling 153,000 lines of code.

* Added top-level ``decorators`` directory with ``requires`` decorator.
  The ``requires`` decorator renders the following two function definitions equivalent::

    from abjad.tools.decoratortools import requires

  ::

    @requires(int)
    def foo(x):
        return x ** 2

  ::

    def foo(x):
        assert isinstance(x, int)
        return x ** 2

* Added new classes to ``scoretools``::

    scoretools.InstrumentationSpecifier
    scoretools.Performer

* Added ``scoretools.list_performer_names()``::

    >>> for name in scoretools.list_performer_names()[:10]:
    ...     name
    ... 
    'accordionist'
    'bassist'
    'bassoonist'
    'cellist'
    'clarinetist'
    'flutist'
    'guitarist'
    'harpist'
    'harpsichordist'
    'hornist'

* Added ``scoretools.list_primary_performer_names()``.

* Added ``scoretools.measure_to_one_line_input_string()``::

    >>> measure = Measure((3, 4), "c4 d4 e4")

  ::

    >>> measure
    Measure(3/4, [c4, d4, e4])

  ::

    >>> scoretools.measure_to_one_line_input_string(measure)
    "Measure((3, 4), 'c4 d4 e4')"

* Added new classes to ``instrumenttools``::

    SopraninoSaxophone
    SopranoSaxophone
    AltoSaxophone
    TenorSaxophone
    BaritoneSaxophone
    BassSaxophone
    ContrabassSaxophone

  ::

    ClarinetInA

  ::

        AltoTrombone
        BassTrombone

  ::

        Harpsichord

* Added known untuned percussion::

    >>> for name in instrumenttools.UntunedPercussion.known_untuned_percussion[:10]:
    ...     print name
    ... 
    agogô
    anvil
    bass drum
    bongo drums
    cabasa
    cajón
    castanets
    caxixi
    claves
    conga drums

* Added ``_Instrument.get_default_performer_name()``::

    >>> bassoon = instrumenttools.Bassoon()

  ::

    >>> bassoon.get_default_performer_name()
    'bassoonist'

* Added ``_Instrument.get_performer_names()``::

    >>> bassoon.get_performer_names()
    ['instrumentalist', 'reed player', 'double reed player', 'bassoonist']

* Added read / write ``_Instrument.pitch_range``::

    >>> marimba.pitch_range = (-24, 36)
    >>> marimba.pitch_range
    PitchRange('[C2, C7]')

* Added read-only ``_Instrument.default_pitch_range``::

    >>> marimba = instrumenttools = instrumenttools.Marimba()
    >>> marimba.default_pitch_range
    PitchRange('[F2, C7]')

* Added ``instrumenttools.list_instruments()``::

    >>> for instrument_name in instrumenttools.list_instrument_names()[:10]:
    ...     instrument_name
    ... 
    'accordion'
    'alto flute'
    'alto saxophone'
    'alto trombone'
    'clarinet in B-flat'
    'baritone saxophone'
    'bass clarinet'
    'bass flute'
    'bass saxophone'
    'bass trombone'

* Added other functions to ``instrumenttools``::

    instrumenttools.list_primary_instrument_names()
    instrumenttools.list_secondary_instrument_names()

* Added new class to ``lilypondfiletools``::

    ContextBlock

* Added ``pitchtools.is_symbolic_pitch_range_string()``::

    >>> pitchtools.is_symbolic_pitch_range_string('[A0, C8]')
    True

* Added ``pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name()``::

    >>> pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('A#4')
    "as'"

* Added ``pitchtools.symbolic_string_to_alphabetic_accidental_string_abbreviation()``::

    >>> pitchtools.abbreviation_to_symbolic_string('tqs')
    '#+'

* Added other new functions to ``pitchtools``::

    pitchtools.abbreviation_to_symbolic_string()
    pitchtools.is_smbolic_accidental_string()
    pitchtools.is_pitch_class_octave_number_string()

* Added ``stringtools.string_to_accent_free_snake_case()``::

    >>> stringtools.string_to_accent_free_snake_case('Déja vu')
    'deja_vu'

* Added ``stringtools.strip_diacritics_from_binary_string()``::

    >>> binary_string = 'Dvořák'
    >>> stringtools.strip_diacritics_from_binary_string(binary_string)
    'Dvorak'

* Added other new functions to ``systemtools``::

    stringtools.capitalize_string_start()
    systemtools.is_space_delimited_lowercamelcase_string()
    systemtools.is_underscore_delimited_lowercamelcase_package_name()
    systemtools.is_underscore_delimited_lowercamelcase_string()
    stringtools.is_lower_camel_case_string()
    stringtools.is_upper_camel_case_string()
    stringtools.space_delimited_lowercase_to_upper_camel_case()
    stringtools.upper_camel_case_to_space_delimited_lowercase()
    stringtools.upper_camel_case_to_snake_case()

* Added new functions to ``mathtools``::

    mathtools.is_positive_integer_power_of_two()
    mathtools.is_integer_equivalent_expr()

* Added sequence type-checking predicates::

    scoretools.all_are_chords()
    scoretools.all_are_containers()
    durationtools.all_are_duration_tokens()
    durationtools.all_are_durations()
    gracetools.all_are_grace_containers()
    scoretools.all_are_leaves()
    markuptools.all_are_markup()
    scoretools.all_are_measures()
    scoretools.all_are_notes()
    pitcharraytools.all_are_pitch_arrays()
    pitchtools.all_are_named_pitch_tokens()
    scoretools.all_are_rests()
    scoretools.all_are_scores()
    sievetools.all_are_residue_class_expressions()
    scoretools.all_are_skips()
    spannertools.all_are_spanners()
    scoretools.all_are_staves()
    scoretools.all_are_tuplets()

* Extended ``NamedPitch`` to allow initialization from pitch-class / octave number strings::

    >>> pitchtools.NamedPitch('C#2')
    NamedPitch('cs,')

* Extended ``PitchRange`` to allow initialization from symbolic pitch range strings::

    >>> pitchtools.PitchRange('[A0, C8]')
    PitchRange('[A0, C8]')

* Extended ``PitchRange`` to allow initialization from pitch-class / octave number strings::

    >>> pitchtools.PitchRange('A0', 'C8')
    PitchRange('[A0, C8]')

* Extended ``scoretools.is_bar_line_crossing_leaf()`` to work when no explicit time signature is found.
* Extended ``Markup`` to be able to function as a top-level ``LilyPondFile`` element.
* Extended instruments with ``is_primary`` and ``is_secondary`` attributes.
* Extended instruments with ``instrument_name`` and ``instrument_name_markup`` attributes.
* Extended instruments with ``short_instrument_name`` and ``short_instrument_name_markup`` attributes.
* Extended ``systemtools.IOManager.write_expr_to_ly()`` and ``systemtools.IOManager.write_expr_to_pdf()`` with ``'tagline'`` keyword.
* Extended ``replace-in-files`` script to skip ``.text``, ``.ly`` and ``.txt`` files.

* Renamed ``Accidental.symbolic_string`` to ``Accidental.symbolic_string``.
* Renamed ``Accidental.alphabetic_string`` to ``Accidental.abbreviation``.

* Fixed bug in ``topleveltools.play()``.
* Fixed bug in ``quantizationtools`` regarding quantizing a stream of ``QEvents`` directly.
