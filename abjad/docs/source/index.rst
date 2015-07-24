Abjad (|release|)
=================

`GitHub`_ |
`PyPI`_ |
`Documentation <http://projectabjad.org/>`_ |
`Mailing list <http://groups.google.com/group/abjad-user>`_ |
`Issue Tracker <https://github.com/Abjad/abjad/issues>`_ |
`Travis-CI <https://travis-ci.org/Abjad/abjad>`_

Introduction
------------

Abjad helps composers build up complex pieces of music notation in an iterative
and incremental way. Use Abjad to create symbolic representations of all the
notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad
extends the `Python`_ programming language, you can use Abjad to make
systematic changes to your music as you work. And because Abjad wraps the
powerful `LilyPond`_ music notation package, you can use Abjad to control the
typographic details of the symbols on the page.

Quickstart
----------

1. Get Abjad and LilyPond
`````````````````````````

Get Abjad via `pip`_::

    ~$ sudo pip install abjad

Get `LilyPond`_ from http://lilypond.org/development.html.

See our :doc:`installation instructions </installation>` for detailed help on
getting Abjad, setting it up, and installing any dependencies like `LilyPond`_.

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

That's nice, but a little bland.

Let's split the notes you just made every 5/16, transpose every other
split group up by a major-seventh, slur every split group, and attach an accent
to the first note of each split group:

..  abjad::

    shards = mutate(staff[:]).split(
        durations=[Duration(5, 16)],
        cyclic=True,
        tie_split_notes=False,
        )
    for index, shard in enumerate(shards):
        if index % 2:
            mutate(shard).transpose('M7')
        attach(Slur(), shard)
        attach(Articulation('accent'), shard[0])

    show(staff)

That looks a little more intriguing, doesn't it?

Features
--------

Abjad lets you:

-   Create musical notation in an object-oriented way.
-   Model compositional thinking computationally.
-   Generate and transform complex rhythmic through rhythm-makers,
    meter-rewriting and quantization.
-   Construct powerful component selectors for locating musical objects in a
    score.
-   Control all of the typographic details of music notation.
-   Embed musical notation in `IPython`_ notebooks, `LaTeX`_ and `Sphinx`_
    documents.

Gallery
-------

Many scores have been composed in whole or in part with the assistance of Abjad
and LilyPond.

Here are excerpts from a few such works.

..  container:: example

    **Invisible Cities (ii): Armilla** *(2015)*, for viola duet.

    - Composed by `Josiah Wolf Oberholtzer`_.
    - Written for John Pickford Richards and Elizabeth Weisser.
    - Source available from https://github.com/josiah-wolf-oberholtzer/armilla/.

    ..  container:: table-row

        ..  thumbnail:: gallery/images/oberholtzer-armilla-page8.png
            :class: table-cell thumbnail
            :group: gallery
            :title: Invisible Cities (ii): Armilla
                    by Josiah Wolf Oberholtzer, page 8

        ..  thumbnail:: gallery/images/oberholtzer-armilla-page9.png
            :class: table-cell thumbnail
            :group: gallery
            :title: Invisible Cities (ii): Armilla,
                    by Josiah Wolf Oberholtzer, page 9.

..  container:: example

    **Aurora** *(2015)*, for string orchestra.

    - Composed by `Josiah Wolf Oberholtzer`_.
    - Written for Ensemble Kaleidoskop.
    - Source available from https://github.com/josiah-wolf-oberholtzer/aurora/.

    ..  container:: table-row

        ..  thumbnail:: gallery/images/oberholtzer-aurora-page6.png
            :class: table-cell thumbnail
            :group: gallery
            :title: **Aurora**, by Josiah Wolf Oberholtzer, page 6.
            
        ..  thumbnail:: gallery/images/oberholtzer-aurora-page7.png
            :class: table-cell thumbnail
            :group: gallery
            :title: **Aurora**, by Josiah Wolf Oberholtzer, page 7.

Installation Details
--------------------

..  toctree::
    :maxdepth: 2

    installation

High-level information
----------------------

..  toctree::
    :maxdepth: 2

    system_overview/index

Tutorial and examples
---------------------

..  toctree::
    :maxdepth: 2

    for_beginners/index
    examples/index
    reference_manual/index
    cookbook/index

Abjad's codebase in detail
--------------------------
    
..  toctree::
    :maxdepth: 2

    api/index
    developer_documentation/index

Miscellaneous information
-------------------------

..  toctree::
    :maxdepth: 2

    appendices/index

..  _GitHub: https://github.com/Abjad/abjad
..  _IPython: http://ipython.org/
..  _LaTeX: https://tug.org/
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _pip: https://pip.pypa.io/en/stable/
..  _Josiah Wolf Oberholtzer: http://josiahwolfoberholtzer.com