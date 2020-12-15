Abjad |release|
===============

..  include:: links.rst

..  include:: abstract.rst

----

**Quickstart.** Install LilyPond from http://lilypond.org/development.html. Then get
Abjad via pip:

::

    ~$ pip install abjad

----

**An example.** Start Python, import Abjad, make some notes:

::

    >>> import abjad
    >>> string = "c'16 f' g' a' d' g' a' b' e' a' b' c'' f' b' c'' d''16"
    >>> staff_1 = abjad.Staff(string, name="Staff_1")
    >>> abjad.show(staff_1)

Use Python's list operations to split, reverse, join the input string. Then extend
staff 1:

::

    >>> pitches = string.split()
    >>> pitches = reversed(pitches)
    >>> retrograde = " ".join(pitches)
    >>> staff_1.extend(retrograde)
    >>> abjad.show(staff_1)

Create a second staff:

::

    >>> input = string + " " + retrograde
    >>> staff_2 = abjad.Staff(input, name="Staff_2")

Enclose both staves in a staff group and a score:

::

    >>> staff_group = abjad.StaffGroup(
    ...     [staff_1, staff_2],
    ...     lilypond_type="PianoStaff",
    ...     name="PianoStaff",
    ... )
    >>> score = abjad.Score([staff_group], name="Score")
    >>> abjad.show(score)

Invert the pitches in staff 2:

::

    >>> for note in abjad.select(score["Staff_2"]).notes():
    ...     note.written_pitch = note.written_pitch.invert(axis="G4")
    ... 
    >>> abjad.show(score)

Partition the notes in staff 1 according to a repeating pattern; loop over the parts:

::

    >>> notes = abjad.select(score["Staff_1"]).notes()
    >>> parts = notes.partition_by_counts([2, 4, 4], cyclic=True)
    >>> for part in parts:
    ...     part

Define a function to parameterize the loop, attach slurs, attach articulations:

::

    >>> def slur_parts(staff, counts):
    ...     notes = abjad.select(staff).notes()
    ...     parts = notes.partition_by_counts(counts, cyclic=True)
    ...     for part in parts:
    ...         first_note, last_note = part[0], part[-1]
    ...         accent = abjad.Articulation("accent")
    ...         start_slur = abjad.StartSlur()
    ...         abjad.attach(accent, first_note)
    ...         abjad.attach(start_slur, first_note)
    ...         staccato = abjad.Articulation("staccato")
    ...         stop_slur = abjad.StopSlur()
    ...         abjad.attach(staccato, last_note)
    ...         abjad.attach(stop_slur, last_note)

Call the function one way on staff 1 and another way on staff 2:

::

    >>> slur_parts(score["Staff_1"], [2, 4, 4])
    >>> slur_parts(score["Staff_2"], [4])
    >>> abjad.show(score)

Tupletize notes in staff 1:

::

    >>> notes = abjad.select(score["Staff_1"]).notes()
    >>> abjad.mutate.wrap(notes[:6], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[10:16], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[20:26], abjad.Tuplet("3:2"))
    >>> abjad.show(score)

Tupletize notes in staff 2:

::

    >>> notes = abjad.select(score["Staff_2"]).notes()
    >>> abjad.mutate.wrap(notes[4:10], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[14:20], abjad.Tuplet("3:2"))
    >>> abjad.mutate.wrap(notes[24:30], abjad.Tuplet("3:2"))
    >>> abjad.show(score)

Trim both staves, attach a time signature, attach a doule bar line, clean up tuplet
brackets:

::

    >>> del(score["Staff_1"][-6:])
    >>> del(score["Staff_2"][-3:])
    >>> first_note = abjad.select(score["Staff_1"]).note(0)
    >>> abjad.attach(abjad.TimeSignature((2, 8)), first_note)
    >>> last_note = abjad.select(score["Staff_2"]).note(-1)
    >>> abjad.attach(abjad.BarLine("|."), last_note)
    >>> abjad.override(score).tuplet_bracket.staff_padding = 2
    >>> abjad.show(score)

