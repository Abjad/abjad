Abjad (|release|)
=================

..  include:: links.txt

Introduction
------------

..  include:: abstract.txt

Quickstart
----------

1. Get Abjad and LilyPond
`````````````````````````

Get Abjad via `pip`_::

    ~$ sudo pip install abjad

Get `LilyPond`_ from http://lilypond.org/development.html.

Consult our installation instructions for detailed help on getting Abjad,
setting it up, and installing any dependencies like `LilyPond`_:

..  toctree::
    :maxdepth: 2

    installation

2. Make notation
````````````````

Start your Python interpreter and import Abjad:

..  abjad::

    from abjad import *

First make eight 1/4 notes, rising by half-step from C to G:

..  abjad::

    duration = Duration(1, 4)
    notes = [Note(pitch, duration) for pitch in range(8)]
    staff = Staff(notes)
    show(staff)

..  hint::

    Click on any music notation you find in Abjad's documentation to see its
    `LilyPond`_ source code.

..  note::

    You might notice that the music notation throughout Abjad's documentation
    doesn't quite look like what `LilyPond`_ produces out-of-the-box.
    There are a number of small differences. For example, all of the notes,
    chords and rests are spaced proportionally. There are no bar numbers. The
    glissandi are a little bit thicker than normal. Tuplet brackets show the
    tuplet ratio rather than a single number.

    How does this happen? Our notation examples are generated as part of
    Abjad's doc-building process via a custom `Sphinx`_ extension housed in
    Abjad's :py:mod:`abjadbooktools <abjad.tools.abjadbooktools>` subpackage.
    To get the look-and-feel we want for our examples, we include a default
    :download:`stylesheet <_stylesheets/default.ly>` in each generated file.

    Not all examples are styled the same. When demonstrating `LilyPond`_
    overrides or page layout options we may replace Abjad's default
    documentation stylesheet with another stylesheet or disable documentation
    stylesheets entirely. If, while examining the `LilyPond`_ source files in
    Abjad's documentation, you encounter ``\include "..."`` statements in those
    files, you can find the corresponding stylesheets in Abjad's documentation
    source directory: ``abjad/docs/source/_stylesheets/``.

Now, let's split the notes you just made every 5/16 duration, transpose every
other split group up by a major-seventh, then slur every split group, and
finally attach an accent to the first note of each split group:


..  abjad::

    shards = mutate(staff[:]).split(
        durations=[Duration(5, 16)],
        cyclic=True,
        tie_split_notes=False,
        )
    for index, shard in enumerate(shards):
        if index % 2:
            mutate(shard).transpose('M7')
        if 1 < len(shard):
            attach(Slur(), shard)
        attach(Articulation('accent'), shard[0])

    show(staff)

That looks a little more intriguing, doesn't it?

Now let's create a second staff, copied from the first, invert all of the new
staff's pitches around middle-G, and finally group both staves into a staff
group:

..  abjad::

    copied_staff = mutate(staff).copy()
    staff_group = StaffGroup([staff, copied_staff])
    for note in iterate(copied_staff).by_class(Note):
        note.written_pitch = note.written_pitch.invert(axis='G4')

    show(staff_group)

Explore Abjad's documentation to find even more ways you can create and
transform notation with `Python`_, `LilyPond`_ and Abjad.

Gallery
-------

Many scores have been composed in whole or in part with the assistance of Abjad
and LilyPond. Here are excerpts from a few such works.

Traiettorie inargentate *(2013)*
````````````````````````````````

- For cello.
- Composed by `Trevor Bača`_.
- Written for Séverine Ballon.
- Source available from https://github.com/trevorbaca/traiettorie/.

..  container:: table-row

    ..  thumbnail:: gallery/baca-traiettorie-page6.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 6 of Traiettorie inargentate,
                by Trevor Bača.

    ..  thumbnail:: gallery/baca-traiettorie-page7.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 7 of Traiettorie inargentate,
                by Trevor Bača.

Invisible Cities (iii): Ersilia *(2015)*
````````````````````````````````````````

- For chamber orchestra.
- Composed by `Josiah Wolf Oberholtzer`_.
- Written for Ensemble Dal Niente.
- Source available from https://github.com/josiah-wolf-oberholtzer/ersilia/.

..  container:: table-row

    ..  thumbnail:: gallery/oberholtzer-ersilia-page9.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 9 of Invisible Cities (iii): Ersilia,
                by Josiah Wolf Oberholtzer.

    ..  thumbnail:: gallery/oberholtzer-ersilia-page10.png
        :class: table-cell thumbnail
        :group: gallery
        :title: Page 10 of Invisible Cities (iii): Ersilia,
                by Josiah Wolf Oberholtzer.

Visit our score gallery for many more examples:

..  toctree::

    gallery


Upcoming Events
---------------

`CCRMA Summer Workshop`_ 
````````````````````````

July 11-15, 2016 | Palo Alto, CA

Introduction to the production of professionally engraved musical scores
using the Python programming language and the Abjad API for Formalized
Score Control as part of compositional practice.

The course introduces Abjad's object-oriented approach to music notation
and algorithmic composition through real-world examples and hands-on coding
activities. No previous programming experience is required. Python basics
will be taught from the ground up during the course with musical examples
designed to make sense to composers.

Topics covered include:

-   system installation and configuration,
-   defining your own functions, classes and modules,
-   generating structured tableaux of rhythms, pitch collections and other materials during precomposition,
-   managing polyphony with operations on voices, staves and other musical containers,
-   working with parametric score layout,
-   understanding the document structure of complex scores, and
-   controlling the details of musical typography programmatically.

Taught by Jeff Treviño, Trevor Bača, and Josiah Wolf Oberholtzer.

..  note::

    For information on the Women in Computer Music Scholarship for the
    Formalized Score Control workshop, please visit `this page.
    <https://ccrma.stanford.edu/workshops/women-in-computer-music-abjad-scholarship>`_

