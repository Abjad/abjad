Pärt: *Cantus in Memory of Benjamin Britten*
============================================


Let's make some imports:

..  abjad::

    import abjad
    import copy
    from abjad.demos import part


The string music
----------------

Creating the music for the strings is a bit more involved, but conceptually
falls into two steps.  First, we'll procedurally generate basic pitches and
rhythms for all string voices.  Then, we'll make edits to the generated
material by hand.  The entire process is encapsulated in a function.

The pitch material is the same for all of the strings: a descending a-minor
scale, generally decorated with diads.  But, each instrument uses a different
overall range, with the lower instrument playing slower and slower than the
higher instruments, creating a sort of mensuration canon.

For each instrument, the descending scale is fragmented into what we'll call
"descents".  The first descent uses only the first note of that instrument's
scale, while the second descent adds the second note, and the third another.
We'll generate as many descents per instruments as there are pitches in its
overall scale.

Here's what the first 10 descents for the first violin look like:

..  abjad::

    reservoir = part.create_pitch_contour_reservoir()
    for i in range(10):
        descent = reservoir['First Violin'][i]
        print(' '.join(str(x) for x in descent))

Next we add diads to all of the descents, except for the viola's.  We'll use a
dictionary as a lookup table, to tell us what interval to add below a given
pitch class.

Finally, we'll add rhythms to the pitch contours we've been constructing.  Each
string instrument plays twice as slow as the string instrument above it in the
score.  Additionally, all the strings start with some rests, and use a
"long-short" pattern for their rhythms.

Let's see what a few of those look like.  First, we'll build the entire
reservoir from scratch, so you can see the process:

..  abjad::

    pitch_contour_reservoir = part.create_pitch_contour_reservoir()
    shadowed_contour_reservoir = part.shadow_pitch_contour_reservoir(pitch_contour_reservoir)
    durated_reservoir = part.durate_pitch_contour_reservoir(shadowed_contour_reservoir)

Then we'll grab the sub-reservoir for the first violins, taking the first ten
descents (which includes the silences we've been adding as well).  We'll label
each descent with some markup, to distinguish them, throw them into a Staff and
give them a 6/4 time signature, just so they line up properly.

..  abjad::

    descents = durated_reservoir['First Violin'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = abjad.Markup(r'\rounded-box \bold {}'.format(i), Up)
        abjad.attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = abjad.Staff(sequence(descents).flatten())
    time_signature = abjad.TimeSignature((6, 4))
    leaf = abjad.inspect(staff).get_leaf(0)
    abjad.attach(time_signature, leaf)
    show(staff)

Let's look at the second violins too:

..  abjad::

    descents = durated_reservoir['Second Violin'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = abjad.Markup(r'\rounded-box \bold {}'.format(i), Up)
        abjad.attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = abjad.Staff(sequence(descents).flatten())
    time_signature = abjad.TimeSignature((6, 4))
    leaf = abjad.inspect(staff).get_leaf(0)
    abjad.attach(time_signature, leaf)
    show(staff)

And, last we'll take a peek at the violas.  They have some longer notes, so
we'll split their music cyclically every 3 half notes, just so nothing crosses
the bar lines accidentally:

..  abjad::

    descents = durated_reservoir['Viola'][:10]
    for i, descent in enumerate(descents[1:], 1):
        markup = abjad.Markup(r'\rounded-box \bold {}'.format(i), Up)
        abjad.attach(markup, descent[0])

..  abjad::
    :stylesheet: non-proportional.ly

    staff = abjad.Staff(abjad.sequence(descents).flatten())
    shards = abjad.mutate(staff[:]).split([(3, 2)], cyclic=True)
    time_signature = abjad.TimeSignature((6, 4))
    leaf = abjad.inspect(staff).get_leaf(0)
    abjad.attach(time_signature, leaf)
    show(staff)

You can see how each part is twice as slow as the previous, and starts a little
bit later too. 

The indicators
--------------

Now we'll apply various kinds of marks, including dynamics, articulations,
bowing indications, expressive instructures, page breaks and rehearsal marks.

We'll start with the bowing marks.  This involves creating a piece of custom
markup to indicate rebowing.  We accomplish this by aggregating together some
``abjad.MarkupCommand`` and ``abjad.MusicGlyph`` objects.  The completed
``abjad.Markup`` object is then copied and attached at the correct locations in
the score. 

Why copy it?  An indicator can only be attached to a single leaf.  If we
attached the original piece of markup to each of our target components in turn,
only the last would actually receive the markup, as it would have be detached
from the preceding components.

After dealing with custom markup, applying dynamics is easy.  Just instantiate
and attach.

We apply expressive marks the same way we applied our dynamics.

We use the ``abjad.LilyPondCommand`` to create LilyPond system breaks,
and attach them to measures in the percussion part.  After this, our score will
break in the exact same places as the original.

We'll make the rehearsal marks the exact same way we made our line breaks.

And then we add our final bar lines: instantiate and attach.

The LilyPond file
-----------------

Finally, we create some functions to apply formatting directives to our score,
then wrap it into a ``LilyPondFile`` and apply some more formatting.

In our ``part.configure_score()`` functions, we use ``abjad.SpacingVector`` to
create the correct Scheme construct to tell LilyPond how to handle vertical
space for its staves and staff groups. You should consult LilyPond's vertical
spacing documentation for a complete explanation of what this Scheme code
means:

..  abjad::

    spacing_vector = abjad.SpacingVector(0, 0, 8, 0)
    print(format(spacing_vector))

In our ``part.configure_lilypond_file()`` function, we need to construct a
ContextBlock definition in order to tell LilyPond to hide empty staves, and
additionally to hide empty staves if they appear in the first system. 

Let's run our original toplevel function to build the complete score:

..  abjad::

    lilypond_file = part.make_part_lilypond_file()

And here we show it:

..  abjad::
    :no-resize:
    :no-stylesheet:
    :no-trim:
    :pages: 1-2
    :with-columns: 2
    :with-thumbnail:

    show(lilypond_file)

Note that we only show the first two pages as the *Cantus* is still under
copyright. Please visit the Universal Editions website to purchase the complete
score for performance.

Explore the ``abjad/demos/part`` directory for the complete code to this
example, or import it into your Python session directly with ``from
abjad.demos import part``.
