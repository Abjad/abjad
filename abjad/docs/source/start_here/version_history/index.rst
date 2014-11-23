:tocdepth: 2

Version history
===============


Abjad 2.15
----------

Released 2014-11-22. Implements 496 public classes and 387 functions totaling
186,963 lines of code.


IPython / MIDI integration
^^^^^^^^^^^^^^^^^^^^^^^^^^

Abjad's IPython extension now supports the toplevel `play()` function. Just
call `play()` on any valid expression during an IPython notebook session to
generate and embed MP3 versions of that expression.

This functionality requires that you have `fluidsynth` and `ffmpeg` installed.


Travis-CI integration
^^^^^^^^^^^^^^^^^^^^^

Abjad is now tested via the Travis-CI (http://travis-ci.org/Abjad/abjad)
continuous integration service. Travis runs Abjad's complete test battery under
both Python 2.7 and 3.4 on every push or pull request made on GitHub.


The graphing protocol
^^^^^^^^^^^^^^^^^^^^^

Abjad's toplevel `graph()` function can now generate a Graphviz PDF from any
expression which has a `__graph__()` method that returns a `GraphvizGraph`
instance.


Markuptools improvements
^^^^^^^^^^^^^^^^^^^^^^^^

Abjad's Markup class now sports a variety of instance- and class-methods
mirroring LilyPond's markup functions.


Tempo improvements
^^^^^^^^^^^^^^^^^^

Tempo.to_markup()
MetricModulation
Accelerando
Ritardando
TempoSpanner


Other indicatortools improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clef and StaffPosition
BreathMark
Fermata
ColorFingering
RehearsalMark


Pitchtools improvements
^^^^^^^^^^^^^^^^^^^^^^^

A number of classes for object-modeling pitch-class transformations were added
to pitchtools. These include `Inversion`, `Multiplication` and `Transposition`.


Rhythmmakertools improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rhythm-makers can now mask their divisions in a patterned way via the new
`BooleanPattern` class.


Spannertools improvements
^^^^^^^^^^^^^^^^^^^^^^^^^

BowSpanner
TempoSpanner


Thanks
^^^^^^

Special thanks to:

- George K. Thiruvathukal <thiruvathukal@gmail.com>

for his help with Abjad's MIDI/IPython and Travis-CI integration.


Older versions
--------------

..  toctree::
    :maxdepth: 1

    version_2_15
    version_2_14
    version_2_13
    version_2_12
    version_2_11
    version_2_10
    version_2_9
    version_2_8
    version_2_7
    version_2_6
    version_2_5
    version_2_4
    version_2_3
    version_2_2
    version_2_1
    version_2_0