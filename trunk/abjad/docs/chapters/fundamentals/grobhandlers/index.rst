Grobs
=====

Introduction
------------

The term :term:`grob` stands for `graphical object`.  It is a word borrowed from LilyPond  to refer to those elements in a score that have graphical properties and thus have a visible existence in a score. 

From the `LilyPond documentation <http://lilypond.org/doc/v2.13/Documentation/user/lilypond-internals-big-page#grob_002dinterface>`__:

   A grob represents a piece of music notation. [...] A grob is often associated with a symbol, but some grobs do not print any symbols. They take care of grouping objects. For example, there is a separate grob that stacks staves vertically. The NoteCollision object is also an abstract grob: It only moves around chords, but doesn’t print anything.

   Grobs have properties [...] that can be read and set. Two types of them exist: immutable and mutable. Immutable variables define the default style and behavior. They are shared between many objects. They can be changed using \\override and \\revert. Mutable properties are variables that are specific to one grob. Typically, lists of other objects, or results from computations are stored in mutable properties. 


Many elements in Abjad are :class:`grob handlers <abjad.core.grobhandler._GrobHandler>`, which means that they support user setting of graphical properties supported by the LilyPond grobs.  
For example, because a :class:`NoteHead <abjad.notehead.notehead.NoteHead>` is a :class:`_GrobHandler <abjad.core.grobhandler._GrobHandler>`, we can change its graphical appearance by setting any of the different properties supported by the corresponding LilyPond notehead grob to anything supported by LilyPond for that grob:

::

	abjad> n = Note(1, (1, 4))
	abjad> n.notehead.color = 'red'

.. image:: images/notehead_color.png

Another example: `Glissandi` are usually represented with straight lines, but maybe you want a wiggly line. You can change the style of the `glissando` to, for example, `zigzag` by simply setting the glissando style property:

::

	abjad> s = Staff([Note(0, (1, 4)), Note(12, (1, 4))])
	abjad> g = Glissando(s.leaves)
	abjad> g.style = 'zigzag'

.. image:: images/glissando_style.png

Notice that the `grob` properties that can be set for the different Abjad objects, as well as the values these properties can take, depend entirely on those defined by LilyPond. You must, therefore, always refer to the LilyPond documentation to find out exactly what `grob` properties can be set. 

This has just been a brief introduction to the graphical attribute handling capabilities in Abjad. Many objects support many different properties. 
It is **highly** recommended that you read the LilyPond documentation carefully in order to develop an intuition of what properties can generally be set and how. This will help you tremendously at the long run to take full advantage of the affordances of Abjad.


.. note::
   
   Refer to the `LilyPond documentation <http://lilypond.org/doc/v2.13/Documentation/user/lilypond-internals-big-page#grob_002dinterface>`__ for the properties supported by all grobs.


