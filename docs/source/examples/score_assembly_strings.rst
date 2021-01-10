Score reproduction
==================

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

    >>> def create_pitch_contour_reservoir():
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

Here's what the first 10 descents for the first violin look like:

::

    >>> reservoir = create_pitch_contour_reservoir()
    >>> len(reservoir["Violin_1"])

    >>> for i in range(10):
    ...     descent = reservoir["Violin_1"][i]
    ...     string = " ".join(str(x) for x in descent)
    ...     print(string)
    ...

Next we add dyads to all of the descents, except for the viola's. We'll use a dictionary
as a lookup table, to tell us what interval to add below a given pitch class.

::

    >>> def shadow_pitch_contour_reservoir(pitch_contour_reservoir):
    ...     shadow_pitch_lookup = {
    ...         abjad.NamedPitchClass("a"): -5,  # add a P4 below
    ...         abjad.NamedPitchClass("g"): -3,  # add a m3 below
    ...         abjad.NamedPitchClass("f"): -1,  # add a m2 below
    ...         abjad.NamedPitchClass("e"): -4,  # add a M3 below
    ...         abjad.NamedPitchClass("d"): -2,  # add a M2 below
    ...         abjad.NamedPitchClass("c"): -3,  # add a m3 below
    ...         abjad.NamedPitchClass("b"): -2,  # add a M2 below
    ...     }
    ...     shadowed_reservoir = {}
    ...     for name, pitch_contours in pitch_contour_reservoir.items():
    ...         # The viola does not receive any dyads
    ...         if name == "Viola":
    ...             shadowed_reservoir["Viola"] = pitch_contours
    ...             continue
    ...         shadowed_pitch_contours = []
    ...         for pitch_contour in pitch_contours[:-1]:
    ...             shadowed_pitch_contour = []
    ...             for pitch in pitch_contour:
    ...                 pitch_class = pitch.pitch_class
    ...                 shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
    ...                 dyad = (shadow_pitch, pitch)
    ...                 shadowed_pitch_contour.append(dyad)
    ...             shadowed_pitch_contours.append(tuple(shadowed_pitch_contour))
    ...         # treat the final contour differently: the last note does not become a dyad
    ...         final_shadowed_pitch_contour = []
    ...         for pitch in pitch_contours[-1][:-1]:
    ...             pitch_class = pitch.pitch_class
    ...             shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
    ...             dyad = (shadow_pitch, pitch)
    ...             final_shadowed_pitch_contour.append(dyad)
    ...         final_shadowed_pitch_contour.append(pitch_contours[-1][-1])
    ...         shadowed_pitch_contours.append(tuple(final_shadowed_pitch_contour))
    ...         shadowed_reservoir[name] = tuple(shadowed_pitch_contours)
    ...     return shadowed_reservoir

Finally, we'll add rhythms to the pitch contours we've been constructing. Each string
instrument plays twice as slow as the string instrument above it in the score.
Additionally, all the strings start with some rests, and use a long-short pattern for
their rhythms.

::

    >>> def durate_pitch_contour_reservoir(pitch_contour_reservoir):
    ...     names = ["Violin_1", "Violin_2", "Viola", "Cello", "Bass"]
    ...     durated_reservoir = {}
    ...     for i, name in enumerate(names):
    ...         long_duration = abjad.Duration(1, 2) * pow(2, i)
    ...         short_duration = long_duration / 2
    ...         rest_duration = abjad.Multiplier(3, 2) * long_duration
    ...         div = rest_duration // abjad.Duration(3, 2)
    ...         mod = rest_duration % abjad.Duration(3, 2)
    ...         initial_rest = []
    ...         for i in range(div):
    ...             rest = abjad.MultimeasureRest((3, 2))
    ...             initial_rest.append(rest)
    ...         maker = abjad.LeafMaker()
    ...         if mod:
    ...             initial_rest += maker([None], mod)
    ...         durated_contours = [tuple(initial_rest)]
    ...         pitch_contours = pitch_contour_reservoir[name]
    ...         durations = [long_duration, short_duration]
    ...         counter = 0
    ...         maker = abjad.LeafMaker()
    ...         for pitch_contour in pitch_contours:
    ...             contour = []
    ...             for pitch in pitch_contour:
    ...                 leaves = maker([pitch], [durations[counter]])
    ...                 contour.extend(leaves)
    ...                 counter = (counter + 1) % 2
    ...             durated_contours.append(tuple(contour))
    ...         durated_reservoir[name] = tuple(durated_contours)
    ...     return durated_reservoir

