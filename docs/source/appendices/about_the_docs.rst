About the docs
==============

LilyPond examples in Abjad's docs are generated via a custom Sphinx extension housed in
Abjad's :py:mod:`abjad.ext.sphinx <abjad.ext.sphinx>` subpackage. The examples are styled
in a particular way: notes, rests, chords are spaced proportionally; there are no bar
numbers; tuplet numbers are cleaned up.

* All examples in Abjad's docs embed a LilyPond ``\include "..."`` statement.

* Most examples include Abjad's :download:`default LilyPond stylesheet </_stylesheets/default.ily>`.

* Some examples include a different stylesheet.

* Abjad houses all LilyPond stylesheets in ``abjad/docs/source/_stylesheets/``.

----

*Authored: Oberholtzer (2.21); updated Bača (3.2).*
