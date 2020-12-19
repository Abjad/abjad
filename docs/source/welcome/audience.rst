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