Let's see what a few of those look like. First, we'll build the entire reservoir from
scratch, to demonstrate the process:

::

    >>> reservoir = create_pitch_contour_reservoir()
    >>> shadowed_reservoir = shadow_pitch_contour_reservoir(reservoir)
    >>> durated_reservoir = durate_pitch_contour_reservoir(shadowed_reservoir)

Then we'll grab the subreservoir for the first violins, taking the first ten descents
(which includes the silences we've been adding as well). We'll label each descent with
some markup, to distinguish them, throw them into a Staff and give them a 6/4 time
signature, just so they line up properly.

::

    >>> descents = durated_reservoir["Violin_1"][:10]
    >>> for i, descent in enumerate(descents[1:], 1):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

..  book::
    :lilypond/no-stylesheet:

    >>> notes = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(notes)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

Let's look at the second violins too:

::

    >>> descents = durated_reservoir["Violin_2"][:10]
    >>> for i, descent in enumerate(descents[1:], 1):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

..  book::
    :lilypond/no-stylesheet:

    >>> notes = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(notes)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

And, last we'll take a peek at the violas. They have some longer notes, so we'll split
their music cyclically every 3 half notes, just so nothing crosses the bar lines
accidentally:

::

    >>> descents = durated_reservoir["Viola"][:10]
    >>> for i, descent in enumerate(descents[1:], 1):
    ...     string = rf"\markup \rounded-box \bold {i}"
    ...     markup = abjad.Markup(string, direction=abjad.Up, literal=True)
    ...     abjad.attach(markup, descent[0])
    ...

..  book::
    :lilypond/no-stylesheet:

    >>> notes = abjad.sequence(descents).flatten()
    >>> staff = abjad.Staff(notes)
    >>> shards = abjad.mutate.split(staff[:], [(3, 2)], cyclic=True)
    >>> time_signature = abjad.TimeSignature((6, 4))
    >>> leaf = abjad.select(staff).leaf(0)
    >>> abjad.attach(time_signature, leaf)
    >>> abjad.show(staff)

You can see how each part is twice as slow as the previous, and starts a little bit later
too. 

Now we'll attach dynamics, articulations, bow markings, markup, page breaks and rehearsal
marks.

We'll start with the bow marks. This involves creating a piece of custom markup. We then
copy the markup and attach copies where we want them in the score. Why make copies of the
markup?  An indicator can only be attached to one note at a time. If we attach the
original markup to each note in turn, only the last note will receive the markup; the
markup will be automatically detached from the preceding notes. We attach dynamics and
expressive marks directly. We attach rehearsal marks and LilyPond line breaks to match
the layout of the original.

::

    >>> def make_bell_phrase():
    ...     phrase = []
    ...     for _ in range(3):
    ...         measure = abjad.Container("r2. a'2.")
    ...         abjad.attach(abjad.TimeSignature((6, 4)), measure[0])
    ...         abjad.attach(abjad.LaissezVibrer(), measure[-1])
    ...         phrase.append(measure)
    ...         phrase.append(abjad.Container("R1."))
    ...     for _ in range(2):
    ...         phrase.append(abjad.Container("R1."))
    ...     return phrase


    >>> def add_bell_music_to_score(score):
    ...     bell_voice = score["Bell_Voice"]
    ...     for _ in range(11):
    ...         bell_voice.extend(make_bell_phrase())
    ...     for _ in range(19):
    ...         bell_voice.append(abjad.Container("R1."))
    ...     measure = abjad.Container(r"a'1.")
    ...     abjad.attach(abjad.LaissezVibrer(), measure[-1])
    ...     bell_voice.append(measure)


    >>> def add_string_music_to_score(score):
    ...     # generate some pitch and rhythm information
    ...     pitch_contour_reservoir = create_pitch_contour_reservoir()
    ...     shadowed_contour_reservoir = shadow_pitch_contour_reservoir(pitch_contour_reservoir)
    ...     durated_reservoir = durate_pitch_contour_reservoir(shadowed_contour_reservoir)
    ...     # add six dotted-whole notes and the durated contours to each string voice
    ...     for name, descents in durated_reservoir.items():
    ...         instrument_voice = score["%s_Voice" % name]
    ...         instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
    ...         for descent in descents:
    ...             instrument_voice.extend(descent)
    ...     # apply instrument-specific edits
    ...     edit_violin_1_voice(score, durated_reservoir)
    ...     edit_violin_2_voice(score, durated_reservoir)
    ...     edit_viola_voice(score, durated_reservoir)
    ...     edit_cello_voice(score, durated_reservoir)
    ...     edit_bass_voice(score, durated_reservoir)
    ...     # chop all string parts into 6/4 measures
    ...     strings_staff_group = score["Strings_Staff_Group"]
    ...     # NOTE: this takes a long time:
    ...     for voice in abjad.select(strings_staff_group).components(abjad.Voice):
    ...         shards = abjad.mutate.split(voice[:], [(6, 4)], cyclic=True)
    ...         for shard in shards:
    ...             container = abjad.Container()
    ...             abjad.mutate.wrap(shard, container)


    >>> def edit_violin_1_voice(score, durated_reservoir):
    ...     voice = score["Violin_1_Voice"]
    ...     descents = durated_reservoir["Violin_1"]
    ...     last_descent = abjad.Selection(descents[-1])
    ...     copied_descent = abjad.mutate.copy(last_descent)
    ...     voice.extend(copied_descent)
    ...     final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    ...     maker = abjad.NoteMaker()
    ...     final_sustain_notes = maker(["c'"], final_sustain_rhythm)
    ...     voice.extend(final_sustain_notes)
    ...     abjad.tie(final_sustain_notes)
    ...     voice.extend("r4 r2.")


    >>> def edit_violin_2_voice(score, durated_reservoir):
    ...     voice = score["Violin_2_Voice"]
    ...     descents = durated_reservoir["Violin_2"]
    ...     last_descent = abjad.Selection(descents[-1])
    ...     copied_descent = abjad.mutate.copy(last_descent)
    ...     copied_descent = list(copied_descent)
    ...     copied_descent[-1].written_duration = abjad.Duration(1, 1)
    ...     copied_descent.append(abjad.Note("a2"))
    ...     for leaf in copied_descent:
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, leaf)
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, leaf)
    ...     voice.extend(copied_descent)
    ...     final_sustain = []
    ...     for _ in range(32):
    ...         final_sustain.append(abjad.Note("a1."))
    ...     final_sustain.append(abjad.Note("a2"))
    ...     final_sustain = abjad.Selection(final_sustain)
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, final_sustain[0])
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, final_sustain[0])
    ...     voice.extend(final_sustain)
    ...     abjad.tie(final_sustain)
    ...     voice.extend("r4 r2.")


    >>> def edit_viola_voice(score, durated_reservoir):
    ...     voice = score["Viola_Voice"]
    ...     descents = durated_reservoir["Viola"]
    ...     for leaf in descents[-1]:
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, leaf)
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, leaf)
    ...     last_descent = abjad.Selection(descents[-1])
    ...     copied_descent = abjad.mutate.copy(last_descent)
    ...     for leaf in copied_descent:
    ...         if leaf.written_duration == abjad.Duration(4, 4):
    ...             leaf.written_duration = abjad.Duration(8, 4)
    ...         else:
    ...             leaf.written_duration = abjad.Duration(4, 4)
    ...     voice.extend(copied_descent)
    ...     bridge = abjad.Note("e1")
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, bridge)
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, bridge)
    ...     voice.append(bridge)
    ...     final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    ...     maker = abjad.NoteMaker()
    ...     final_sustain_notes = maker(["e"], final_sustain_rhythm)
    ...     articulation = abjad.Articulation("accent")
    ...     abjad.attach(articulation, final_sustain_notes[0])
    ...     articulation = abjad.Articulation("tenuto")
    ...     abjad.attach(articulation, final_sustain_notes[0])
    ...     voice.extend(final_sustain_notes)
    ...     abjad.tie(final_sustain_notes)
    ...     voice.extend("r4 r2.")


    >>> def edit_cello_voice(score, durated_reservoir):
    ...     voice = score["Cello_Voice"]
    ...     descents = durated_reservoir["Cello"]
    ...     logical_tie = abjad.select(voice[-1]).logical_tie()
    ...     for leaf in logical_tie.leaves:
    ...         parent = abjad.get.parentage(leaf).parent
    ...         index = parent.index(leaf)
    ...         parent[index] = abjad.Chord(["e,", "a,"], leaf.written_duration)
    ...     selection = voice[-len(descents[-1]) :]
    ...     unison_descent = abjad.mutate.copy(selection)
    ...     voice.extend(unison_descent)
    ...     for chord in unison_descent:
    ...         index = abjad.get.parentage(chord).parent.index(chord)
    ...         parent[index] = abjad.Note(chord.written_pitches[1], chord.written_duration)
    ...         articulation = abjad.Articulation("accent")
    ...         abjad.attach(articulation, parent[index])
    ...         articulation = abjad.Articulation("tenuto")
    ...         abjad.attach(articulation, parent[index])
    ...     voice.extend("a,1. ~ a,2")
    ...     voice.extend("b,1 ~ b,1. ~ b,1.")
    ...     voice.extend("a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2")
    ...     voice.extend("r4 r2.")

    >>> def edit_bass_voice(score, durated_reservoir):
    ...     string = r"<e, e>1. ~ <e, e>1. ~ <e, e>1 ~ <e, e>2 ~"
    ...     string += r" <e, e>1. ~ <e, e>1. ~ <e, e>2"
    ...     string += r" <d, d>\longa <c, c>\maxima"
    ...     string += r" <b,>\longa <a,>\maxima r4 r2."
    ...     score["Bass_Voice"][-3:] = string

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

    >>> def attach_markup_commands(score, commands):
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

    >>> def attach_final_bar_lines(score):
    ...     last_leaf = abjad.select(score).leaf(-1)
    ...     bar_line = abjad.BarLine("|.")
    ...     abjad.attach(bar_line, last_leaf)


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


    >>> def configure_score(score):
    ...     # configure bell staff
    ...     bell_staff = score["Bell_Staff"]
    ...     leaf = abjad.select(bell_staff).leaf(0)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     bells = abjad.Instrument(
    ...         name="Campana in La", short_name="Camp.", pitch_range="[C4, C6]"
    ...     )
    ...     abjad.attach(bells, leaf)
    ...     mark = abjad.MetronomeMark((1, 4), (112, 120))
    ...     abjad.attach(mark, leaf)
    ...     # time_signature = abjad.TimeSignature((6, 4))
    ...     # abjad.attach(time_signature, leaf)
    ...     # configure first violin staff
    ...     violin_1_staff = score["Violin_1_Staff"]
    ...     leaf = abjad.select(violin_1_staff).leaf(0)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     violin = abjad.Violin(
    ...         markup=abjad.Markup("Violin I"), short_markup=abjad.Markup("Vl. I")
    ...     )
    ...     abjad.attach(violin, leaf)
    ...     # configure second violin staff
    ...     violin_2_staff = score["Violin_2_Staff"]
    ...     leaf = abjad.select(violin_2_staff).leaf(0)
    ...     clef = abjad.Clef("treble")
    ...     abjad.attach(clef, leaf)
    ...     violin = abjad.Violin(
    ...         markup=abjad.Markup("Violin II"), short_markup=abjad.Markup("Vl. II")
    ...     )
    ...     abjad.attach(violin, leaf)
    ...     # configure viola staff
    ...     leaf = abjad.select(score["Viola_Staff"]).leaf(0)
    ...     clef = abjad.Clef("alto")
    ...     abjad.attach(clef, leaf)
    ...     viola = abjad.Viola()
    ...     abjad.attach(viola, leaf)
    ...     # configure cello staff
    ...     leaf = abjad.select(score["Cello_Staff"]).leaf(0)
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, leaf)
    ...     cello = abjad.Cello()
    ...     abjad.attach(cello, leaf)
    ...     # configure bass staff
    ...     leaf = abjad.select(score["Bass_Staff"]).leaf(0)
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, leaf)
    ...     contrabass = abjad.Contrabass(short_markup=abjad.Markup("Cb."))
    ...     abjad.attach(contrabass, leaf)
    ...     # configure score
    ...     vector = abjad.SpacingVector(0, 0, 8, 0)
    ...     abjad.override(score).vertical_axis_group.staff_staff_spacing = vector
    ...     abjad.override(score).staff_grouper.staff_staff_spacing = vector
    ...     abjad.override(score).staff_symbol.thickness = 0.5
    ...     scheme = abjad.Scheme("format-mark-box-numbers")
    ...     abjad.setting(score).mark_formatter = scheme

