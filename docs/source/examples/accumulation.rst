Accumulation, of cells
======================

::

    >>> import math

This example demonstrates one way of modeling composition as an accumulation of musical
cells. The piece that concerns us here is "Désordre" (1986) from the first book of György
Ligeti's piano etudes. We'll model the first two systems of the score. We model each cell
as two voices inside a simultaneous container. The top voice will hold the octave. The
lower voice will hold the eighth-note run:

.. image :: images/desordre.png

The functions we'll use:

::

    >>> def make_desordre_cell(pitches, hand):
    ...     pitches = pitches.split()
    ...     notes = [abjad.Note(pitch, (1, 8)) for pitch in pitches]
    ...     rh_lower_voice = abjad.Voice(notes, name=f"{hand}_Lower_Voice")
    ...     abjad.beam(notes)
    ...     abjad.slur(notes)
    ...     dynamic = abjad.Dynamic("f")
    ...     abjad.attach(dynamic, notes[0])
    ...     dynamic = abjad.Dynamic("p")
    ...     abjad.attach(dynamic, notes[1])
    ...     literal = abjad.LilyPondLiteral(r"\voiceTwo")
    ...     abjad.attach(literal, notes[0])
    ...     numerator = int(math.ceil(len(pitches) / 2.0))
    ...     duration = (numerator, 8)
    ...     lower_pitch = abjad.NamedPitch(pitches[0])
    ...     upper_pitch = lower_pitch + abjad.NamedInterval("P8")
    ...     octave_pitches = [lower_pitch, upper_pitch]
    ...     chord = abjad.Chord(octave_pitches, duration)
    ...     articulation = abjad.Articulation(">")
    ...     abjad.attach(articulation, chord)
    ...     literal = abjad.LilyPondLiteral(r"\voiceOne")
    ...     abjad.attach(literal, chord)
    ...     rh_upper_voice = abjad.Voice([chord], name=f"{hand}_Upper_Voice")
    ...     voices = [rh_lower_voice, rh_upper_voice]
    ...     container = abjad.Container(voices, simultaneous=True)
    ...     for leaf in rh_lower_voice[:-1]:
    ...         bar_line = abjad.BarLine("")
    ...         abjad.attach(bar_line, leaf)
    ...     return container

::

    >>> def make_desordre_measure(pitches, hand):
    ...     measure = abjad.Container()
    ...     duration = 0
    ...     sublists = pitches.split("|")
    ...     for sublist in sublists:
    ...         container = make_desordre_cell(sublist, hand)
    ...         duration += abjad.get.duration(container)
    ...         measure.append(container)
    ...     duration = duration.with_denominator(8)
    ...     time_signature = abjad.TimeSignature(duration)
    ...     first_note = abjad.select(measure).note(0)
    ...     abjad.attach(time_signature, first_note)
    ...     return measure

::

    >>> def make_desordre_staff(pitches, hand):
    ...     staff = abjad.Staff(name=f"{hand}_Staff")
    ...     for sequence in pitches:
    ...         measure = make_desordre_measure(sequence, hand)
    ...         staff.append(measure)
    ...     return staff

::

    >>> def make_desordre_score(rh_pitches, lh_pitches):
    ...     rh_staff = make_desordre_staff(rh_pitches, "RH")
    ...     lh_staff = make_desordre_staff(lh_pitches, "LH")
    ...     leaves = abjad.select(lh_staff).leaves()
    ...     abjad.iterpitches.respell_with_sharps(leaves)
    ...     staves = [rh_staff, lh_staff]
    ...     piano_staff = abjad.StaffGroup(
    ...         staves, lilypond_type="PianoStaff", name="Piano_Staff"
    ...     )
    ...     score = abjad.Score([piano_staff], name="Score")
    ...     first_note = abjad.select(lh_staff).note(0)
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, first_note)
    ...     key_signature = abjad.KeySignature("b", "major")
    ...     abjad.attach(key_signature, first_note)
    ...     return score


