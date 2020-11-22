Bartók: *Mikrokosmos*
=====================

..  book-defaults::
    :lilypond/stylesheet: literature-examples.ily

This example reconstructs the last five measures of Bartók's "Wandering" from
*Mikrokosmos*, volume III. The end result is just a few measures long but
covers basic features you'll use in Abjad. 

Here is the finished excerpt:

..  book-import:: abjad.demos:bartok
    :hide:

..  book-import:: abjad.demos.bartok:make_bartok_score
    :hide:

..  book::
    :hide:

    >>> abjad.show(bartok.make_bartok_score())

The score
---------

We'll construct the fragment top-down from containers to notes. We could have
done it the other way around but it will be easier to keep the big picture in
mind this way. Later, you can rebuild the example bottom-up as an exercise.

First let's create an empty score. We can see our work after we add some notes:

::

    >>> score = abjad.Score()
    >>> piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff")
    >>> upper_staff = abjad.Staff(name="Upper_Staff")
    >>> upper_staff_voice = abjad.Voice(name="Upper_Staff_Voice")
    >>> upper_staff.append(upper_staff_voice)
    >>> lower_staff = abjad.Staff(name="Lower_Staff")
    >>> lower_staff_voice_2 = abjad.Voice(name="Lower_Staff_Voice_II")
    >>> lower_staff.append(lower_staff_voice_2)
    >>> piano_staff.append(upper_staff)
    >>> piano_staff.append(lower_staff)
    >>> score.append(piano_staff)

The notes
---------

Now let's add notes to the upper staff:

::

    >>> upper_staff_voice.append(r"{ \time 2/4 a'8 g'8 f'8 e'8 }")
    >>> upper_staff_voice.append(r"{ \time 3/4 d'4 g'8 f'8 e'8 d'8 }")
    >>> upper_staff_voice.append(r"{ \time 2/4 c'8 d'16 e'16 f'8 e'8 }")
    >>> upper_staff_voice.append("{ d'2 }")
    >>> upper_staff_voice.append("{ d'2 }")
    >>> abjad.show(score)

Then to the monophonic part of the lower staff:

::

    >>> lower_staff_voice_2.append("{ b4 d'8 c'8 }")
    >>> lower_staff_voice_2.append("{ b8 a8 af4 c'8 bf8 }")
    >>> lower_staff_voice_2.append("{ a8 g8 fs8 g16 a16 }")
    >>> abjad.show(score)

The simultaneous voices in measure four are more complicated:

::

    >>> container = abjad.Container(
    ...     [
    ...         abjad.Voice(name="Lower_Staff_Voice_I"),
    ...         abjad.Voice(name="Lower_Staff_Voice_II"),
    ...     ],
    ...     simultaneous=True
    >>> )
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, container["Lower_Staff_Voice_I"])
    >>> container["Lower_Staff_Voice_I"].append("b2")
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, container["Lower_Staff_Voice_II"])
    >>> container["Lower_Staff_Voice_II"].extend("b4 a4")
    >>> lower_staff.append(container)
    >>> abjad.show(score)

Measure five follows the same pattern:

::

    >>> container = abjad.Container(
    ...     [
    ...         abjad.Voice(name="Lower_Staff_Voice_I"),
    ...         abjad.Voice(name="Lower_Staff_Voice_II"),
    ...     ],
    ...     simultaneous=True
    >>> )
    >>> literal = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(literal, container["Lower_Staff_Voice_I"])
    >>> container["Lower_Staff_Voice_I"].append("b2")
    >>> literal = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> abjad.attach(literal, container["Lower_Staff_Voice_II"])
    >>> container["Lower_Staff_Voice_II"].append("g2")
    >>> lower_staff.append(container)
    >>> abjad.show(score)

Caching leaves
--------------

It will help to store the contents of each voice is a list before adding
details to the score. This effectively flattens out the polyphonic structure of
the excerpt and makes our score easier to work with:

::

    >>> upper_staff_leaves = abjad.select(upper_staff).leaves()

::

    >>> len(upper_staff_leaves)

