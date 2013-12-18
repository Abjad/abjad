Mozart: *Musikalisches Würfelspiel*
===================================

..  note::

    Explore the `abjad/demos/mozart/` directory for the complete code to this
    example, or import it into your Python session directly with:

    * `from abjad.demos import mozart`


Mozart's dice game is a method for aleatorically generating
sixteen-measure-long minuets.  For each measure, two six-sided dice are rolled,
and the sum of the dice used to look up a measure number in one of two tables
(one for each half of the minuet).  The measure number then locates a single
measure from a collection of musical fragments.  The fragments are concatenated
together, and "music" results.

Implementing the dice game in a composition environment is somewhat akin to
(although also somewhat more complicated than) the ubiquitous `hello world
program <http://en.wikipedia.org/wiki/Hello_world_program>`_ which every
programming language uses to demonstrate its basic syntax.

..  figure:: images/mozart-tables.png
    :align: center
    :width: 640px

    *Part of a pen-and-paper implementation from the 20th century.*

..  note::

    The musical dice game in question (*k516f*) has long been attributed to
    Mozart, albeit inconclusively.  Its actual provenance is a musicological
    problem with which we are unconcerned here.

The materials
-------------

At the heart of the dice game is a large collection, *or corpus*, of musical
fragments.  Each fragment is a single 3/8 measure, consisting of a treble voice
and a bass voice.  Traditionally, these fragments are stored in a "score", or
"table of measures", and located via two tables of measure numbers, which act
as lookups, indexing into that collection.

Duplicate measures in the original corpus are common.  Notably, the 8th measure
- actually a pair of measures represent the first and second alternate ending
of the first half of the minuet - are always identical.  The last measure of
the piece is similarly limited - there are only two possibilities rather than
the usual eleven (for the numbers 2 to 12, being all the possible sums of two
6-sided dice).

How might we store this corpus compactly?

Some basic musical information in Abjad can be stored as strings, rather than
actual collections of class instances.  Abjad can parse simple LilyPond strings
via :py:func:`p <abjad.tools.systemtools.p>`, which interprets a subset of LilyPond
syntax, and understands basic concepts like notes, chords, rests and skips, as
well as beams, slurs, ties, and articulations.

::

   >>> staff = Staff("""
   ...     c'4 ( d'4 <cs' e'>8 ) -. r8 
   ...     <g' b' d''>4 ^ \marcato ~ <g' b' d''>1
   ...     """)
   >>> f(staff)
   \new Staff {
       c'4 (
       d'4
       <cs' e'>8 -\staccato )
       r8
       <g' b' d''>4 ^\marcato ~
       <g' b' d''>1
   }


::

   >>> show(staff)

.. image:: images/index-1.png


So, instead of storing our musical information as Abjad components, we'll
represent each fragment in the corpus as a pair of strings: one representing
the bass voice contents, and the other representing the treble.  This pair of
strings can be packaged together into a collection.  For this implementation,
we'll package them into a dictionary.  Python dictionaries are cheap, and often
provide more clarity than lists; the composer does not have to rely on
remembering a convention for what data should appear in which position in a
list - they can simply label that data semantically.  In our musical
dictionary, the treble voice will use the key 't' and the bass voice will use
the key 'b'.

::

   >>> fragment = {'t': "g''8 ( e''8 c''8 )", 'b': '<c e>4 r8'}


Instead of relying on measure number tables to find our fragments - as in the
original implementation, we'll package our fragment dictionaries into a list of
lists of fragment dictionaries.  That is to say, each of the sixteen measures
in the piece will be represented by a list of fragment dictionaries.
Furthermore, the 8th measure, which breaks the pattern, will simply be a list
of two fragment dictionaries.  Structuring our information in this way lets us
avoid using measure number tables entirely; Python's list-indexing affordances
will take care of that for us.  The complete corpus looks like this:

