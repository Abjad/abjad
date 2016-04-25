Pärt: *Cantus in Memory of Benjamin Britten*
============================================

..  note::

    Explore the ``abjad/demos/part`` directory for the complete code to this
    example, or import it into your Python session directly with ``from
    abjad.demos import part``.

Let's make some imports:

..  abjad::

    import copy
    from abjad import *

..  import:: abjad.demos.part.make_part_lilypond_file:make_part_lilypond_file

The score template
------------------

..  import:: abjad.demos.part.PartCantusScoreTemplate:PartCantusScoreTemplate

The bell music
--------------

..  import:: abjad.demos.part.add_bell_music_to_score:add_bell_music_to_score

The string music
----------------

Creating the music for the strings is a bit more involved, but conceptually
falls into two steps.  First, we'll procedurally generate basic pitches and
rhythms for all string voices.  Then, we'll make edits to the generated
material by hand.  The entire process is encapsulated in the following
function:

..  import:: abjad.demos.part.add_string_music_to_score:add_string_music_to_score

The pitch material is the same for all of the strings: a descending a-minor
scale, generally decorated with diads.  But, each instrument uses a different
overall range, with the lower instrument playing slower and slower than the
higher instruments, creating a sort of mensuration canon.

For each instrument, the descending scale is fragmented into what we'll call
"descents".  The first descent uses only the first note of that instrument's
scale, while the second descent adds the second note, and the third another.
We'll generate as many descents per instruments as there are pitches in its
overall scale:

..  import:: abjad.demos.part.create_pitch_contour_reservoir:create_pitch_contour_reservoir

Here's what the first 10 descents for the first violin look like:

..  abjad::

    reservoir = create_pitch_contour_reservoir()
    for i in range(10):
        descent = reservoir['First Violin'][i]
        print(' '.join(str(x) for x in descent))

Next we add diads to all of the descents, except for the viola's.  We'll use a
dictionary as a lookup table, to tell us what interval to add below a given
pitch class:

..  import:: abjad.demos.part.shadow_pitch_contour_reservoir:shadow_pitch_contour_reservoir

Finally, we'll add rhythms to the pitch contours we've been constructing.  Each
string instrument plays twice as slow as the string instrument above it in the
score.  Additionally, all the strings start with some rests, and use a
"long-short" pattern for their rhythms:

..  import:: abjad.demos.part.durate_pitch_contour_reservoir:durate_pitch_contour_reservoir

Let's see what a few of those look like.  First, we'll build the entire
reservoir from scratch, so you can see the process:

..  abjad::

    pitch_contour_reservoir = create_pitch_contour_reservoir()
    shadowed_contour_reservoir = shadow_pitch_contour_reservoir(pitch_contour_reservoir)
    durated_reservoir = durate_pitch_contour_reservoir(shadowed_contour_reservoir)

