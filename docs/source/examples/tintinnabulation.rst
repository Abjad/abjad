Tintinnabulation
================

::

    >>> import copy

This example models the first two pages of Arvo Pärt's *Cantus in Memory of Benjamin
Britten*. First, we generate basic pitches and rhythms for the strings. Then we make
edits to the material by hand. The entire process is encapsulated in a function. The
pitch material is the same for all of the strings: a descending a-minor scale, generally
decorated with dyads. But, each instrument uses a different overall range, with the lower
instrument playing slower than the higher instruments, creating a sort of mensuration
canon. For each instrument, the descending scale is fragmented into what we'll call
"descents." The first descent uses only the first note of that instrument's scale, while
the second descent adds the second note, and the third another. We'll generate as many
descents per instruments as there are pitches in its overall scale.

::

    >>> def make_scalar_descents():
    ...     string = """
    ...         a, b, c d e f g
    ...         a b c' d' e' f' g'
    ...         a' b' c'' d'' e'' f'' g''
    ...         a'' b'' c''' d''' e''' f''' g''' a'''
    ...     """
    ...     gamut = abjad.PitchSegment(string)
    ...     pitch_ranges = {
    ...         "Violin_1": abjad.PitchRange("[C4, A6]"),
    ...         "Violin_2": abjad.PitchRange("[A3, A5]"),
    ...         "Viola": abjad.PitchRange("[E3, A4]"),
    ...         "Cello": abjad.PitchRange("[A2, A3]"),
    ...         "Bass": abjad.PitchRange("[C3, A3]"),
    ...     }
    ...     reservoir = {}
    ...     for name, pitch_range in pitch_ranges.items():
    ...         start = gamut.index(pitch_range.start_pitch)
    ...         stop = gamut.index(pitch_range.stop_pitch)
    ...         pitches = abjad.PitchSegment(reversed(gamut[start : stop + 1]))
    ...         pitch_descents = []
    ...         for i in range(len(pitches)):
    ...             descent = tuple(pitches[: i + 1])
    ...             pitch_descents.append(descent)
    ...         reservoir[name] = tuple(pitch_descents)
    ...     return reservoir

Here are the violin descents:

::

    >>> voice_name_to_descents = make_scalar_descents()
    >>> descents = voice_name_to_descents["Violin_1"]
    >>> for descent in descents:
    ...     string = " ".join(str(_) for _ in descent)
    ...     print(string)

Next we add dyads to all of the descents, except for the viola's. We'll use a dictionary
as a lookup table, to tell us what interval to add below a given pitch class. Nonfinal
descents are treated one way; the final descent in each reservoir is treated another way:

::

    >>> def make_pitch_pair_descents(voice_to_scalar_descents):
    ...     pc_to_shadow_interval = {
    ...         "a": -5,  # add a P4 below
    ...         "g": -3,  # add a m3 below
    ...         "f": -1,  # add a m2 below
    ...         "e": -4,  # add a M3 below
    ...         "d": -2,  # add a M2 below
    ...         "c": -3,  # add a m3 below
    ...         "b": -2,  # add a M2 below
    ...     }
    ...     voice_to_pitch_pair_descents = {}
    ...     for voice_name, scalar_descents in voice_to_scalar_descents.items():
    ...         if voice_name == "Viola":
    ...             voice_to_pitch_pair_descents["Viola"] = scalar_descents
    ...             continue
    ...         pitch_pair_descents = []
    ...         for scalar_descent in scalar_descents[:-1]:
    ...             pitch_pair_descent = []
    ...             for pitch in scalar_descent:
    ...                 pitch_class = str(pitch.pitch_class)
    ...                 shadow_pitch = pitch + pc_to_shadow_interval[pitch_class]
    ...                 pitch_pair = (shadow_pitch, pitch)
    ...                 pitch_pair_descent.append(pitch_pair)
    ...             pitch_pair_descents.append(tuple(pitch_pair_descent))
    ...         final_pitch_pair_descent = []
    ...         for pitch in scalar_descents[-1][:-1]:
    ...             pitch_class = str(pitch.pitch_class)
    ...             shadow_pitch = pitch + pc_to_shadow_interval[pitch_class]
    ...             pitch_pair = (shadow_pitch, pitch)
    ...             final_pitch_pair_descent.append(pitch_pair)
    ...         final_pitch_pair_descent.append(scalar_descents[-1][-1])
    ...         pitch_pair_descents.append(tuple(final_pitch_pair_descent))
    ...         voice_to_pitch_pair_descents[voice_name] = tuple(pitch_pair_descents)
    ...     return voice_to_pitch_pair_descents