----

Unlike `Max <https://cycling74.com/products/max>`_, `OpenMusic
<http://repmus.ircam.fr/openmusic/home>`_ or `Pure Data <https://puredata.info/>`_, Abjad
is not a stand-alone piece of consumer software: Abjad provides no graphic user
interface, and Abjad provides no audio output beyond LilyPond's built-in MIDI
functionality. Abjad is for making PDFs of music meant to be read by human performers,
and for doing this with the techniques of computer programming. Abjad does this by
extending the Python programming language with a set of functions and classes. Abjad's
functions and classes "teach" Python about music notation, relying on LilyPond to create
PDFs of the music you create. When you compose with Abjad you can:

* Explore any Python package as part of music composition.
* Model compositional thinking programmatically.
* Create musical objects with a subset of LilyPond's input language.
* Inspect derived properties of the objects you create.
* Iterate and surgically select objects with Abjad's selectors.
* Generate precompositional material programmatically.
* Generate complete scores programmatically.
* Style everything with LilyPond.

Perhaps the core intuition behind Abjad is that music tends to be full of patterns, and
that composers should be able to work explicitly with patterns in the music we compose.
Abjad provides an interface to this type of thinking: string manipulation, pattern
matching, all the techniques of programming become available to work with music notation
and composition. Beginning work with Abjad means intuiting the reasons for working with a
programming language, even if you aren't a programmer yet. Continued work with Abjad
means comitting to developing as a programmer as yet another part of the practice of
composition.

----

Read more about Abjad here:

..  toctree::
    :maxdepth: 2

    installation
    for_beginners/index
    literature_examples/index
    recipes_pitch
    from_abjads_developers
    containerized_model
    reference_manual/index
    lilypond_context_concatenation
    api/index

----

Score gallery
-------------

Many scores have been composed with Abjad, including these:

Invisible Cities (iii): Ersilia *(2015)*
````````````````````````````````````````
- For chamber orchestra.
- Composed by `Josiah Wolf Oberholtzer`_.
- Written for Ensemble Dal Niente.
- Source available from https://github.com/josiah-wolf-oberholtzer/ersilia/.

..  container:: table-row

    ..  thumbnail:: gallery/oberholtzer-ersilia-page-9.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 9 of Invisible Cities (iii): Ersilia,
                by Josiah Wolf Oberholtzer.

    ..  thumbnail:: gallery/oberholtzer-ersilia-page-10.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 10 of Invisible Cities (iii): Ersilia,
                by Josiah Wolf Oberholtzer.

Traiettorie inargentate *(2013)*
````````````````````````````````

- For cello.
- Composed by `Trevor Bača`_.
- Written for Séverine Ballon.
- Source available from https://github.com/trevorbaca/traiettorie/.

..  container:: table-row

    ..  thumbnail:: gallery/baca-traiettorie-page-6.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 6 of Traiettorie inargentate,
                by Trevor Bača.

    ..  thumbnail:: gallery/baca-traiettorie-page-7.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 7 of Traiettorie inargentate,
                by Trevor Bača.

Visit Abjad's score gallery for many more examples.

..  toctree::

    gallery

----

..  toctree::
    :maxdepth: 1
    :hidden:

    about_the_docs
    publications
    summer_workshop
    changes

Happy composing and welcome to Abjad!

*Authored: Bača (2.0); revised: Oberholtzer (2.19-21), Bača (3.1, 3.2).*

..  _GitHub: https://github.com/Abjad/abjad
..  _Josiah Wolf Oberholtzer: http://josiahwolfoberholtzer.com
..  _LaTeX: https://tug.org/
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _Trevor Bača: http://www.trevorbaca.com/
..  _pip: https://pip.pypa.io/en/stable/