::

    >>> def configure_lilypond_file(lilypond_file):
    ...     lilypond_file._global_staff_size = 8
    ...     context_block = abjad.ContextBlock(source_lilypond_type=r"Staff \RemoveEmptyStaves")
    ...     abjad.override(context_block).vertical_axis_group.remove_first = True
    ...     lilypond_file.layout_block.items.append(context_block)
    ...     lilypond_file.paper_block.system_separator_markup = "slashSeparator"
    ...     bottom_margin = abjad.LilyPondDimension(0.5, "in")
    ...     lilypond_file.paper_block.bottom_margin = bottom_margin
    ...     top_margin = abjad.LilyPondDimension(0.5, "in")
    ...     lilypond_file.paper_block.top_margin = top_margin
    ...     left_margin = abjad.LilyPondDimension(0.75, "in")
    ...     lilypond_file.paper_block.left_margin = left_margin
    ...     right_margin = abjad.LilyPondDimension(0.5, "in")
    ...     lilypond_file.paper_block.right_margin = right_margin
    ...     paper_width = abjad.LilyPondDimension(5.25, "in")
    ...     lilypond_file.paper_block.paper_width = paper_width
    ...     paper_height = abjad.LilyPondDimension(7.25, "in")
    ...     lilypond_file.paper_block.paper_height = paper_height
    ...     lilypond_file.header_block.composer = abjad.Markup("Arvo Pärt")
    ...     title = "Cantus in Memory of Benjamin Britten (1980)"
    ...     lilypond_file.header_block.title = abjad.Markup(title)

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

    >>> def make_lilypond_file(breaks, markup_commands):
    ...     score = make_empty_score()
    ...     add_bell_music_to_score(score)
    ...     add_string_music_to_score(score)
    ...     attach_bow_marks(score)
    ...     attach_dynamics(score)
    ...     attach_markup_commands(score, markup_commands)
    ...     attach_page_breaks(score, breaks)
    ...     attach_rehearsal_marks(score)
    ...     attach_final_bar_lines(score)
    ...     configure_score(score)
    ...     lilypond_file = abjad.LilyPondFile.new(score)
    ...     configure_lilypond_file(lilypond_file)
    ...     return lilypond_file

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

    >>> lilypond_file = make_lilypond_file(breaks, markup_commands)
    >>> abjad.show(lilypond_file)

:author:`[Treviño (2.19), Bača (3.2)]`