Here's what's inside:

::

    >>> voice_to_descents = make_scalar_descents()
    >>> voice_to_descents = make_pitch_pair_descents(voice_to_descents)
    >>> descents = voice_to_descents["Violin_1"]
    >>> for descent in descents[:7]:
    ...     strings = []
    ...     for item in descent:
    ...         if isinstance(item, tuple):
    ...             string = f"({str(item[0])}, {str(item[1])})"
    ...         else:
    ...             string = str(item)
    ...         strings.append(string)
    ...     string = " ".join(strings)
    ...     print(string)

Finally, we'll add rhythms to the pitch contours we've been constructing. Each string
instrument plays twice as slow as the string instrument above it in the score.
Additionally, all the strings start with some rests, and use a long-short pattern for
their rhythms.

::

    >>> def make_chord_descents(voice_to_pitch_pair_descents):
    ...     voice_names = ["Violin_1", "Violin_2", "Viola", "Cello", "Bass"]
    ...     voice_to_descents = {}
    ...     for i, voice_name in enumerate(voice_names):
    ...         long_duration = abjad.Duration(1, 2) * (2 ** i)
    ...         short_duration = long_duration / 2
    ...         rest_duration = abjad.Multiplier(3, 2) * long_duration
    ...         div = rest_duration // abjad.Duration(3, 2)
    ...         mod = rest_duration % abjad.Duration(3, 2)
    ...         initial_rest = []
    ...         for i in range(div):
    ...             rest = abjad.MultimeasureRest((3, 2))
    ...             initial_rest.append(rest)
    ...         if mod:
    ...             rest = abjad.Rest(mod)
    ...             initial_rest.append(rest)
    ...         chord_descents = [tuple(initial_rest)]
    ...         pitch_pair_descents = voice_to_pitch_pair_descents[voice_name]
    ...         durations = [long_duration, short_duration]
    ...         counter = 0
    ...         for pitch_pair_descent in pitch_pair_descents:
    ...             chord_descent = []
    ...             for pitch in pitch_pair_descent:
    ...                 duration = durations[counter]
    ...                 if isinstance(pitch, tuple):
    ...                     chord = abjad.Chord(pitch, duration)
    ...                     chord_descent.append(chord)
    ...                 else:
    ...                     assert isinstance(pitch, abjad.NamedPitch)
    ...                     note = abjad.Note(pitch, duration)
    ...                     chord_descent.append(note)
    ...                 counter = (counter + 1) % 2
    ...             chord_descents.append(tuple(chord_descent))
    ...         voice_to_descents[voice_name] = tuple(chord_descents)
    ...     return voice_to_descents

Let's see what a few of these look like. First we build everything:

::

    >>> voice_to_descents = make_scalar_descents()
    >>> voice_to_descents = make_pitch_pair_descents(voice_to_descents)
    >>> voice_to_descents = make_chord_descents(voice_to_descents)

Here are the first ten violin 1 descents:

::

    >>> descents = voice_to_descents["Violin_1"][:10]
    >>> for i, descent in enumerate(descents):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

    >>> leaves = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(leaves)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

Here are the first ten violin 2 descents:

::

    >>> descents = voice_to_descents["Violin_2"][:10]
    >>> for i, descent in enumerate(descents):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

    >>> leaves = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(leaves)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

Here are the first ten viola descents. They have some longer notes, so we'll split their
music cyclically every 3 half notes, just so nothing crosses the bar lines accidentally:

..  book::
    :lilypond/no-stylesheet:

    >>> descents = voice_to_descents["Viola"][:10]
    >>> for i, descent in enumerate(descents):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

    >>> notes = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(notes)
    >>> selections = abjad.mutate.split(staff[:], [(3, 2)], cyclic=True)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

You can see how each part is twice as slow as the previous, and starts a little bit later
too. 

Now we'll attach dynamics, articulations, bow marks, markup, page breaks and rehearsal
marks.