Then we'll grab the sub-reservoir for the first violins, taking the first ten
descents (which includes the silences we've been adding as well).  We'll label
each descent with some markup, to distinguish them, throw them into a Staff and
give them a 6/4 time signature, just so they line up properly.

..  abjad::

    descents = durated_reservoir['First Violin'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = markuptools.Markup(
            r'\rounded-box \bold {}'.format(i),
            Up,
            )
        attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = Staff(sequencetools.flatten_sequence(descents))
    time_signature = TimeSignature((6, 4))
    attach(time_signature, staff)
    show(staff)

Let's look at the second violins too:

..  abjad::

    descents = durated_reservoir['Second Violin'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = markuptools.Markup(
            r'\rounded-box \bold {}'.format(i),
            Up,
            )
        attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = Staff(sequencetools.flatten_sequence(descents))
    time_signature = TimeSignature((6, 4))
    attach(time_signature, staff)
    show(staff)

And, last we'll take a peek at the violas.  They have some longer notes, so
we'll split their music cyclically every 3 half notes, just so nothing crosses
the bar lines accidentally:

..  abjad::

    descents = durated_reservoir['Viola'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = markuptools.Markup(
            r'\rounded-box \bold {}'.format(i),
            Up,
            )
        attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = Staff(sequencetools.flatten_sequence(descents))
    shards = mutate(staff[:]).split([(3, 2)], cyclic=True)
    time_signature = indicatortools.TimeSignature((6, 4))
    attach(time_signature, staff)
    show(staff)

You can see how each part is twice as slow as the previous, and starts a little
bit later too.

The edits
---------

..  import:: abjad.demos.part.edit_first_violin_voice:edit_first_violin_voice
..  import:: abjad.demos.part.edit_second_violin_voice:edit_second_violin_voice
..  import:: abjad.demos.part.edit_viola_voice:edit_viola_voice
..  import:: abjad.demos.part.edit_cello_voice:edit_cello_voice
..  import:: abjad.demos.part.edit_bass_voice:edit_bass_voice

The marks
---------

Now we'll apply various kinds of marks, including dynamics, articulations,
bowing indications, expressive instructures, page breaks and rehearsal marks.

We'll start with the bowing marks.  This involves creating a piece of custom
markup to indicate rebowing.  We accomplish this by aggregating together some
`markuptools.MarkupCommand` and `markuptools.MusicGlyph` objects.  The
completed `markuptools.Markup` object is then copied and attached at the
correct locations in the score.

Why copy it?  A `Mark` can only be attached to a single `Component`.  If we
attached the original piece of markup to each of our target components in turn,
only the last would actually receive the markup, as it would have be detached
from the preceding components.

Let's take a look:

..  import:: abjad.demos.part.apply_bowing_marks:apply_bowing_marks

After dealing with custom markup, applying dynamics is easy.  Just instantiate
and attach:

..  import:: abjad.demos.part.apply_dynamics:apply_dynamics

We apply expressive marks the same way we applied our dynamics:

..  import:: abjad.demos.part.apply_expressive_marks:apply_expressive_marks

We use the `indicatortools.LilyPondCommand` class to create LilyPond system
breaks, and attach them to measures in the percussion part.  After this, our
score will break in the exact same places as the original:

..  import:: abjad.demos.part.apply_page_breaks:apply_page_breaks

We'll make the rehearsal marks the exact same way we made our line breaks:

..  import:: abjad.demos.part.apply_rehearsal_marks:apply_rehearsal_marks

And then we add our final bar lines.  `indicatortools.BarLine` objects inherit from
`indicatortools.Mark`, so you can probably guess by now how we add them to the
score... instantiate and attach:

..  import:: abjad.demos.part.apply_final_bar_lines:apply_final_bar_lines

The LilyPond file
-----------------

Finally, we create some functions to apply formatting directives to our `Score`
object, then wrap it into a `LilyPondFile` and apply some more formatting.

In our `configure_score()` functions, we use
`schemetools.make_spacing_vector()` to create the correct Scheme construct to
tell LilyPond how to handle vertical space for its staves and staff groups. You
should consult LilyPond's vertical spacing documentation for a complete
explanation of what this Scheme code means:

..  abjad::

    spacing_vector = schemetools.make_spacing_vector(0, 0, 8, 0)
    print(format(spacing_vector))

..  import:: abjad.demos.part.configure_score:configure_score

In our `configure_lilypond_file()` function, we need to construct a
ContextBlock definition in order to tell LilyPond to hide empty staves, and
additionally to hide empty staves if they appear in the first system:

..  import:: abjad.demos.part.configure_lilypond_file:configure_lilypond_file

Let's run our original toplevel function to build the complete score:

..  abjad::

    lilypond_file = make_part_lilypond_file()

And here we show it:

..  abjad::
    :no-resize:
    :no-stylesheet:
    :no-trim:
    :pages: 1-2
    :with-columns: 2
    :with-thumbnail:

    show(lilypond_file)

..  note::

    We only show the first two pages as the *Cantus* is still under copyright.
