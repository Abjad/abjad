Hexachord recombination, all-interval
=====================================

Defining a function to recombine all-interval hexachords
--------------------------------------------------------

Consider the following hexachord:

::

    >>> hexachord = abjad.PitchClassSegment([0, 4, 9, 10, 8, 5])
    >>> abjad.show(hexachord)

The final pitch-class in this hexachord is 5:

::

    >>> hexachord[-1]

And the tritone transposition of this pitch-class is 11:

::

    >>> hexachord[-1] + 6

Then consider the inversion of this hexachord, transposed to start at pitch-class 11:

::

    >>> abjad.show(hexachord.invert().transpose(11))

These two hexachords complement each other; together they complete the aggregate:

::

    >>> aggregate = hexachord + hexachord.invert().transpose(11)
    >>> abjad.show(aggregate)

We can define a function to recombine any hexachord  like the one above:

::

    >>> def recombine(hexachord):
    ...     complement = hexachord.invert().transpose(hexachord[-1].number + 6)
    ...     aggregate = hexachord + complement
    ...     return aggregate

----

Up-voicing aggregates (as pitch segments)
-----------------------------------------

This type of hexachord recombination is due to Eliot Carter, who voiced the aggregates
that result from this process upwards from a start pitch. We define a function to do
this. Then we write some LilyPond code to beautify the example:

::

    >>> def voice(aggregate, start):
    ...     pitches = []
    ...     pitches.append(abjad.NumberedPitch(aggregate[0]))
    ...     for pitch_class in aggregate[1:]:
    ...         pitch = abjad.NumberedPitch(pitch_class)
    ...         while pitch < pitches[-1]:
    ...             pitch += 12
    ...         pitches.append(pitch)
    ...     segment = abjad.PitchSegment(pitches).transpose(start)
    ...     return segment

::

    >>> preamble = r"""#(set-global-staff-size 16)
    ... \layout {
    ...     \context {
    ...         \Score
    ...         proportionalNotationDuration = #(ly:make-moment 1 16)
    ...         \override SpacingSpanner.uniform-stretching = ##t
    ...     }
    ... }"""

::

    >>> aggregate = recombine(hexachord)
    >>> segment = voice(aggregate, -24)
    >>> lilypond_file = abjad.illustrate(segment)
    >>> lilypond_file.items.insert(0, preamble)
    >>> abjad.show(lilypond_file)

----

Up-voicing aggregates (as chords)
---------------------------------

Carter's preference in his sketches was to visualize aggregates as chords. We define a
function to do the same:

::

    >>> def make_score(segment):
    ...     treble_pitches, bass_pitches = [], []
    ...     for pitch in segment:
    ...         if pitch.number < 0:
    ...             bass_pitches.append(pitch)
    ...         else:
    ...             treble_pitches.append(pitch)
    ...     treble_chord = abjad.Chord(treble_pitches, (1, 1))
    ...     bass_chord = abjad.Chord(bass_pitches, (1, 1))
    ...     clef = abjad.Clef("bass")
    ...     abjad.attach(clef, bass_chord)
    ...     treble_staff = abjad.Staff([treble_chord], name="RH")
    ...     bass_staff = abjad.Staff([bass_chord], name="LH")
    ...     staves = [treble_staff, bass_staff]
    ...     piano_staff = abjad.StaffGroup(staves, lilypond_type="PianoStaff")
    ...     score = abjad.Score([piano_staff], name="Score")
    ...     abjad.override(score).time_signature.transparent = True
    ...     return score

::

    >>> aggregate = recombine(hexachord)
    >>> segment = voice(aggregate, -24)
    >>> score = make_score(segment)
    >>> lilypond_file = abjad.LilyPondFile(items=[score])
    >>> abjad.show(lilypond_file)

----

Examples
--------

Now we recombine our source hexachord, followed by three transforms.

**Example 1.** Source hexachord (repeated from above), recombined with its complement:

::

    >>> hexachord = abjad.PitchClassSegment([0, 4, 9, 10, 8, 5])
    >>> abjad.show(hexachord)

    >>> aggregate = recombine(hexachord)
    >>> segment = voice(aggregate, -24)
    >>> score = make_score(segment)
    >>> lilypond_file = abjad.LilyPondFile(items=[score])
    >>> abjad.show(lilypond_file)

----

**Example 2.** Inversion of hexachord, recombined with its complement:

::

    >>> transform = hexachord.invert()
    >>> abjad.show(transform)
    
    >>> aggregate = recombine(transform)
    >>> segment = voice(aggregate, -24)
    >>> score = make_score(segment)
    >>> lilypond_file = abjad.LilyPondFile(items=[score])
    >>> abjad.show(lilypond_file)

----

**Example 3.** Transposed retrograde of source hexachord, recombined with its complement:

::

    >>> transform = hexachord.retrograde()
    >>> transform = transform.transpose((0 - hexachord[-1].number))
    >>> abjad.show(transform)

::

    >>> aggregate = recombine(transform)
    >>> segment = voice(aggregate, -24)
    >>> score = make_score(segment)
    >>> lilypond_file = abjad.LilyPondFile(items=[score])
    >>> abjad.show(lilypond_file)

----

**Example 4.** Inverted-and-transposed retrograde of source hexachord, recombined with
its complement:

::

    >>> transform = hexachord.retrograde()
    >>> transform = transform.transpose((0 - hexachord[-1].number))
    >>> transform = transform.invert()
    >>> abjad.show(transform)

::

    >>> aggregate = recombine(transform)
    >>> segment = voice(aggregate, -24)
    >>> score = make_score(segment)
    >>> lilypond_file = abjad.LilyPondFile(items=[score])
    >>> abjad.show(lilypond_file)

:author:`[Evans (3.2). From Eliot Carter's concept of parallel-inverted all-interval
collections. Hexachords appear in Carter's Harmony Book.]`