::

    >>> def add_bell_music(score):
    ...     bell_voice = score["Bell_Voice"]
    ...     strings = 3 * [r"{ r2. a'2. \laissezVibrer }", "{ R1. }"]
    ...     strings.extend(["{ R1. }", "{ R1. }"])
    ...     strings = 11 * strings
    ...     for string in strings:
    ...         bell_voice.append(string)
    ...     strings = 19 * ["{ R1. }"]
    ...     for string in strings:
    ...         bell_voice.append(string)
    ...     bell_voice.append(r"{ a'1. \laissezVibrer }")

    >>> def edit_violin_1(score, voice_to_descents):
    ...     voice = score["Violin_1_Voice"]
    ...     descents = voice_to_descents["Violin_1"]
    ...     container = abjad.Container(descents[-1])
    ...     for duration in 43 * [(6, 4)]:
    ...         note = abjad.Note("c'", duration)
    ...         tie = abjad.Tie()
    ...         abjad.attach(tie, note)
    ...         container.append(note)
    ...     container.extend("c'2 r4 r2.")
    ...     voice.extend(container)

    >>> def edit_violin_2(score, voice_to_descents):
    ...     voice = score["Violin_2_Voice"]
    ...     descents = voice_to_descents["Violin_2"]
    ...     container = abjad.Container(descents[-1])
    ...     container[-1].written_duration = (1, 1)
    ...     container.append("a2")
    ...     for leaf in container:
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, leaf)
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, leaf)
    ...     voice.extend(container)
    ...     string = " ".join(32 * ["a1."]) + " a2"
    ...     container = abjad.Container(string)
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, container[0])
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, container[0])
    ...     for leaf in container[:-1]:
    ...         tie = abjad.Tie()
    ...         abjad.attach(tie, leaf)
    ...     container.extend("r4 r2.")
    ...     voice.extend(container)

    >>> def edit_viola(score, voice_to_descents):
    ...     voice = score["Viola_Voice"]
    ...     descents = voice_to_descents["Viola"]
    ...     container = abjad.Container(descents[-1])
    ...     for leaf in container:
    ...         if leaf.written_duration == abjad.Duration(4, 4):
    ...             leaf.written_duration = (8, 4)
    ...         else:
    ...             leaf.written_duration = (4, 4)
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, leaf)
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, leaf)
    ...     container.append("e1")
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, container[-1])
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, container[-1])
    ...     container.append("e1.")
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, container[-1])
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, container[-1])
    ...     tie = abjad.Tie()
    ...     abjad.attach(tie, container[-1])
    ...     for duration in 20 * [(6, 4)]:
    ...         note = abjad.Note("e", duration)
    ...         tie = abjad.Tie()
    ...         abjad.attach(tie, note)
    ...         container.append(note)
    ...     container.extend("e2 r4 r2.")
    ...     voice.extend(container)

    >>> def edit_cello(score, voice_to_descents):
    ...     voice = score["Cello_Voice"]
    ...     logical_tie = abjad.select(voice[-1]).logical_tie()
    ...     for leaf in logical_tie:
    ...         chord = abjad.Chord(["e,", "a,"], leaf.written_duration)
    ...         abjad.mutate.replace(leaf, chord)
    ...     descents = voice_to_descents["Cello"]
    ...     descent = descents[-1]
    ...     voice.extend(descent)
    ...     for chord in descent:
    ...         if isinstance(chord, abjad.Note):
    ...             continue
    ...         pitch = chord.written_pitches[1]
    ...         note = abjad.Note(pitch, chord.written_duration)
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, note)
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, note)
    ...         abjad.mutate.replace(chord, note)
    ...     voice.extend("a,1. ~ a,2")
    ...     voice.extend("b,1 ~ b,1. ~ b,1.")
    ...     voice.extend("a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2")
    ...     voice.extend("r4 r2.")

    >>> def edit_bass(score, voice_to_descents):
    ...     string = r"<e, e>1. ~ <e, e>1. ~ <e, e>1 ~ <e, e>2 ~"
    ...     string += r" <e, e>1. ~ <e, e>1. ~ <e, e>2"
    ...     string += r" <d, d>\longa <c, c>\maxima"
    ...     string += r" <b,>\longa <a,>\maxima r4 r2."
    ...     score["Bass_Voice"][-3:] = string


    >>> def add_string_music(score):
    ...     voice_to_descents = make_scalar_descents()
    ...     voice_to_descents = make_pitch_pair_descents(voice_to_descents)
    ...     voice_to_descents = make_chord_descents(voice_to_descents)
    ...     for name, descents in voice_to_descents.items():
    ...         instrument_voice = score["%s_Voice" % name]
    ...         instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
    ...         for descent in descents:
    ...             instrument_voice.extend(descent)
    ...     extra_components = make_scalar_descents()
    ...     extra_components = make_pitch_pair_descents(extra_components)
    ...     extra_components = make_chord_descents(extra_components)
    ...     edit_violin_1(score, extra_components)
    ...     edit_violin_2(score, extra_components)
    ...     edit_viola(score, extra_components)
    ...     edit_cello(score, extra_components)
    ...     edit_bass(score, extra_components)
    ...     strings_staff_group = score["Strings_Staff_Group"]
    ...     for voice in abjad.select(strings_staff_group).components(abjad.Voice):
    ...         selections = abjad.mutate.split(voice[:], [(6, 4)], cyclic=True)
    ...         for selection in selections:
    ...             container = abjad.Container()
    ...             abjad.mutate.wrap(selection, container)

    >>> rebow_string = r"""\markup \concat {
    ...     \musicglyph "scripts.downbow" \hspace #1 \musicglyph "scripts.upbow"
    ... }"""

    >>> def attach_bow_marks(score):
    ...     for measure in score["Violin_1_Voice"][7 - 1 : 9 - 1]:
    ...         chords = abjad.select(measure).components(abjad.Chord)
    ...         for i, chord in enumerate(chords):
    ...             if i % 2 == 0:
    ...                 articulation = abjad.Articulation("downbow")
    ...             else:
    ...                 articulation = abjad.Articulation("upbow")
    ...             abjad.attach(articulation, chord)
    ...     markup = abjad.Markup(rebow_string, literal=True)
    ...     abjad.attach(markup, score["Violin_1_Voice"][65 - 1][0])
    ...     markup = abjad.Markup(rebow_string, literal=True)
    ...     abjad.attach(markup, score["Violin_2_Voice"][76 - 1][0])
    ...     markup = abjad.Markup(rebow_string, literal=True)
    ...     abjad.attach(markup, score["Viola_Voice"][87 - 1][0])

    >>> def attach_dynamics(score):
    ...     voice = score["Bell_Voice"]
    ...     dynamic = abjad.Dynamic("ppp")
    ...     abjad.attach(dynamic, voice[0][1])
    ...     dynamic = abjad.Dynamic("pp")
    ...     abjad.attach(dynamic, voice[8][1])
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[18][1])
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[26][1])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[34][1])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[42][1])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[52][1])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[60][1])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[68][1])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[76][1])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[84][1])
    ...     dynamic = abjad.Dynamic("pp")
    ...     abjad.attach(dynamic, voice[-1][0])
    ...     # first violin
    ...     voice = score["Violin_1_Voice"]
    ...     dynamic = abjad.Dynamic("ppp")
    ...     abjad.attach(dynamic, voice[6][1])
    ...     dynamic = abjad.Dynamic("pp")
    ...     abjad.attach(dynamic, voice[15][0])
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[22][3])
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[31][0])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[38][3])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[47][0])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[55][2])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[62][2])
    ...     # second violin
    ...     voice = score["Violin_2_Voice"]
    ...     dynamic = abjad.Dynamic("pp")
    ...     abjad.attach(dynamic, voice[7][0])
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[12][0])
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[16][0])
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[25][1])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[34][1])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[44][1])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[54][0])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[62][1])
    ...     # viola
    ...     voice = score["Viola_Voice"]
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[8][0])
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[19][1])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[30][0])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[36][0])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[42][0])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[52][0])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[62][0])
    ...     # cello
    ...     voice = score["Cello_Voice"]
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, voice[10][0])
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[21][0])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[31][0])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[43][0])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[52][1])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[62][0])
    ...     # bass
    ...     voice = score["Bass_Voice"]
    ...     dynamic = abjad.Dynamic("mp")
    ...     abjad.attach(dynamic, voice[14][0])
    ...     dynamic = abjad.Dynamic("mf")
    ...     abjad.attach(dynamic, voice[27][0])
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, voice[39][0])
    ...     dynamic = abjad.Dynamic("ff")
    ...     abjad.attach(dynamic, voice[51][0])
    ...     dynamic = abjad.Dynamic("fff")
    ...     abjad.attach(dynamic, voice[62][0])

    >>> def handle_markup_commands(score, commands):
    ...     for command in commands:
    ...         voice_name, measure_index, leaf_index, string = command[:4]
    ...         if len(command) == 5:
    ...             direction = command[4]
    ...         else:
    ...             direction = abjad.Up
    ...         voice_name = voice_name + "_Voice"
    ...         voice = score[voice_name]
    ...         string = r"\markup " + string
    ...         markup = abjad.Markup(string, direction=direction, literal=True)
    ...         abjad.attach(markup, voice[measure_index][leaf_index])

    >>> def attach_page_breaks(score, measure_indices):
    ...     bell_voice = score["Bell_Voice"]
    ...     for measure_index in measure_indices:
    ...         command = abjad.LilyPondLiteral(r"\break", "after")
    ...         abjad.attach(command, bell_voice[measure_index])

    >>> def attach_rehearsal_marks(score):
    ...     bell_voice = score["Bell_Voice"]
    ...     measure_indices = [
    ...         6,
    ...         12,
    ...         18,
    ...         24,
    ...         30,
    ...         36,
    ...         42,
    ...         48,
    ...         54,
    ...         60,
    ...         66,
    ...         72,
    ...         78,
    ...         84,
    ...         90,
    ...         96,
    ...         102,
    ...     ]
    ...     for measure_index in measure_indices:
    ...         command = abjad.LilyPondLiteral(r"\mark \default", "before")
    ...         abjad.attach(command, bell_voice[measure_index])

    >>> def attach_upper_context_indicators(score):
    ...     leaf = abjad.select(score["Bell_Staff"]).leaf(0)
    ...     metronome_mark = abjad.MetronomeMark((1, 4), (112, 120))
    ...     abjad.attach(metronome_mark, leaf)
    ...     time_signature = abjad.TimeSignature((6, 4))
    ...     abjad.attach(time_signature, leaf)
    ...     instrument = abjad.Instrument(pitch_range="[C4, C6]")
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup "Campana (La)"'
    ...     string = rf'\set Staff.instrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     string = r'\markup \hcenter-in #8 "Camp."'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Violin_1_Staff"]).leaf(0)
    ...     instrument = abjad.Violin()
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup \hcenter-in #8 "Vn. I"'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Violin_2_Staff"]).leaf(0)
    ...     instrument = abjad.Violin()
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup \hcenter-in #8 "Vn. II"'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Viola_Staff"]).leaf(0)
    ...     instrument = abjad.Viola()
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup \hcenter-in #8 "Va."'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("alto")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Cello_Staff"]).leaf(0)
    ...     instrument = abjad.Cello()
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup \hcenter-in #8 "Vc."'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Bass_Staff"]).leaf(0)
    ...     instrument = abjad.Contrabass()
    ...     abjad.attach(instrument, leaf)
    ...     string = r'\markup \hcenter-in #8 "Cb."'
    ...     string = rf'\set Staff.shortInstrumentName = {string}'
    ...     literal = abjad.LilyPondLiteral(string)
    ...     abjad.attach(literal, leaf)
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, leaf)
    ...     leaf = abjad.select(score["Bass_Staff"]).leaf(-1)
    ...     bar_line = abjad.BarLine("|.")
    ...     abjad.attach(bar_line, leaf)

