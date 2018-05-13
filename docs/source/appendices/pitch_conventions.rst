:tocdepth: 2

Pitch conventions
=================

..  abjad::

    import abjad

Pitch numbers
-------------

Abjad numbers pitches like this:

..  abjad::

    score, treble_staff, bass_staff = abjad.Score.make_piano_score()
    duration = abjad.Duration(1, 32)

..  abjad::

    pitches = range(-12, 12 + 1)
    abjad_configuration.set_default_accidental_spelling('sharps')

..  abjad::

    for pitch in pitches:
        note = abjad.Note(pitch, duration)
        rest = abjad.Rest(duration)
        if 0 <= note.written_pitch.number:
            treble_staff.append(note)
            bass_staff.append(rest)
        else:
            treble_staff.append(rest)
            bass_staff.append(note)
        number = note.written_pitch.number
        markup = abjad.Markup(str(number), Down)
        abjad.attach(markup, bass_staff[-1])

..  abjad::

    abjad.override(score).beam.transparent = True
    abjad.override(score).time_signature.stencil = False
    abjad.override(score).flag.transparent = True
    abjad.override(score).rest.transparent = True
    abjad.override(score).stem.stencil = False
    abjad.override(score).text_script.staff_padding = 6
    moment = abjad.SchemeMoment((1, 56))
    abjad.setting(score).proportional_notation_duration = moment

..  abjad::

    lilypond_file = abjad.LilyPondFile.new(
        score,
        global_staff_size=15,
        )
    show(lilypond_file)


Diatonic pitch numbers
----------------------

Abjad numbers diatonic pitches like this:

..  abjad::

    score, treble_staff, bass_staff = abjad.Score.make_piano_score()
    duration = abjad.Duration(1, 32)

..  abjad::

    pitches = []
    diatonic_pitches = [0, 2, 4, 5, 7, 9, 11]

..  abjad::

    pitches.extend([-24 + x for x in diatonic_pitches])
    pitches.extend([-12 + x for x in diatonic_pitches])
    pitches.extend([0 + x for x in diatonic_pitches])
    pitches.extend([12 + x for x in diatonic_pitches])
    pitches.append(24)
    abjad_configuration.set_default_accidental_spelling('sharps')

..  abjad::

    for pitch in pitches:
        note = abjad.Note(pitch, duration)
        rest = abjad.Rest(duration)
        if 0 <= note.written_pitch.number:
            treble_staff.append(note)
            bass_staff.append(rest)
        else:
            treble_staff.append(rest)
            bass_staff.append(note)
        number = note.written_pitch._get_diatonic_pitch_number()
        markup = markuptools.Markup(str(number), Down)
        abjad.attach(markup, bass_staff[-1])

..  abjad::

    abjad.override(score).beam.transparent = True
    abjad.override(score).time_signature.stencil = False
    abjad.override(score).flag.transparent = True
    abjad.override(score).rest.transparent = True
    abjad.override(score).stem.stencil = False
    abjad.override(score).text_script.staff_padding = 6
    moment = abjad.SchemeMoment((1, 52))
    abjad.setting(score).proportional_notation_duration = moment

..  abjad::

    lilypond_file = abjad.LilyPondFile.new(
        score,
        global_staff_size=15,
        )
    show(lilypond_file)


Accidental abbreviations
------------------------

Abjad abbreviates accidentals like this:

    ======================         ============================
    accidental name                abbreviation
    ======================         ============================
    quarter sharp                  'qs'
    quarter flat                   'qf'
    sharp                          's'
    flat                           'f'
    three-quarters sharp           'tqs'
    three-quarters flat            'tqf'
    double sharp                   'ss'
    double flat                    'ff'
    ======================         ============================


Octave designation
------------------

Abjad designates octaves with both numbers and ticks:

    ===============        =============
    octave notation        tick notation
    ===============        =============
    C7                     c''''
    C6                     c'''
    C5                     c''
    C4                     c'
    C3                     c
    C2                     c,
    C1                     c,,
    ===============        =============


Default accidental spelling
---------------------------

By default Abjad picks between enharmonic equivalents according to
the following table:

    ============================        ====================================
    pitch-class number                  pitch-class name
    ============================        ====================================
    0                                   C
    1                                   C#
    2                                   D
    3                                   Eb
    4                                   E
    5                                   F
    6                                   F#
    7                                   G
    8                                   Gb
    9                                   A
    10                                  Bb
    11                                  B
    ============================        ====================================

You can change the default accidental spelling like this:

..  abjad::

    abjad_configuration.set_default_accidental_spelling('sharps')

Or like this:

..  abjad::

    abjad_configuration.set_default_accidental_spelling('flats')

Or like this:

..  abjad::

    abjad_configuration.set_default_accidental_spelling('mixed')