::

   def make_mozart_measure_corpus():
       r'''Makes Mozart measure corpus.
       '''
   
       return [
           [
               {'b': 'c4 r8', 't': "e''8 c''8 g'8"},
               {'b': '<c e>4 r8', 't': "g'8 c''8 e''8"},
               {'b': '<c e>4 r8', 't': "g''8 ( e''8 c''8 )"},
               {'b': '<c e>4 r8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
               {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
               {'b': 'c4 r8', 't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
               {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
               {'b': '<c e>4 r8', 't': "e''16 c''16 g''16 e''16 c'''16 g''16"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
               {'b': '<c e>4 r8', 't': "g''8 c''8 e''8"},
               {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
           ],
           [
               {'b': 'c4 r8', 't': "e''8 c''8 g'8"},
               {'b': '<c e>4 r8', 't': "g'8 c''8 e''8"},
               {'b': '<c e>4 r8', 't': "g''8 e''8 c''8"},
               {'b': '<e g>4 r8', 't': "c''16 g'16 c''16 e''16 g'16 c''16"},
               {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
               {'b': 'c4 r8', 't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
               {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
               {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
               {'b': '<c e>4 r8', 't': "c''8 g'8 e''8"},
               {'b': '<c e>4 <c g>8', 't': "g''8 c''8 e''8"},
               {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
           ],
           [
               {'b': '<b, g>4 g,8', 't': "d''16 e''16 f''16 d''16 c''16 b'16"},
               {'b': 'g,4 r8', 't': "b'8 d''8 g''8"},
               {'b': 'g,4 r8', 't': "b'8 d''16 b'16 a'16 g'16"},
               {'b': '<g b>4 r8', 't': "f''8 d''8 b'8"},
               {'b': '<b, d>4 r8', 't': "g''16 fs''16 g''16 d''16 b'16 g'16"},
               {'b': '<g b>4 r8', 't': "f''16 e''16 f''16 d''16 c''16 b'16"},
               {'b': '<g, g>4 <b, g>8',
                   't': "b'16 c''16 d''16 e''16 f''16 d''16"},
               {'b': 'g8 g8 g8', 't': "<b' d''>8 <b' d''>8 <b' d''>8"},
               {'b': 'g,4 r8', 't': "b'16 c''16 d''16 b'16 a'16 g'16"},
               {'b': 'b,4 r8', 't': "d''8 ( b'8 g'8 )"},
               {'b': 'g4 r8', 't': "b'16 a'16 b'16 c''16 d''16 b'16"},
           ],
           [
               {'b': '<c e>4 r8', 't': "c''16 b'16 c''16 e''16 g'8"},
               {'b': 'c4 r8', 't': "e''16 c''16 b'16 c''16 g'8"},
               {'b': '<e g>4 r8', 't': "c''8 ( g'8 e'8 )"},
               {'b': '<e g>4 r8', 't': "c''8 e''8 g'8"},
               {'b': '<e g>4 r8', 't': "c''16 b'16 c''16 g'16 e'16 c'16"},
               {'b': '<c e>4 r8', 't': "c''8 c''16 d''16 e''8"},
               {'b': 'c4 r8',
                   't': "<c'' e''>8 <c'' e''>16 <d'' f''>16 <e'' g''>8"},
               {'b': '<e g>4 r8', 't': "c''8 e''16 c''16 g'8"},
               {'b': '<e g>4 r8', 't': "c''16 g'16 e''16 c''16 g''8"},
               {'b': '<e g>4 r8', 't': "c''8 e''16 c''16 g''8"},
               {'b': '<e g>4 r8', 't': "c''16 e''16 c''16 g'16 e'8"},
           ],
           [
               {'b': 'c4 r8', 't': "fs''8 a''16 fs''16 d''16 fs''16"},
               {'b': 'c8 c8 c8', 't': "<fs' d''>8 <d'' fs''>8 <fs'' a''>8"},
               {'b': 'c4 r8', 't': "d''16 a'16 fs''16 d''16 a''16 fs''16"},
               {'b': 'c8 c8 c8', 't': "<fs' d''>8 <fs' d''>8 <fs' d''>8"},
               {'b': 'c4 r8', 't': "d''8 a'8 ^\\turn fs''8"},
               {'b': 'c4 r8', 't': "d''16 cs''16 d''16 fs''16 a''16 fs''16"},
               {'b': '<c a>4 <c a>8', 't': "fs''8 a''8 d''8"},
               {'b': '<c fs>8 <c fs>8 <c a>8', 't': "a'8 a'16 d''16 fs''8"},
               {'b': 'c8 c8 c8', 't': "<d'' fs''>8 <d'' fs''>8 <d'' fs''>8"},
               {'b': '<c d>8 <c d>8 <c d>8', 't': "fs''8 fs''16 d''16 a''8"},
               {'b': '<c a>4 r8', 't': "fs''16 d''16 a'16 a''16 fs''16 d''16"},
           ],
           [
               {'b': '<b, d>8 <b, d>8 <b, d>8',
                   't': "g''16 fs''16 g''16 b''16 d''8"},
               {'b': '<b, d>4 r8', 't': "g''8 b''16 g''16 d''16 b'16"},
               {'b': '<b, d>4 r8', 't': "g''8 b''8 d''8"},
               {'b': '<b, g>4 r8', 't': "a'8 fs'16 g'16 b'16 g''16"},
               {'b': '<b, d>4 <b, g>8',
                   't': "g''16 fs''16 g''16 d''16 b'16 g'16"},
               {'b': 'b,4 r8', 't': "g''8 b''16 g''16 d''16 g''16"},
               {'b': '<b, g>4 r8', 't': "d''8 g''16 d''16 b'16 d''16"},
               {'b': '<b, g>4 r8', 't': "d''8 d''16 g''16 b''8"},
               {'b': '<b, d>8 <b, d>8 <b, g>8',
                   't': "a''16 g''16 fs''16 g''16 d''8"},
               {'b': '<b, d>4 r8', 't': "g''8 g''16 d''16 b''8"},
               {'b': '<b, d>4 r8', 't': "g''16 b''16 g''16 d''16 b'8"},
           ],
           [
               {'b': 'c8 d8 d,8', 't': "e''16 c''16 b'16 a'16 g'16 fs'16"},
               {'b': 'c8 d8 d,8',
                   't': "a'16 e''16 <b' d''>16 <a' c''>16 <g' b'>16 <fs' a'>16"},
               {'b': 'c8 d8 d,8',
                   't': "<b' d''>16 ( <a' c''>16 ) <a' c''>16 ( <g' b'>16 ) "
                       "<g' b'>16 ( <fs' a'>16 )"},
               {'b': 'c8 d8 d,8', 't': "e''16 g''16 d''16 c''16 b'16 a'16"},
               {'b': 'c8 d8 d,8', 't': "a'16 e''16 d''16 g''16 fs''16 a''16"},
               {'b': 'c8 d8 d,8', 't': "e''16 a''16 g''16 b''16 fs''16 a''16"},
               {'b': 'c8 d8 d,8', 't': "c''16 e''16 g''16 d''16 a'16 fs''16"},
               {'b': 'c8 d8 d,8', 't': "e''16 g''16 d''16 g''16 a'16 fs''16"},
               {'b': 'c8 d8 d,8', 't': "e''16 c''16 b'16 g'16 a'16 fs'16"},
               {'b': 'c8 d8 d,8', 't': "e''16 c'''16 b''16 g''16 a''16 fs''16"},
               {'b': 'c8 d8 d,8', 't': "a'8 d''16 c''16 b'16 a'16"},
           ],
           [
               {'b': 'g,8 g16 f16 e16 d16', 't': "<g' b' d'' g''>4 r8"},
               {'b': 'g,8 b16 g16 fs16 e16', 't': "<g' b' d'' g''>4 r8"},
           ],
           [
               {'b': 'd4 c8', 't': "fs''8 a''16 fs''16 d''16 fs''16"},
               {'b': '<d fs>4 r8', 't': "d''16 a'16 d''16 fs''16 a''16 fs''16"},
               {'b': '<d a>8 <d fs>8 <c d>8', 't': "fs''8 a''8 fs''8"},
               {'b': '<c a>4 <c a>8',
                   't': "fs''16 a''16 d'''16 a''16 fs''16 a''16"},
               {'b': 'd4 c8', 't': "d'16 fs'16 a'16 d''16 fs''16 a''16"},
               {'b': 'd,16 d16 cs16 d16 c16 d16',
                   't': "<a' d'' fs''>8 fs''4 ^\\trill"},
               {'b': '<d fs>4 <c fs>8', 't': "a''8 ( fs''8 d''8 )"},
               {'b': '<d fs>4 <c fs>8', 't': "d'''8 a''16 fs''16 d''16 a'16"},
               {'b': '<d fs>4 r8', 't': "d''16 a'16 d''8 fs''8"},
               {'b': '<c a>4 <c a>8', 't': "fs''16 d''16 a'8 fs''8"},
               {'b': '<d fs>4 <c a>8', 't': "a'8 d''8 fs''8"},
           ],
           [
               {'b': '<b, g>4 r8', 't': "g''8 b''16 g''16 d''8"},
               {'b': 'b,16 d16 g16 d16 b,16 g,16', 't': "g''8 g'8 g'8"},
               {'b': 'b,4 r8', 't': "g''16 b''16 g''16 b''16 d''8"},
               {'b': '<b, d>4 <b, d>8',
                   't': "a''16 g''16 b''16 g''16 d''16 g''16"},
               {'b': '<b, d>4 <b, d>8', 't': "g''8 d''16 b'16 g'8"},
               {'b': '<b, d>4 <b, d>8', 't': "g''16 b''16 d'''16 b''16 g''8"},
               {'b': '<b, d>4 r8', 't': "g''16 b''16 g''16 d''16 b'16 g'16"},
               {'b': '<b, d>4 <b, d>8',
                   't': "g''16 d''16 g''16 b''16 g''16 d''16"},
               {'b': '<b, d>4 <b, g>8', 't': "g''16 b''16 g''8 d''8"},
               {'b': 'g,16 b,16 g8 b,8', 't': "g''8 d''4 ^\\trill"},
               {'b': 'b,4 r8', 't': "g''8 b''16 d'''16 d''8"},
           ],
           [
               {'b': "c16 e16 g16 e16 c'16 c16",
                   't': "<c'' e''>8 <c'' e''>8 <c'' e''>8"},
               {'b': 'e4 e16 c16',
                   't': "c''16 g'16 c''16 e''16 g''16 <c'' e''>16"},
               {'b': '<c g>4 <c e>8', 't': "e''8 g''16 e''16 c''8"},
               {'b': '<c g>4 r8', 't': "e''16 c''16 e''16 g''16 c'''16 g''16"},
               {'b': '<c g>4 <c g>8',
                   't': "e''16 g''16 c'''16 g''16 e''16 c''16"},
               {'b': 'c16 b,16 c16 d16 e16 fs16',
                   't': "<g' c'' e''>8 e''4 ^\\trill"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "e''8 c''8 g'8"},
               {'b': '<c g>4 <c e>8', 't': "e''8 c''16 e''16 g''16 c'''16"},
               {'b': '<c g>4 <c e>8', 't': "e''16 c''16 e''8 g''8"},
               {'b': '<c g>4 <c g>8', 't': "e''16 c''16 g'8 e''8"},
               {'b': '<c g>4 <c e>8', 't': "e''8 ( g''8 c'''8 )"},
           ],
           [
               {'b': 'g4 g,8', 't': "<c'' e''>8 <b' d''>8 r8"},
               {'b': '<g, g>4 g8', 't': "d''16 b'16 g'8 r8"},
               {'b': 'g8 g,8 r8', 't': "<c'' e''>8 <b' d''>16 <g' b'>16 g'8"},
               {'b': 'g4 r8', 't': "e''16 c''16 d''16 b'16 g'8"},
               {'b': 'g8 g,8 r8', 't': "g''16 e''16 d''16 b'16 g'8"},
               {'b': 'g4 g,8', 't': "b'16 d''16 g''16 d''16 b'8"},
               {'b': 'g8 g,8 r8', 't': "e''16 c''16 b'16 d''16 g''8"},
               {'b': '<g b>4 r8', 't': "d''16 b''16 g''16 d''16 b'8"},
               {'b': '<b, g>4 <b, d>8', 't': "d''16 b'16 g'8 g''8"},
               {'b': 'g16 fs16 g16 d16 b,16 g,16', 't': "d''8 g'4"},
           ],
           [
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "e''8 c''8 g'8"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "g'8 c''8 e''8"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                   't': "g''8 e''8 c''8"},
               {'b': '<c e>4 <e g>8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
               {'b': '<c e>4 <c g>8',
                   't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
               {'b': '<c g>4 <c e>8',
                   't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
               {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
               {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                   't': "g''8 c''8 e''8"},
               {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
           ],
           [
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                   't': "e''8 ( c''8 g'8 )"},
               {'b': '<c e>4 <c g>8', 't': "g'8 ( c''8 e''8 )"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                   't': "g''8 e''8 c''8"},
               {'b': '<c e>4 <c e>8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
               {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
               {'b': '<c g>4 <c e>8',
                   't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
               {'b': '<c e>4 <e g>8', 't': "g''8 f''16 e''16 d''16 c''16"},
               {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
               {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                   't': "g''8 c''8 e''8"},
               {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
           ],
           [
               {'b': "<f a>4 <g d'>8", 't': "d''16 f''16 d''16 f''16 b'16 d''16"},
               {'b': 'f4 g8', 't': "d''16 f''16 a''16 f''16 d''16 b'16"},
               {'b': 'f4 g8', 't': "d''16 f''16 a'16 d''16 b'16 d''16"},
               {'b': 'f4 g8', 't': "d''16 ( cs''16 ) d''16 f''16 g'16 b'16"},
               {'b': 'f8 d8 g8', 't': "f''8 d''8 g''8"},
               {'b': 'f16 e16 d16 e16 f16 g16',
                   't': "f''16 e''16 d''16 e''16 f''16 g''16"},
               {'b': 'f16 e16 d8 g8', 't': "f''16 e''16 d''8 g''8"},
               {'b': 'f4 g8', 't': "f''16 e''16 d''16 c''16 b'16 d''16"},
               {'b': 'f4 g8', 't': "f''16 d''16 a'8 b'8"},
               {'b': 'f4 g8', 't': "f''16 a''16 a'8 b'16 d''16"},
               {'b': 'f4 g8', 't': "a'8 f''16 d''16 a'16 b'16"},
           ],
           [
               {'b': 'c8 g,8 c,8', 't': "c''4 r8"},
               {'b': 'c4 c,8', 't': "c''8 c'8 r8"},
           ],
       ]


We can then use the :py:func:`~abjad.tools.systemtools.p` function we saw earlier
to "build" the treble and bass components of a measure like this:

::

   def make_mozart_measure(measure_dict):
       r'''Makes Mozart measure.
       '''
   
       # parse the contents of a measure definition dictionary
       # wrap the expression to be parsed inside a LilyPond { } block
       treble = parse('{{ {} }}'.format(measure_dict['t']))
       bass = parse('{{ {} }}'.format(measure_dict['b']))
       return treble, bass


Let's try with a measure-definition of our own:

::

   >>> my_measure_dict = {'b': r'c4 ^\trill r8', 't': "e''8 ( c''8 g'8 )"}
   >>> treble, bass = make_mozart_measure(my_measure_dict)


::

   >>> f(treble)
   {
       e''8 (
       c''8
       g'8 )
   }


::

   >>> f(bass)
   {
       c4 ^\trill
       r8
   }


Now with one from the Mozart measure collection defined earlier.
We'll grab the very last choice for the very last measure:

::

   >>> my_measure_dict = make_mozart_measure_corpus()[-1][-1]
   >>> treble, bass = make_mozart_measure(my_measure_dict)


::

   >>> f(treble)
   {
       c''8
       c'8
       r8
   }


::

   >>> f(bass)
   {
       c4
       c,8
   }


The structure
-------------

After storing all of the musical fragments into a corpus, concatenating those
elements into a musical structure is relatively trivial.  We'll use the
:py:func:`~random.choice` function from Python's `random` module.
:py:func:`random.choice` randomly selects one element from an input list.

::

   >>> import random
   >>> my_list = [1, 'b', 3]
   >>> my_result = [random.choice(my_list) for i in range(20)]
   >>> my_result
   [3, 3, 'b', 1, 'b', 'b', 3, 1, 'b', 'b', 3, 'b', 1, 3, 'b', 1, 3, 3, 3, 3]


Our corpus is a list comprising sixteen sublists, one for each measure in the
minuet.  To build our musical structure, we can simply iterate through the
corpus and call `choice` on each sublist, appending the chosen results to
another list.  The only catch is that the *eighth* measure of our minuet is
actually the first-and-second-ending for the repeat of the first phrase.  The
sublist of the corpus for measure eight contains *only* the first and second
ending definitions, and both of those measures should appear in the final
piece, always in the same order.  We'll have to intercept that sublist while we
iterate through the corpus and apply some different logic.

The easist way to intercept measure eight is to use the Python builtin
`enumerate`, which allows you to iterate through a collection while also
getting the index of each element in that collection:

::

   def choose_mozart_measures():
       r'''Chooses Mozart measures.
       '''
   
       measure_corpus = make_mozart_measure_corpus()
       chosen_measures = []
       for i, choices in enumerate(measure_corpus):
           if i == 7: # get both alternative endings for mm. 8
               chosen_measures.extend(choices)
           else:
               choice = random.choice(choices)
               chosen_measures.append(choice)
       return chosen_measures


..  note::

    In `choose_mozart_measures` we test for index *7*, rather then *8*, because
    list indices count from *0* instead of *1*.

The result will be a *seventeen*-item-long list of measure definitions:

::

   >>> choices = choose_mozart_measures()
   >>> for i, measure in enumerate(choices):
   ...     print i, measure
   ... 
   0 {'b': '<c e>4 r8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"}
   1 {'b': '<c e>4 r8', 't': "c''8 g'8 e''8"}
   2 {'b': 'b,4 r8', 't': "d''8 ( b'8 g'8 )"}
   3 {'b': '<e g>4 r8', 't': "c''8 e''16 c''16 g'8"}
   4 {'b': 'c4 r8', 't': "d''16 cs''16 d''16 fs''16 a''16 fs''16"}
   5 {'b': '<b, d>4 r8', 't': "g''8 b''16 g''16 d''16 b'16"}
   6 {'b': 'c8 d8 d,8', 't': "a'16 e''16 d''16 g''16 fs''16 a''16"}
   7 {'b': 'g,8 g16 f16 e16 d16', 't': "<g' b' d'' g''>4 r8"}
   8 {'b': 'g,8 b16 g16 fs16 e16', 't': "<g' b' d'' g''>4 r8"}
   9 {'b': '<d fs>4 <c fs>8', 't': "a''8 ( fs''8 d''8 )"}
   10 {'b': 'b,4 r8', 't': "g''8 b''16 d'''16 d''8"}
   11 {'b': '<c g>4 <c e>8', 't': "e''8 ( g''8 c'''8 )"}
   12 {'b': 'g8 g,8 r8', 't': "g''16 e''16 d''16 b'16 g'8"}
   13 {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "g''8 c''8 e''8"}
   14 {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "g''8 e''8 c''8"}
   15 {'b': 'f4 g8', 't': "f''16 d''16 a'8 b'8"}
   16 {'b': 'c4 c,8', 't': "c''8 c'8 r8"}


The score
---------

Now that we have our raw materials, and a way to organize them, we can start
building our score.  The tricky part here is figuring out how to implement
LilyPond's repeat structure in Abjad.  LilyPond structures its repeats
something like this:

::

    \repeat volta n {
        music to be repeated
    }

    \alternative {
        { ending 1 }
        { ending 2 }
        { ending n }
    }

    ...music after the repeat...

What you see above is really just two containers, each with a little text
("\repeat volta n" and "alternative") prepended to their opening curly brace.
To create that structure in Abjad, we'll need to use the
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` class, which allows you
to place LilyPond commands like "\break" relative to any score component:

::

   >>> container = Container("c'4 d'4 e'4 f'4")
   >>> command = indicatortools.LilyPondCommand('before-the-container', 'before')
   >>> attach(command, container)
   >>> command = indicatortools.LilyPondCommand('after-the-container', 'after')
   >>> attach(command, container)
   >>> command = indicatortools.LilyPondCommand('opening-of-the-container', 'opening')
   >>> attach(command, container)
   >>> command = indicatortools.LilyPondCommand('closing-of-the-container', 'closing')
   >>> attach(command, container)
   >>> command = indicatortools.LilyPondCommand('to-the-right-of-a-note', 'right')
   >>> attach(command, container[2])
   >>> f(container)
   \before-the-container
   {
       \opening-of-the-container
       c'4
       d'4
       e'4 \to-the-right-of-a-note
       f'4
       \closing-of-the-container
   }
   \after-the-container


Notice the second argument to each
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` above, like `before`
and `closing`.  These are format slot indications, which control where the
command is placed in the LilyPond code relative to the score element it is
attached to.  To mimic LilyPond's repeat syntax, we'll have to create two
:py:class:`~abjad.tools.indicatortools.LilyPondCommand` instances, both using
the "before" format slot, insuring that their command is placed before their
container's opening curly brace.

Now let's take a look at the code that puts our score together:

::

   def make_mozart_score():
       r'''Makes Mozart score.
       '''
   
       score_template = templatetools.TwoStaffPianoScoreTemplate()
       score = score_template()
   
       # select the measures to use
       choices = choose_mozart_measures()
   
       # create and populate the volta containers
       treble_volta = Container()
       bass_volta = Container()
       for choice in choices[:7]:
           treble, bass = make_mozart_measure(choice)
           treble_volta.append(treble)
           bass_volta.append(bass)
   
       # attach indicators to the volta containers
       command = indicatortools.LilyPondCommand(
           'repeat volta 2', 'before'
           )
       attach(command, treble_volta)
       command = indicatortools.LilyPondCommand(
           'repeat volta 2', 'before'
           )
       attach(command, bass_volta)
   
       # append the volta containers to our staves
       score['RH Voice'].append(treble_volta)
       score['LH Voice'].append(bass_volta)
   
       # create and populate the alternative ending containers
       treble_alternative = Container()
       bass_alternative = Container()
       for choice in choices[7:9]:
           treble, bass = make_mozart_measure(choice)
           treble_alternative.append(treble)
           bass_alternative.append(bass)
   
       # attach indicators to the alternative containers
       command = indicatortools.LilyPondCommand(
           'alternative', 'before'
           )
       attach(command, treble_alternative)
       command = indicatortools.LilyPondCommand(
           'alternative', 'before'
           )
       attach(command, bass_alternative)
   
       # append the alternative containers to our staves
       score['RH Voice'].append(treble_alternative)
       score['LH Voice'].append(bass_alternative)
   
       # create the remaining measures
       for choice in choices[9:]:
           treble, bass = make_mozart_measure(choice)
           score['RH Voice'].append(treble)
           score['LH Voice'].append(bass)
   
       # attach indicators
       time_signature = indicatortools.TimeSignature((3, 8))
       attach(time_signature, score['RH Staff'])
       bar_line = indicatortools.BarLine('|.')
       attach(bar_line, score['RH Voice'][-1])
       bar_line = indicatortools.BarLine('|.')
       attach(bar_line, score['LH Voice'][-1])
   
       # remove the old, default piano instrument attached to the piano staff
       # and attach a custom instrument mark
       detach(instrumenttools.Instrument, score['Piano Staff'])
   
       klavier = instrumenttools.Piano(
           instrument_name='Katzenklavier', 
           short_instrument_name='kk.',
           )
       attach(klavier, score['Piano Staff'])
   
       return score


::

   >>> score = make_mozart_score()
   >>> show(score)

.. image:: images/index-2.png


..  note::

    Our instrument name got cut off!  Looks like we need to do a little
    formatting.  Keep reading...

The document
------------

As you can see above, we've now got our randomized minuet.  However, we can
still go a bit further.  LilyPond provides a wide variety of settings for
controlling the overall *look* of a musical document, often through its
`\header`, `\layout` and `\paper` blocks.  Abjad, in turn, gives us
object-oriented access to these settings through the its `lilypondfiletools`
module.

We'll use :py:func:`abjad.tools.lilypondfiletools.make_basic_lilypond_file` to
wrap our :py:class:`~abjad.tools.scoretools.Score` inside a
:py:class:`~abjad.tools.lilypondfiletools.LilyPondFile` instance.  From there
we can access the other "blocks" of our document to add a title, a composer's
name, change the global staff size, paper size, staff spacing and so forth.

::

   def make_mozart_lilypond_file():
       r'''Makes Mozart LilyPond file.
       '''
   
       score = make_mozart_score()
       lily = lilypondfiletools.make_basic_lilypond_file(score)
       title = markuptools.Markup(r'\bold \sans "Ein Musikalisches Wuerfelspiel"')
       composer = schemetools.Scheme("W. A. Mozart (maybe?)")
       lily.global_staff_size = 12
       lily.header_block.title = title
       lily.header_block.composer = composer
       lily.layout_block.ragged_right = True
       lily.paper_block.markup_system_spacing__basic_distance = 8
       lily.paper_block.paper_width = 180
       return lily


::

   >>> lilypond_file = make_mozart_lilypond_file()
   >>> print lilypond_file
   LilyPondFile(Score-"Two-Staff Piano Score"<<1>>)


::

   >>> print lilypond_file.header_block
   HeaderBlock(2)


::

   >>> f(lilypond_file.header_block)
   \header {
       composer = #"W. A. Mozart (maybe?)"
       title = \markup {
           \bold
               \sans
                   "Ein Musikalisches Wuerfelspiel"
           }
   }


::

   >>> print lilypond_file.layout_block
   LayoutBlock(1)


::

   >>> f(lilypond_file.layout_block)
   \layout {
       ragged-right = ##t
   }


::

   >>> print lilypond_file.paper_block
   PaperBlock(2)


::

   >>> f(lilypond_file.paper_block)
   \paper {
       markup-system-spacing #'basic-distance = #8
       paper-width = #180
   }


And now the final result:

::

   >>> show(lilypond_file)

.. image:: images/index-3.png