::

    >>> def make_empty_score():
    ...     bell_voice = abjad.Voice(name="Bell_Voice")
    ...     bell_staff = abjad.Staff([bell_voice], name="Bell_Staff")
    ...     violin_1_voice = abjad.Voice(name="Violin_1_Voice")
    ...     violin_1_staff = abjad.Staff([violin_1_voice], name="Violin_1_Staff")
    ...     violin_2_voice = abjad.Voice(name="Violin_2_Voice")
    ...     violin_2_staff = abjad.Staff([violin_2_voice], name="Violin_2_Staff")
    ...     viola_voice = abjad.Voice(name="Viola_Voice")
    ...     viola_staff = abjad.Staff([viola_voice], name="Viola_Staff")
    ...     cello_voice = abjad.Voice(name="Cello_Voice")
    ...     cello_staff = abjad.Staff([cello_voice], name="Cello_Staff")
    ...     bass_voice = abjad.Voice(name="Bass_Voice")
    ...     bass_staff = abjad.Staff([bass_voice], name="Bass_Staff")
    ...     staves = [
    ...         violin_1_staff, violin_2_staff, viola_staff, cello_staff, bass_staff
    ...     ]
    ...     strings_staff_group = abjad.StaffGroup(staves, name="Strings_Staff_Group")
    ...     score = abjad.Score([bell_staff, strings_staff_group], name="Score")
    ...     return score

