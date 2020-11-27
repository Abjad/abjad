Abjad |release|
===============

..  include:: links.txt

..  include:: abstract.txt

Quickstart
----------

Get Abjad via `pip`_::

    ~$ sudo pip install abjad

Then get `LilyPond`_ from http://lilypond.org/development.html. Read the
:ref:`installation instructions<installation>` for help installing Abjad and
dependencies like `LilyPond`_.

..  toctree::
    :hidden:
    :maxdepth: 2

    installation

Start Python and import Abjad:

::

    >>> import abjad

Then make some notes:

::

    >>> duration = abjad.Duration(1, 4)
    >>> notes = [abjad.Note(pitch, duration) for pitch in range(8)]
    >>> staff = abjad.Staff(notes)
    >>> abjad.show(staff)

Split these notes at every 5/16 of a whole note. Transpose every other group up
a major-seventh. Then slur and accent each group:

::

    >>> groups = abjad.mutate.split(
    ...     staff[:],
    ...     durations=[abjad.Duration(5, 16)],
    ...     cyclic=True,
    ... )
    >>> for index, group in enumerate(groups):
    ...     if index % 2:
    ...         abjad.mutate.transpose(group, "M7")
    ...     if 1 < len(group):
    ...         abjad.slur(group)
    ...     accent = abjad.Articulation("accent")
    ...     abjad.attach(accent, group[0])
    ...
    >>> abjad.show(staff)

Then create a second staff and invert its pitches:

::

    >>> copied_staff = abjad.mutate.copy(staff)
    >>> staff_group = abjad.StaffGroup(
    ...     [staff, copied_staff],
    ...     lilypond_type="PianoStaff",
    ... )
    >>> for note in abjad.select(copied_staff).notes():
    ...     note.written_pitch = note.written_pitch.invert(axis="G4")
    ... 
    >>> abjad.show(staff_group)

Notice that the music notation examples in Abjad's docs are styled in a special
way: notes, chords and rests are spaced proportionally; there are no bar
numbers; tuplet numbers are cleaned up; and so on. These settings differ
somewhat from LilyPond defaults. [#f1]_ 

Features
--------

Abjad 3.1 implements an extensive collection of tools for score formalization.
Among its core features, Abjad lets you:

-   Model compositional thinking computationally.
-   Create music notation in an object-oriented way.
-   Select musical objects programmatically.
-   Control the typographic details of music notation.
-   Parse LilyPond and RTM syntax into Abjad objects.
-   Create and transform complex rhythms.

.. -   Embed musical notation in `IPython`_ notebooks, `LaTeX`_ and `Sphinx`_ documents.

Read more about Abjad here:

..  toctree::
    :maxdepth: 2

    for_beginners/index
    literature_examples/index
    core_concepts/index
    reference_manual/index

Then join the :ref:`Abjad mailing list<mailing_list>` to ask questions and
contribute.

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

`CCRMA Summer Workshop`_ 
````````````````````````
Summers | Palo Alto, CA

Introduction to the production of professionally engraved musical scores using
the Python programming language and the Abjad API for Formalized Score Control
as part of compositional practice.

The course introduces Abjad's object-oriented approach to music notation and
algorithmic composition through real-world examples and hands-on coding
activities. No previous programming experience is required. Python basics will
be taught from the ground up during the course with musical examples designed
to make sense to composers.

Topics covered include:

-   system installation and configuration
-   defining your own functions, classes and modules
-   generating structured tableaux of rhythms, pitch collections and other
    materials during precomposition
-   managing polyphony with operations on voices, staves and other musical containers
-   working with parametric score layout
-   understanding the document structure of complex scores
-   controlling the details of musical typography programmatically

Taught by Jeff Treviño, Trevor Bača and Josiah Wolf Oberholtzer.

Visit the `CCRMA`_ website for the most up-to-date scheduling information about
this annual course.

Additional information
----------------------

The most important resource for intermediate and experienced users of Abjad is
the Abjad API, which documents the hundreds of classes that make up the system:

..  toctree::
    :maxdepth: 2

    api/index

The Abjad package ecosystem includes tools for rhythmic quantization and
rhythmic construction:

- https://github.com/abjad/abjad-ext-nauert
- https://github.com/abjad/abjad-ext-rmakers

.. - IPython integration: https://github.com/abjad/abjad-ext-ipython
.. - Quantization tools: https://github.com/abjad/abjad-ext-nauert

Finally, a number of publications discussing Abjad are available for download here:

-   Bača, Trevor, Josiah Wolf Oberholtzer, Jeffrey Treviño and Vıctor Adán.
    `"Abjad: An Open-Software System For Formalized Score Control."
    <https://github.com/Abjad/tenor2015/blob/master/abjad.pdf>`_
    Proceedings of the First International Conference on Technologies for Music
    Notation and Representation. 2015.

-   Davancens, Joseph.
    `"Heave, Sway, Surge."
    <https://github.com/jdavancens/dissertationpdf/blob/master/Heave%2C%20Sway%2C%20Surge%20-%20Essay.pdf>`_
    Doctoral dissertation,
    University of California, Santa Cruz.
    2019.

-   Evans, Gregory Rowland.
    `"An introduction to modeling composition through Abjad's model of music notation."
    <https://github.com/GregoryREvans/thesis/blob/master/An_Introduction_to_Modeling_Composition_through_Abjad's_Model_of_Music_Notation.pdf>`_
    Master's thesis,
    University of Miami.
    2019.

-   Oberholtzer, Josiah Wolf.
    `A Computational Model of Music Composition.
    <http://dash.harvard.edu/handle/1/17463123>`_
    Doctoral dissertation,
    Harvard University,
    Graduate School of Arts & Sciences.
    2015.

-   Treviño, Jeffrey Robert.
    `Compositional and analytic applications of automated music notation via
    object-oriented programming.
    <https://escholarship.org/uc/item/3kk9b4rv.pdf>`_
    Doctoral dissertation,
    University of California, San Diego.
    2013.

Happy composing and welcome to Abjad |release|!

..  rubric:: Footnotes

..  [#f1] LilyPond examples in Abjad's docs are generated via a custom
          `Sphinx`_ extension housed in the :py:mod:`abjad.ext.sphinx
          <abjad.ext.sphinx>` subpackage. A default :download:`stylesheet
          <_stylesheets/default.ily>` is included in each generated file. But
          not all excerpts are styled the same: examples demonstrating
          `LilyPond`_ overrides include a non-default stylesheet, for example.
          ``\include "..."`` statements in Abjad examples reference files in
          the ``abjad/docs/source/_stylesheets/`` directory.

..  _CCRMA Summer Workshop: https://ccrma.stanford.edu/workshops/python-and-abjad-in-music-comp-2018
..  _CCRMA: https://ccrma.stanford.edu
..  _GitHub: https://github.com/Abjad/abjad
..  _IPython: http://ipython.org/
..  _Josiah Wolf Oberholtzer: http://josiahwolfoberholtzer.com
..  _LaTeX: https://tug.org/
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _Trevor Bača: http://www.trevorbaca.com/
..  _pip: https://pip.pypa.io/en/stable/