::

    >>> def make_desordre_lilypond_file(score):
    ...     lilypond_file = abjad.LilyPondFile.new(
    ...         music=score,
    ...         default_paper_size=("a4", "letter"),
    ...         global_staff_size=10,
    ...     )
    ...     lilypond_file.layout_block.indent = 0
    ...     lilypond_file.layout_block.ragged_right = True
    ...     lilypond_file.layout_block.merge_differently_dotted = True
    ...     lilypond_file.layout_block.merge_differently_headed = True
    ...     context_block = abjad.ContextBlock(source_lilypond_type="Score")
    ...     lilypond_file.layout_block.items.append(context_block)
    ...     context_block.remove_commands.append("Bar_number_engraver")
    ...     context_block.remove_commands.append("Default_bar_line_engraver")
    ...     context_block.remove_commands.append("Timing_translator")
    ...     abjad.override(context_block).beam.breakable = True
    ...     abjad.override(context_block).glissando.breakable = True
    ...     abjad.override(context_block).note_column.ignore_collision = True
    ...     abjad.override(context_block).spacing_spanner.uniform_stretching = True
    ...     abjad.override(context_block).text_script.staff_padding = 4
    ...     abjad.override(context_block).text_spanner.breakable = True
    ...     abjad.override(context_block).time_signature.stencil = False
    ...     abjad.override(context_block).tuplet_bracket.bracket_visibility = True
    ...     abjad.override(context_block).tuplet_bracket.minimum_length = 3
    ...     abjad.override(context_block).tuplet_bracket.padding = 2
    ...     scheme = abjad.Scheme("ly:spanner::set-spacing-rods")
    ...     abjad.override(context_block).tuplet_bracket.springs_and_rods = scheme
    ...     scheme = abjad.Scheme("tuplet-number::calc-fraction-text")
    ...     abjad.override(context_block).tuplet_number.text = scheme
    ...     abjad.setting(context_block).autoBeaming = False
    ...     moment = abjad.SchemeMoment((1, 8))
    ...     abjad.setting(context_block).proportionalNotationDuration = moment
    ...     abjad.setting(context_block).tupletFullLength = True
    ...     context_block = abjad.ContextBlock(source_lilypond_type="Staff")
    ...     lilypond_file.layout_block.items.append(context_block)
    ...     # LilyPond CAUTION: Timing_translator must appear
    ...     #                   before Default_bar_line_engraver!
    ...     context_block.consists_commands.append("Timing_translator")
    ...     context_block.consists_commands.append("Default_bar_line_engraver")
    ...     scheme = abjad.Scheme("'numbered")
    ...     abjad.override(context_block).time_signature.style = scheme
    ...     context_block = abjad.ContextBlock(source_lilypond_type="Voice")
    ...     lilypond_file.layout_block.items.append(context_block)
    ...     context_block.remove_commands.append("Forbid_line_break_engraver")
    ...     return lilypond_file



Observe the following characteristics of the cell:

1. Each cell comprises an octave followed by an eighth-note run.

2. Octave stems point up while the stems of eighth notes point down.

3. All eighth-note runs are beamed and slurred.

4. The first note of each cell is marked forte; the following notes are played piano.

5. The duration of each cell varies from 3 to 8 eighth notes.

First the eighth notes. The notes belonging to the eighth note run are first beamed and
slurred. Then we add the dynamics to the first two notes, and finally we put them inside
a Voice. After naming the voice we attach a LilyPond ``\voiceTwo`` command so that the
stems of the notes point down.

::

    >>> pitches = "b e' f'".split()
    >>> notes = [abjad.Note(_, (1, 8)) for _ in pitches]
    >>> rh_lower_voice = abjad.Voice(notes, name="RH_Lower_Voice")
    >>> abjad.beam(notes)
    >>> abjad.slur(notes)
    >>> dynamic = abjad.Dynamic("f")
    >>> abjad.attach(dynamic, notes[0])
    >>> dynamic = abjad.Dynamic("p")
    >>> abjad.attach(dynamic, notes[1])
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, notes[0])
    >>> abjad.show(rh_lower_voice)


Now we construct the octave. The duration of the chord is half the duration of the
running eighth notes if the duration of the running notes is divisible by two. Otherwise
the duration of the chord is the next integer greater than this half.  We add the
articulation marking and finally add the chord to a voice. We attach a LilyPond
``\voiceOne`` command so that the stem of the octave point up:

::

    >>> lower_pitch = abjad.NamedPitch(pitches[0])
    >>> upper_pitch = lower_pitch + abjad.NamedInterval("P8")
    >>> octave_pitches = [lower_pitch, upper_pitch]
    >>> numerator = int(math.ceil(len(pitches) / 2.))
    >>> duration = (numerator, 8)
    >>> chord = abjad.Chord(octave_pitches, duration)
    >>> articulation = abjad.Articulation(">")
    >>> abjad.attach(articulation, chord)
    >>> rh_upper_voice = abjad.Voice([chord], name="RH_Upper_Voice")
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, rh_upper_voice)
    >>> abjad.show(rh_upper_voice)


