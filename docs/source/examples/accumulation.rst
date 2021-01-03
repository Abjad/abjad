Accumulation, of cells
======================

..  book-defaults::
    :lilypond/stylesheet: literature-examples.ily

::

    >>> from abjad.demos import ligeti

This example demonstrates one way of modeling composition as an accumulation of musical
cells. The piece that concerns us here is "Désordre" (1986) from the first book of György
Ligeti's piano etudes. We'll model the first two systems of the score:

.. image :: images/desordre.jpg

Observe the following characteristics of the cell:

1. Each cell comprises an octave followed by an eighth-note run.

2. Octave stems point up while the stems of eighth notes point down.

3. All eighth-note runs are beamed and slurred.

4. The first note of each cell is marked forte; the following notes are played piano.

5. The duration of each cell varies from 3 to 8 eighth notes.

The two "layers" of the cell we will model with two Voices inside a simultaneous
Container. The top Voice will hold the octave "chord" while the lower Voice will hold the
eighth note run. First the eighth notes:

::

    >>> pitches = [1, 2, 3]
    >>> maker = abjad.NoteMaker()
    >>> notes = maker(pitches, [(1, 8)])
    >>> abjad.beam(notes)
    >>> abjad.slur(notes)
    >>> abjad.attach(abjad.Dynamic("f"), notes[0])
    >>> abjad.attach(abjad.Dynamic("p"), notes[1])

::

    >>> voice_lower = abjad.Voice(notes, name="rh_lower")
    >>> command = abjad.LilyPondLiteral(r"\voiceTwo")
    >>> leaf = abjad.get.leaf(voice_lower, 0)
    >>> abjad.attach(command, leaf)
    >>> abjad.show(voice_lower)

The notes belonging to the eighth note run are first beamed and slurred. Then we add the
dynamics to the first two notes, and finally we put them inside a Voice. After naming the
voice we number it ``2`` so that the stems of the notes point down.

Now we construct the octave:

::

    >>> import math
    >>> n = int(math.ceil(len(pitches) / 2.))
    >>> chord = abjad.Chord([pitches[0], pitches[0] + 12], (n, 8))
    >>> articulation = abjad.Articulation(">")
    >>> abjad.attach(articulation, chord)

::

    >>> voice_higher = abjad.Voice([chord], name="rh_higher")
    >>> command = abjad.LilyPondLiteral(r"\voiceOne")
    >>> abjad.attach(command, voice_higher)
    >>> abjad.show(voice_higher)

The duration of the chord is half the duration of the running eighth notes if the
duration of the running notes is divisible by two. Otherwise the duration of the chord is
the next integer greater than this half.  We add the articulation marking and finally ad
the Chord to a Voice, to which we set the number to 1, forcing the stem to always point
up.

Finally we combine the two voices in a simultaneous container which results in a complete
cell:

::

    >>> voices = [voice_lower, voice_higher]
    >>> container = abjad.Container(voices, simultaneous=True)
    >>> staff = abjad.Staff([container])
    >>> abjad.show(staff)

Because this cell appears over and over again, we want to reuse this code to generate any
number of these cells. We here encapsulate it in a function that will take only a list of
pitches.

..  book-import:: abjad.demos.ligeti:make_desordre_cell

Now we can call this function to create any number of cells. That was actually the
hardest part of reconstructing the opening of Ligeti's "Désordre." Because the repetition
of patters occurs also at the level of measures and staves, we will now define functions
to create these other higher level constructs.

The measure
-----------

We define a function to create a measure from a list of lists of numbers.

