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

Get Abjad & LilyPond
````````````````````

Get Abjad via `pip`_::

    ~$ sudo pip install abjad

Get `LilyPond`_ from http://lilypond.org/development.html.

See our :doc:`installation instructions </installation>` for detailed help on
getting Abjad and its dependencies.

Make music
``````````

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

Details
-------

.. toctree::
    :maxdepth: 2

    installation
    system_overview/index
    for_beginners/index
    examples/index
    reference_manual/index
    cookbook/index
    api/index
    developer_documentation/index
    appendices/index

..  _GitHub: https://github.com/Abjad/abjad
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _pip: https://pip.pypa.io/en/stable/