Texts on Abjad
--------------

A number of papers and dissertations discuss Abjad.

-   Bača, Trevor, Josiah Wolf Oberholtzer, Jeffrey Treviño and Vıctor Adán.
    `"Abjad: An Open-Software System For Formalized Score Control."
    <https://github.com/Abjad/tenor2015/blob/master/abjad.pdf>`_
    Proceedings of the First International Conference on Technologies for Music
    Notation and Representation. 2015.

-   Oberholtzer, Josiah Wolf.
    `A Computational Model of Music Composition.
    <http://dash.harvard.edu/handle/1/17463123>`_
    Doctoral dissertation,
    Harvard University,
    Graduate School of Arts & Sciences.
    2015.

-   Trevino, Jeffrey Robert.
    `Compositional and analytic applications of automated music notation via
    object-oriented programming.
    <https://escholarship.org/uc/item/3kk9b4rv.pdf>`_
    Doctoral dissertation,
    University of California, San Diego.
    2013.

Features
--------

Abjad lets you:

-   Create musical notation in an object-oriented way.
-   Model compositional thinking computationally.
-   Generate and transform complex rhythms through rhythm-makers,
    meter-rewriting and quantization.
-   Construct powerful component selectors for locating musical objects in a
    score.
-   Parse LilyPond and RTM syntax into musical objects.
-   Control all of the typographic details of music notation.
-   Embed musical notation in `IPython`_ notebooks, `LaTeX`_ and `Sphinx`_
    documents.

Explore the high-level overview of Abjad's concepts or our tutorials and
examples to see these features in action:

..  toctree::
    :maxdepth: 2

    for_beginners/index
    literature_examples/index
    cookbook/index
    core_concepts/index
    reference_manual/index

Abjad's codebase in detail
--------------------------

..  toctree::
    :maxdepth: 2

    api/index

..  toctree::
    :maxdepth: 2

    developer_documentation/index

Miscellaneous information
-------------------------

..  toctree::
    :maxdepth: 2

    appendices/index

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
..  _CCRMA Summer Workshop: https://ccrma.stanford.edu/workshops/abjad
