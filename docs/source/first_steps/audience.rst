Audience
========

Unlike `Max <https://cycling74.com/products/max>`_, `OpenMusic
<http://repmus.ircam.fr/openmusic/home>`_ or `Pure Data <https://puredata.info/>`_, Abjad
is not a stand-alone piece of consumer software: Abjad provides no graphic user
interface, and Abjad provides no audio output beyond LilyPond's built-in MIDI
functionality. Abjad is for making PDFs of music meant for human musicians, and for doing
this with the techniques of computer programming. Abjad does this by extending the Python
programming language with a set of classes and functions. Abjad's classes and functions
"teach" Python about music notation. You can think of Abjad as a Python API for building
LilyPond files. You can also think of Abjad as an API for working with data structures
that model music notation. When you compose with Abjad you can:

* Model compositional thinking programmatically.
* Generate precompositional material programmatically.
* Generate complete scores programmatically.
* Create musical objects with a subset of LilyPond's input language.
* Inspect derived properties of the objects you create.
* Iterate objects with Abjad's selectors.
* Style everything with LilyPond.

The primary intuition behind Abjad is that music tends to be full of patterns, and
composers should be able to work programmatically with the patterned parts of music we
compose. Abjad provides an interface to this type of thinking: string manipulation,
pattern matching, all the techniques of programming become available as parts of
music composition.

Do you have to know LilyPond to work with Abjad? Yes, though you can get started without
being an expert LilyPond user. Styling the notation you produce with Abjad means styling
notation with LilyPond:

https://lilypond.org/doc/v2.20/Documentation/learning/tutorial 

Do you have to know Python to work with Abjad? Yes, though again you can get started
without being an expert Python programmer. Working with Abjad means adding computer
programming to the practice of music composition:

https://docs.python.org/3/tutorial/