::

    >>> def make_lilypond_file(preamble, breaks, markup_commands):
    ...     score = make_empty_score()
    ...     add_bell_music(score)
    ...     add_string_music(score)
    ...     attach_bow_marks(score)
    ...     attach_dynamics(score)
    ...     handle_markup_commands(score, markup_commands)
    ...     attach_page_breaks(score, breaks)
    ...     attach_rehearsal_marks(score)
    ...     attach_upper_context_indicators(score)
    ...     lilypond_file = abjad.LilyPondFile(items=[preamble, score])
    ...     return lilypond_file
    
::

    >>> preamble =r"""#(set-global-staff-size 8)
    ... 
    ... \header {
    ...     tagline = ##f
    ...     composer = \markup { "Arvo Pärt" }
    ...     title = \markup { "Cantus in Memory of Benjamin Britten (1980)" }
    ... }
    ... 
    ... \layout {
    ...     \context {
    ...         \Staff
    ...         \RemoveEmptyStaves
    ...         \override VerticalAxisGroup.remove-first = ##t
    ...     }
    ...     \context {
    ...         \Score
    ...         \override StaffGrouper.staff-staff-spacing = #'(
    ...             (basic-distance . 0) (minimum-distance . 0)
    ...             (padding . 8) (stretchability . 0))
    ...         \override StaffSymbol.thickness = #0.5
    ...         \override VerticalAxisGroup.staff-staff-spacing = #'(
    ...             (basic-distance . 0) (minimum-distance . 0)
    ...             (padding . 8) (stretchability . 0))
    ...         markFormatter = #format-mark-box-numbers
    ...     }
    ... }
    ... 
    ... \paper {
    ...     system-separator-markup = #slashSeparator
    ...     bottom-margin = 0.5\in
    ...     top-margin = 0.5\in
    ...     left-margin = 0.75\in
    ...     right-margin = 0.5\in
    ...     paper-width = 5.25\in
    ...     paper-height = 7.25\in
    ... }"""