::

    >>> lower_staff_voice_2_leaves = []
    >>> for leaf in abjad.select(lower_staff).leaves():
    ...     voice = abjad.get.parentage(leaf).get(abjad.Voice)
    ...     if voice.name == "Lower_Staff_Voice_II":
    ...         lower_staff_voice_2_leaves.append(leaf)
    ...

::

    >>> len(lower_staff_voice_2_leaves)

::

    >>> lower_staff_voice_1_leaves = []
    >>> for leaf in abjad.select(lower_staff).leaves():
    ...     voice = abjad.get.parentage(leaf).get(abjad.Voice)
    ...     if voice.name == "Lower_Staff_Voice_I":
    ...         lower_staff_voice_1_leaves.append(leaf)
    ...

::

    >>> len(lower_staff_voice_1_leaves)

Notice that the only voice in the upper staff runs the full length of the
excerpt. So does voice 2 in the lower staff. But voice 1 in the lower staff is
only two measures long.

The details
-----------

The bottom staff has a treble clef just like the top staff. Let's change that,
and add a double bar to the end of the score:

::

    >>> clef = abjad.Clef("bass")
    >>> leaf = lower_staff_voice_2_leaves[0]
    >>> abjad.attach(clef, leaf)
    >>> bar_line = abjad.deprecated.add_final_bar_line(score)
    >>> abjad.show(score)

Now let's add dynamics. We override LilyPond's DynamicLineSpanner grob to
control the distance of dynamics from each staff:

::

    >>> abjad.attach(abjad.Dynamic("pp"), upper_staff_leaves[0])
    >>> abjad.attach(abjad.Dynamic("mp"), upper_staff_leaves[5])
    >>> abjad.attach(abjad.Dynamic("pp"), lower_staff_voice_2_leaves[1])
    >>> abjad.attach(abjad.Dynamic("mp"), lower_staff_voice_2_leaves[6])
    >>> abjad.override(upper_staff).dynamic_line_spanner.staff_padding = 2
    >>> abjad.override(lower_staff).dynamic_line_spanner.staff_padding = 3
    >>> abjad.show(score)

Notice that the beams of the eighth and sixteenth notes appear as you would
usually expect: grouped by beat. We get this for free thanks to LilyPond's
default beaming algorithm. But this is not the way Bartók notated the beams.
Let's set the beams as Bartók did with some crossing the bar lines:

::

    >>> abjad.beam(upper_staff_leaves[:4])
    >>> abjad.beam(lower_staff_voice_2_leaves[1:5])
    >>> abjad.beam(lower_staff_voice_2_leaves[6:10])
    >>> abjad.show(score)

Now we add slurs:

::

    >>> abjad.slur(upper_staff_leaves[:5])
    >>> abjad.slur(upper_staff_leaves[5:])
    >>> abjad.slur(lower_staff_voice_2_leaves[1:6])
    >>> abjad.slur(lower_staff_voice_2_leaves[-10:])
    >>> leaf = lower_staff_voice_2_leaves[-10]
    >>> abjad.override(leaf).slur.direction = abjad.Down
    >>> abjad.show(score)

And hairpins:

::

    >>> abjad.hairpin("< !", upper_staff_leaves[-7:-2])
    >>> abjad.hairpin("> !", upper_staff_leaves[-2:])
    >>> leaf = upper_staff_leaves[-2]
    >>> abjad.override(leaf).hairpin.to_barline = False
    >>> abjad.show(score)

And a text spanner with LilyPond markup:

::

    >>> markup = abjad.Markup("ritard.")
    >>> start_text_span = abjad.StartTextSpan(left_text=markup)
    >>> abjad.text_spanner(
    ...     upper_staff_leaves[-7:],
    ...     start_text_span=start_text_span
    >>> )
    >>> abjad.override(upper_staff_leaves[-7]).text_spanner.staff_padding = 2
    >>> abjad.show(score)

Finally, we tie the last two notes in each staff:

::

    >>> abjad.tie(upper_staff_leaves[-2:])
    >>> abjad.tie(lower_staff_voice_1_leaves)
    >>> abjad.show(score)
