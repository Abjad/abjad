Ligeti: *Désordre*
==================

..  note::

    Explore the ``abjad/demos/desordre/`` directory for the complete code to
    this example, or import it into your Python session directly with ``from
    abjad.demos import desordre``.

This example demonstrates the power of exploiting redundancy to model musical
structure. The piece that concerns us here is Ligeti's *Désordre*: the first
piano study from Book I. Specifically, we will focus on modeling the first
section of the piece:

.. image :: images/desordre.jpg

The redundancy is immediately evident in the repeating pattern found in both
staves. The pattern is hierarchical. At the smallest level we have what we will
here call a *cell*:

..  import:: abjad.demos.desordre.make_desordre_cell:make_desordre_cell
    :hide:

..  abjad::
    :hide:
    :stylesheet: non-proportional.ly

    cell = Staff([make_desordre_cell([1, 2, 3])])
    show(cell)


There are two of these cells per measure. Notice that the cells are strictly
contained within the measure (i.e., there are no cells crossing a bar line).
So, the next level in the hierarchy is the measure.  Notice that the measure
sizes (the meters) change and that these changes occur independently for each
staff, so that each staff carries it's own sequence of measures. Thus, the
staff is the next level in the hierarchy.  Finally there's the piano staff,
which is composed of the right hand and left hand staves.

In what follows we will model this structure in this order (*cell*, measure,
staff, piano staff), from bottom to top.

The cell
--------

Before plunging into the code, observe the following characteristic of the
*cell*:

1. It is composed of two layers: the top one which is an octave "chord" and the
bottom one which is a straight eighth note run.

2. The total duration of the *cell* can vary, and is always the sum of the
eight note funs.

3. The eight note runs are always stem down while the octave "chord" is always
stem up.

4. The eight note runs are always beamed together and slurred, and the first
two notes always have the dynamic markings 'f' 'p'.

The two "layers" of the *cell* we will model with two Voices inside a
simultaneous Container. The top Voice will hold the octave "chord" while the
lower Voice will hold the eighth note run. First the eighth notes:

..  abjad::

    pitches = [1,2,3]
    notes = scoretools.make_notes(pitches, [(1, 8)])
    beam = Beam()
    attach(beam, notes)
    slur = Slur()
    attach(slur, notes)
    dynamic = Dynamic('f')
    attach(dynamic, notes[0])
    dynamic = Dynamic('p')
    attach(dynamic, notes[1])

..  abjad::

    voice_lower = Voice(notes)
    voice_lower.name = 'rh_lower'
    command = indicatortools.LilyPondCommand('voiceTwo')
    attach(command, voice_lower)

The notes belonging to the eighth note run are first beamed and slurred. Then
we add the dynamics to the first two notes, and finally we put them inside
a Voice. After naming the voice we number it ``2`` so that the stems of the
notes point down.

Now we construct the octave:

..  abjad::

    import math
    n = int(math.ceil(len(pitches) / 2.))
    chord = Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = Articulation('>')
    attach(articulation, chord)

..  abjad::

    voice_higher = Voice([chord])
    voice_higher.name = 'rh_higher'
    command = indicatortools.LilyPondCommand('voiceOne')
    attach(command, voice_higher)

The duration of the chord is half the duration of the running eighth notes if
the duration of the running notes is divisible by two. Otherwise the duration
of the chord is the next integer greater than this half.  We add the
articulation marking and finally ad the Chord to a Voice, to which we set the
number to 1, forcing the stem to always point up.

Finally we combine the two voices in a simultaneous container:

..  abjad::
    
    container = Container([voice_lower, voice_higher])
    container.is_simultaneous = True

This results in the complete *Désordre* *cell*:

..  abjad::
    :stylesheet: non-proportional.ly
    
    cell = Staff([container])
    show(cell)

Because this *cell* appears over and over again, we want to reuse this code to
generate any number of these *cells*. We here encapsulate it in a function that
will take only a list of pitches:

..  import:: abjad.demos.desordre.make_desordre_cell:make_desordre_cell

Now we can call this function to create any number of *cells*. That was
actually the hardest part of reconstructing the opening of Ligeti's *Désordre*.
Because the repetition of patters occurs also at the level of measures and
staves, we will now define functions to create these other higher level
constructs.

The measure
-----------

We define a function to create a measure from a list of lists of numbers:

..  import:: abjad.demos.desordre.make_desordre_measure:make_desordre_measure

The function is very simple. It simply creates a DynamicMeasure and then
populates it with *cells* that are created internally with the function
previously defined. The function takes a list `pitches` which is actually a
list of lists of pitches (e.g., ``[[1,2,3], [2,3,4]]``. The list of lists of
pitches is iterated to create each of the *cells* to be appended to the
DynamicMeasures. We could have defined the function to take ready made *cells*
directly, but we are building the hierarchy of functions so that we can pass
simple lists of lists of numbers to generate the full structure.  To construct
a Ligeti measure we would call the function like so:

..  abjad::
    :stylesheet: non-proportional.ly

    pitches = [[0, 4, 7], [0, 4, 7, 9], [4, 7, 9, 11]]
    measure = make_desordre_measure(pitches)
    staff = Staff([measure])
    show(staff)

The staff
---------

Now we move up to the next level, the staff:

..  import:: abjad.demos.desordre.make_desordre_staff:make_desordre_staff

The function again takes a plain list as argument. The list must be a list of
lists (for measures) of lists (for cells) of pitches. The function simply
constructs the Ligeti measures internally by calling our previously defined
function and puts them inside a Staff.  As with measures, we can now create
full measure sequences with this new function:

..  abjad::
    :stylesheet: non-proportional.ly

    pitches = [[[-1, 4, 5], [-1, 4, 5, 7, 9]], [[0, 7, 9], [-1, 4, 5, 7, 9]]]
    staff = make_desordre_staff(pitches)
    show(staff)

The score
---------

Finally a function that will generate the whole opening section of the piece
*Désordre*:

..  import:: abjad.demos.desordre.make_desordre_score:make_desordre_score

The function creates a PianoStaff, constructs Staves with Ligeti music and
appends these to the empty PianoStaff. Finally it sets the clef and key
signature of the lower staff to match the original score.  The argument of the
function is a list of length 2, depth 3. The first element in the list
corresponds to the upper staff, the second to the lower staff.

The final result:

..  abjad::

    top = [
        [[-1, 4, 5], [-1, 4, 5, 7, 9]], 
        [[0, 7, 9], [-1, 4, 5, 7, 9]], 
        [[2, 4, 5, 7, 9], [0, 5, 7]], 
        [[-3, -1, 0, 2, 4, 5, 7]], 
        [[-3, 2, 4], [-3, 2, 4, 5, 7]], 
        [[2, 5, 7], [-3, 9, 11, 12, 14]], 
        [[4, 5, 7, 9, 11], [2, 4, 5]], 
        [[-5, 4, 5, 7, 9, 11, 12]], 
        [[2, 9, 11], [2, 9, 11, 12, 14]],
        ]

..  abjad::

    bottom = [
        [[-9, -4, -2], [-9, -4, -2, 1, 3]], 
        [[-6, -2, 1], [-9, -4, -2, 1, 3]], 
        [[-4, -2, 1, 3, 6], [-4, -2, 1]], 
        [[-9, -6, -4, -2, 1, 3, 6, 1]], 
        [[-6, -2, 1], [-6, -2, 1, 3, -2]], 
        [[-4, 1, 3], [-6, 3, 6, -6, -4]], 
        [[-14, -11, -9, -6, -4], [-14, -11, -9]], 
        [[-11, -2, 1, -6, -4, -2, 1, 3]], 
        [[-6, 1, 3], [-6, -4, -2, 1, 3]],
        ]

..  abjad::

    score = make_desordre_score([top, bottom])

..  abjad::

    lilypond_file = documentationtools.make_ligeti_example_lilypond_file(score)

..  abjad::
    :stylesheet: non-proportional.ly

    show(lilypond_file)

Now that we have the redundant aspect of the piece compactly expressed and
encapsulated, we can play around with it by changing the sequence of pitches.

In order for each staff to carry its own sequence of independent measure
changes, LilyPond requires some special setup prior to rendering. Specifically,
one must move the LilyPond ``Timing_translator`` out from the score context and
into the staff context.

(You can refer to the LilyPond documentation on
`Polymetric notation <http://lilypond.org/doc/v2.12/Documentation/user/lilypond/Displaying-rhythms#Polymetric-notation>`_
to learn all about how this works.)

In this example we a custom ``documentationtools`` function to set up our
LilyPond file automatically.