The function is very simple. It simply creates a DynamicMeasure and then populates it
with cells that are created internally with the function previously defined. The function
takes a list `pitches` which is actually a list of lists of pitches (e.g., ``[[1,2,3],
[2,3,4]]``. The list of lists of pitches is iterated to create each of the cells to be
appended to the DynamicMeasures. We could have defined the function to take ready made
cells directly, but we are building the hierarchy of functions so that we can pass simple
lists of lists of numbers to generate the full structure.  To construct a Ligeti measure
we would call the function like so:

::

    >>> pitches = [[0, 4, 7], [0, 4, 7, 9], [4, 7, 9, 11]]
    >>> measure = ligeti.make_desordre_measure(pitches)
    >>> staff = abjad.Staff([measure])
    >>> abjad.show(staff)

The staff
---------

Now we move up to the next level, the staff.

..  book-import:: abjad.demos.ligeti:make_desordre_measure

The function again takes a plain list as argument. The list must be a list of lists (for
measures) of lists (for cells) of pitches. The function simply constructs the Ligeti
measures internally by calling our previously defined function and puts them inside a
Staff.  As with measures, we can now create full measure sequences with this new
function:

::

    >>> pitches = [[[-1, 4, 5], [-1, 4, 5, 7, 9]], [[0, 7, 9], [-1, 4, 5, 7, 9]]]
    >>> staff = ligeti.make_desordre_staff(pitches)
    >>> abjad.show(staff)

The score
---------

Finally a function that will generate the whole opening section of the piece "Désordre":

..  book-import:: abjad.demos.ligeti:make_desordre_score

The function creates a piano staff, constructs staves with Ligeti music and then appends
these to the empty piano staff. Finally it sets the clef and key signature of the lower
staff to match the original score.  The argument of the function is a list of length 2,
depth 3. The first element in the list corresponds to the upper staff, the second to the
lower staff.

The final result:

::

    >>> upper = [
    ...     [[-1, 4, 5], [-1, 4, 5, 7, 9]], 
    ...     [[0, 7, 9], [-1, 4, 5, 7, 9]], 
    ...     [[2, 4, 5, 7, 9], [0, 5, 7]], 
    ...     [[-3, -1, 0, 2, 4, 5, 7]], 
    ...     [[-3, 2, 4], [-3, 2, 4, 5, 7]], 
    ...     [[2, 5, 7], [-3, 9, 11, 12, 14]], 
    ...     [[4, 5, 7, 9, 11], [2, 4, 5]], 
    ...     [[-5, 4, 5, 7, 9, 11, 12]], 
    ...     [[2, 9, 11], [2, 9, 11, 12, 14]],
    ... ]

::

    >>> lower = [
    ...     [[-9, -4, -2], [-9, -4, -2, 1, 3]], 
    ...     [[-6, -2, 1], [-9, -4, -2, 1, 3]], 
    ...     [[-4, -2, 1, 3, 6], [-4, -2, 1]], 
    ...     [[-9, -6, -4, -2, 1, 3, 6, 1]], 
    ...     [[-6, -2, 1], [-6, -2, 1, 3, -2]], 
    ...     [[-4, 1, 3], [-6, 3, 6, -6, -4]], 
    ...     [[-14, -11, -9, -6, -4], [-14, -11, -9]], 
    ...     [[-11, -2, 1, -6, -4, -2, 1, 3]], 
    ...     [[-6, 1, 3], [-6, -4, -2, 1, 3]],
    ... ]

::

    >>> score = ligeti.make_desordre_score([upper, lower])
    >>> lilypond_file = ligeti.make_desordre_lilypond_file(score)
    >>> abjad.show(lilypond_file)

Now that we have the redundant aspect of the piece compactly expressed and encapsulated,
we can play around with it by changing the sequence of pitches.

In order for each staff to carry its own sequence of independent measure changes,
LilyPond requires some special setup prior to rendering. Specifically, one must move the
LilyPond ``Timing_translator`` out from the score context and into the staff context.
(You can refer to the LilyPond documentation on `Polymetric notation
<http://lilypond.org/doc/v2.12/Documentation/user/lilypond/Displaying-rhythms#Polymetric-notation>`_
to learn all about how this works. In this example we defined a custom function to set up
our LilyPond file automatically.

:author:`[Authored: Adán (2.0); revised: Bača (3.2).]`