Finally we combine the two voices in a simultaneous container:

::

    >>> voices = [rh_lower_voice, rh_upper_voice]
    >>> container = abjad.Container(voices, simultaneous=True)
    >>> staff = abjad.Staff([container], name="RH_Staff")
    >>> abjad.show(staff)

Because this cell appears over and over again, we want to reuse this code to generate any
number of these cells. We here encapsulate it in a function that will take only a list of
pitches:

Now we define a function to create a measure from a list of lists of numbers. The
function is very simple. It simply creates a measure and then populates it with
cells that are created internally with the function previously defined. The function
takes pitch input in the form of a list of lists (e.g., ``[[1, 2, 3], [2, 3, 4]]``. The
input is iterated to create each of the cells to be appended to the measure. We
could have defined the function to take ready made cells directly, but we are building
the hierarchy of functions so that we can pass simple lists of lists of numbers to
generate the full structure.  To construct a Ligeti measure we would call the function
like so:

::

    >>> pitches = "c' e' g' | c' e' g' a' | e' g' a' c'"
    >>> measure = make_desordre_measure(pitches, "RH")
    >>> staff = abjad.Staff([measure], name="RH_Staff")
    >>> abjad.show(staff)

Now we move up to the next level, the staff. The function again takes a plain list as
argument. The list must be a list of lists (for measures) of lists (for cells) of
pitches. The function simply constructs the Ligeti measures internally by calling our
previously defined function and puts them inside a Staff.  As with measures, we can now
create full measure sequences with this new function:

::

    >>> pitches = [[[-1, 4, 5], [-1, 4, 5, 7, 9]], [[0, 7, 9], [-1, 4, 5, 7, 9]]]
    >>> pitches = ["b e' f' | b e' f' g' a'", "c' g' a' | b e' f' g' a'"]
    >>> staff = make_desordre_staff(pitches, "RH")
    >>> abjad.show(staff)

Finally a function that will generate the score. The function creates a piano staff,
constructs staves with Ligeti music and then appends these to the empty piano staff.
Finally it sets the clef and key signature of the lower staff to match the original
score.  The argument of the function is a list of length 2, depth 3. The first element in
the list corresponds to the upper staff, the second to the lower staff. Now that we have
the redundant aspect of the piece compactly expressed and encapsulated, we can play
around with it by changing the sequence of pitches:

In order for each staff to carry its own sequence of independent measure changes,
LilyPond requires some special setup prior to rendering. Specifically, one must move the
LilyPond ``Timing_translator`` out from the score context and into the staff context.
(You can refer to the LilyPond documentation on `Polymetric notation
<http://lilypond.org/doc/v2.12/Documentation/user/lilypond/Displaying-rhythms#Polymetric-notation>`_
to learn all about how this works. In this example we defined a custom function to set up
our LilyPond file automatically.

The final result:

::

    >>> rh_pitches = [
    ...     "b e' f' | b e' f' g' a'",
    ...     "c' g' a' | b e' f' g' a'",
    ...     "d' e' f' g' a' | c' f' g'",
    ...     "a b c' d' e' f' g'",
    ...     "a d' e' | a d' e' f' g'",
    ...     "d' f' g' | a a' b' c'' d''",
    ...     "e' f' g' a' b' | d' e' f'",
    ...     "g e'",
    ... ]

::

    >>> lh_pitches = [
    ...     "ds gs as | ds gs as cs' ds'",
    ...     "fs as cs' | ds gs as cs' ds'",
    ...     "gs as cs' ds' fs' | gs as cs'",
    ...     "ds fs gs as cs' ds' fs' cs'",
    ...     "fs as cs' | fs as cs' ds' as",
    ...     "gs cs' ds' | fs ds' fs' fs gs",
    ...     "as, cs ds fs gs | as, cs ds",
    ... ]

::

    >>> score = make_desordre_score(rh_pitches, lh_pitches)
    >>> lilypond_file = make_desordre_lilypond_file(score)
    >>> abjad.show(lilypond_file)

:author:`[Adán (2.0), Bača (3.2)]`