Finally, we make commands and create the score:

::

    >>> markup_commands = (
    ...     ("Violin_1", 6, 1, r"\left-column { div. \line { con sord. } }"),
    ...     ("Violin_1", 8, 0, "sim."),
    ...     ("Violin_1", 58, 3, "uniti"),
    ...     ("Violin_1", 59, 0, "div."),
    ...     ("Violin_1", 63, 3, "uniti"),
    ...     ("Violin_2", 7, 0, "div."),
    ...     ("Violin_2", 66, 1, "uniti"),
    ...     ("Violin_2", 67, 0, "div."),
    ...     ("Violin_2", 74, 0, "uniti"),
    ...     ("Viola", 8, 0, "sole"),
    ...     ("Cello", 10, 0, "div."),
    ...     ("Cello", 74, 0, "uniti"),
    ...     ("Cello", 84, 1, "uniti"),
    ...     ("Cello", 86, 0, r"\italic { espr. }", abjad.Down),
    ...     ("Cello", 88, 1, r"\italic { molto espr. }", abjad.Down),
    ...     ("Bass", 14, 0, "div."),
    ...     ("Bass", 86, 0, r"\italic { espr. }", abjad.Down),
    ...     ("Bass", 88, 1, r"\italic { molto espr. }", abjad.Down),
    ...     ("Bass", 99, 1, "uniti"),
    ...     ("Violin_1", 102, 0, r"\italic { (non dim.) }", abjad.Down),
    ...     ("Violin_2", 102, 0, r"\italic { (non dim.) }", abjad.Down),
    ...     ("Viola", 102, 0, r"\italic { (non dim.) }", abjad.Down),
    ...     ("Cello", 102, 0, r"\italic { (non dim.) }", abjad.Down),
    ...     ("Bass", 102, 0, r"\italic { (non dim.) }", abjad.Down),
    ... )

    >>> breaks = []
    >>> breaks.extend([5, 10, 15, 20, 25, 30, 35, 40, 45])
    >>> breaks.extend([50, 55, 60, 65, 72, 79, 86, 93, 100])

..  book::
    :lilypond/no-stylesheet:
    :lilypond/pages: 1-10
    :lilypond/with-columns: 2

    >>> lilypond_file = make_lilypond_file(preamble, breaks, markup_commands)
    >>> abjad.show(lilypond_file)

:author:`[Treviño (2.19), Bača (3.2). From Arvo Pärt's Cantus In Memoriam Benjamin
Britten (1980).]`
