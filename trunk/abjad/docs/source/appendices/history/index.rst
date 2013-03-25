From Trevor and Víctor
======================


We are composers `Trevor Bača <http://www.trevorbaca.com>`_ and
`Víctor Adán <http://www.victoradan.net>`__, creators of Abjad, and
our earliest collaborative work dates back to shared undergraduate years
in Austin. It was the mid- to late-90s and we found ourselves interested
in ways of building up ever larger sets of musical materials in our
scores, with ever greater amounts of musical information.

Our work then began with pitch formalization, creating materials in C
and then writing the results as MIDI to hear what we'd created. Turns
out that this is a fairly common gateway into materials generation for
many composers, and so it was for us. Probably this was, and is, due to
the ever present availability of MIDI and, to a lesser extent, CSound.
But even back then it was clear to us to finding ways to embody other
aspects of the musical score -- from nested rhythms to the different
approaches to the musical measure to the arbitrarily complex structures
possible with overlapping musical voices -- would require a wholly
different level of consideration, and different development techniques
as well.

As an example, consider flat lists of floating-point values. This basic
data structure, together with the constant need some type of
quantification or rounding, feeds much of most composers' work with
CSound, pd and the like. It is a good thing, therefore, that essentially
all modern programming languages include tools for manipulating flat
lists of floats out of the box, or in the standard library. But what
happens when you want to think of pitch as something much more than
integers for core values with, perhaps, floats for microtones? What if
you want to work with pitches as fully-fledged objects? Objects capable
of carrying arbitrarily large sets of attributes and values? Objects
that might group together, first into sets, and then into larger
assemblages, and then into still larger complexes of pitch information
loaded, or even overloaded, with cross-relationships or textural
implications? Carrying this surplus of information about pitch, or the
potential uses of pitch, in data structures limited to, or centered
around, the list-of-floats paradigm then becomes a burden.

And what of working with rhythms not only as offset values, as implied
by the list-of-floats approach, but as arbitrarily nested, stretched,
compressed and stacked sets of values, as allowed by the tupleting and
measure structures of conventional score? A different approach is
needed.

There was, and still is, no reason to believe that general purpose
programming languages and development tools should come readily supplied
with the objects and methods most suitable for composerly applications.
And this means that the attributes of a domain-specific language that
will best meet the needs of composes interested in working formally with
the full complement of capabilities in traditional score remains an open
question.

We continued our work in score formalization independenly until 2005,
Trevor in a system that would come to be called Lascaux, and Víctor in
a system dubbed Cuepatlahto. We experimented with C, Mathematica and
Matlab as the core programming languages driving our systems before
settling independently on Python, Víctor out of experinece at MIT,
where he was working on his masters at the Media Lab with Berry Vercoe,
and Trevor out of the working necessities of a professional developer
and engineer.

We passed through indepedent experiences using Finale, Sibelius, Leland
Smith's SCORE, and even Adobe Illustrator as the notational rendering
engines for Lascaux and Cuepatlahto. Through all of this, both systems
were designed to tackle a shared set of problems. These included:

1. The difficulty involved in transcribing larger scale and highly
   parameterized gestures and textures into traditional Western notation.

2. The general inflexbility of closed, commercial music notation
   software packages.

3. The relative inability of objects on the printed page in conventional
   score to point to each other — or, indeed, to other objects or
   ideas outside the printed page — in ways rich enough to help capture,
   model and develop long-range, nonlocal relationships throughout our scores.

Afer collaborating on a joint paper describing the two systems, and
after discussing collaborative design and implementation at length, both
online and in weekends' long review of our respective codebases, we
decided to combine our efforts into a single, unified project. That
project is now Abjad.

In our work on Abjad we strive to develop a powerful and flexible
symbolic system. We picked the phrase 'formalized score control', or
FSC, as a nod to Xenakis, who was so far ahead in so many ways, and also
to highlight our primary project goal: to bring the full power of modern
programming languages, and tools in mathematics, text processing,
pattern recognition, and modular, iterative and incremental development
to bear on all parts of the compositional process.


Why MIDI is not enough
======================

Given that Abjad models written musical score, it might seem odd for
MIDI to be even mentioned in this manual. Yet, until fairly recently,
MIDI has played a role (sometimes tangential, other times fundamental)
in a variety of software tools related to music notation and engraving.



A very brief overview of MIDI
-----------------------------

MIDI (Musical Instrument Digital Interface) was first introduced in 1981
by Dave Smith, the founder of Sequential Circuits. The original purpose
of MIDI was to allow the communication between different electronic
musical instruments; more specifically, to allow one device to send
**control** data to another device. Typical messages might be "note On"
(play a *note*) "note Off" (turn off a *note*). A MIDI "note" message,
for example, is composed of three bytes: the first byte (the Status
byte) tells the device what kind of message this is (e.g. a Note On
message). The second byte encodes key number (which key was pressed) and
the third byte, velocity (how hard the key was pressed). It should be
clear that a *Note* in this context means something very different than
*Note* in the context of a traditional printed score. While the bias
towards keyboard interfaces is clear in the definition of the MIDI Note
control message, one can still give the MIDI note a more general use by
reinterpreting "key number" as pitch and "velocity" as loudness, the
usual perceptual correlates of these control changes as well as the most
meaningful musical parameters in western music.

With the subsequent proliferation of music production software, the SMF
(Standard Midi File) was introduced to allow the recording and storage
of the control data from a MIDI stream. The SMF required a time stamp to
keep track of when control messages took place. These are called
"delta-times" in the SMF specification.

*"The MTrk chunk type is where actual song data is stored. It is simply
a stream of MIDI events (and non-MIDI events), preceded by delta-time
values."*

In combination with the MIDI Note message, the addition of duration now
allowed one to have a minimal but sufficient **machine**
representation--a machine score--of music requiring only these
parameters: duration, pitch and loudness. Such is the case of most piano
music.



Limitations of MIDI from the point of view of score modeling
------------------------------------------------------------

But, alas, there is much more information in a printed score that can
not be practically encoded in a SMF. Common musical notions such as
meter, clef, key signature, articulation, to name only a few, are
ignored. A desire to include some of these concepts in MIDI is evident
in the inclusion of some so called *meta-events*. From the SMF
specification: " specifies non-MIDI information useful to this format or
to sequencers." Examples of *meta-events* are *Time Signature* and *Key
Signature*. In addition to the semantic elements just mentioned, there
are also the typographical elements (such as line thickness, spacing,
color, fonts, etc.) that all printed scores carry. This extra layer of
information is completely absent in a SMF. However, from the point of
view of encoding a printed score, the main limitation of MIDI is not the
lack musical features or the absence of typographical data, but the
assumption that musical durations, pitches and loudnesses can be each
fully and efficiently encoded with integers or even fractions. In a
printed score, this is not the case for any of them. MIDI encodes only
*magnitudes*: time interval magnitudes, pitch interval magnitudes,
velocity magnitudes. While these may be sufficient attributes for an
automated piano performance, they are not all the attributes of notes in
a printed score.



Written note durations vs. MIDI delta-times
-------------------------------------------

Assume a fixed tempo has been set. Assume that all magnitudes are
represented with (and limited to) rational numbers. A time interval
magnitude d = 1/4 has an infinity of equivalent representations in terms
of magnitude: d = 1/4 = 1/8 * 2 = 1/8 + 1/16 * 2 ... etc. So, for
example, while equivalent in magnitude, these are not the same notated
durations:

::

   >>> m1 = Measure((1, 4), [Note("c'4")])
   >>> m2 = Measure((1, 4), 2 * Note(0, (1, 8)))
   >>> tietools.TieSpanner(m2)
   TieSpanner(|1/4(2)|)
   >>> m3 = Measure((1, 4), [Note(0, (1, 8))] + 2 * Note(0, (1, 16)))
   >>> tietools.TieSpanner(m3)
   TieSpanner(|1/4(3)|)
   >>> r = stafftools.RhythmicStaff([m1, m2, m3])


::

   >>> show(r)

.. image:: images/index-1.png


Written note pitch vs. MIDI note-on
-----------------------------------

A similar thing happens with pitches. In MIDI, key (pitch) number 61 is
a half tone above middle C. But how is this pitch to be notated? As a C
sharp or a B flat?

::

   >>> m1 = Measure((1, 4), [Note(1, (1, 4))])
   >>> m2 = Measure((1, 4), [Note(('df', 4), (1, 4))])
   >>> r = Staff([m1, m2])


::

   >>> show(r)

.. image:: images/index-2.png


Conclusion
----------

MIDI was not designed for score representation. MIDI is a simple
communication protocol intended for real-time control. As such, it
naturally lacks the adequate model to represent the full range of
information found in printed scores.


Why LilyPond is right for Abjad
===============================

Early versions of Abjad wrote MIDI files for input to Finale and
Sibelius. Later versions of Abjad wrote ``.pbx`` files for input into
Leland Smith's SCORE. Over time we found LilyPond superior to Finale,
Sibelius and SCORE.

Nested tuplets works out of the box
-----------------------------------

LilyPond uses a single construct to nest tuplets arbitrarily:

::

    \new stafftools.RhythmicStaff {
        \time 7/8
        \times 7/8 {
            c8.
            \times 7/5 { c16 c16 c16 c16 c16 }
            \times 3/5 { c8 c8 c8 c8 c8 }
        }
    }

::

   >>> staff = stafftools.RhythmicStaff([Measure((7, 8), [])])
   >>> measure = staff[0]
   >>> measure.append(Note('c8.'))
   >>> measure.append(Tuplet(Fraction(7, 5), 5 * Note('c16')))
   >>> beamtools.BeamSpanner(measure[-1])
   BeamSpanner({c16, c16, c16, c16, c16})
   >>> measure.append(Tuplet(Fraction(3, 5), 5 * Note('c8')))
   >>> beamtools.BeamSpanner(measure[-1])
   BeamSpanner({c8, c8, c8, c8, c8})
   >>> Tuplet(Fraction(7, 8), measure.music)
   Tuplet(7/8, [c8., {* 5:7 c16, c16, c16, c16, c16 *}, {* 5:3 c8, c8, c8, c8, c8 *}])
   >>> staff.override.tuplet_bracket.bracket_visibility = True
   >>> staff.override.tuplet_bracket.padding = 1.6


::

   >>> show(staff, docs=True)

.. image:: images/index-3.png


LilyPond's tuplet input syntax works the same as any other recursive construct.

Broken tuplets work out of the box
----------------------------------

LilyPond engraves tupletted notes interrupted by nontupletted notes correctly:

::

    \new Staff {
        \times 4/7 { c'16 c'16 c'16 c'16 }
        c'8 c'8
        \times 4/7 { c'16 c'16 c'16 }
    }

::

   >>> t = Tuplet(Fraction(4, 7), Note(0, (1, 16)) * 4)
   >>> notes = Note(0, (1, 8)) * 2
   >>> u = Tuplet(Fraction(4, 7), Note(0, (1, 16)) * 3)
   >>> beamtools.BeamSpanner(t)
   BeamSpanner({c'16, c'16, c'16, c'16})
   >>> beamtools.BeamSpanner(notes)
   BeamSpanner(c'8, c'8)
   >>> beamtools.BeamSpanner(u)
   BeamSpanner({c'16, c'16, c'16})
   >>> measure = Measure((4, 8), [t] + notes + [u])
   >>> staff = stafftools.RhythmicStaff([measure])


::

   >>> show(staff, docs=True)

.. image:: images/index-4.png


Nonbinary meters work out of the box
------------------------------------

The rhythm above rewrites with time signatures in place of tuplets:

::

    \new Staff {
        \time 4/28 c'16 c'16 c'16 c'16 |
        \time 2/8  c'8  c'8 |
        \time 3/28 c'16 c'16 c'16 |
    }

::

   >>> t = Measure((4, 28), Note(0, (1, 16)) * 4)
   >>> u = Measure((2, 8), Note(0, (1, 8)) * 2)
   >>> v = Measure((3, 28), Note(0, (1, 16)) * 3)
   >>> beamtools.BeamSpanner(t)
   BeamSpanner(|4/28(4)|)
   >>> beamtools.BeamSpanner(u)
   BeamSpanner(|2/8(2)|)
   >>> beamtools.BeamSpanner(v)
   BeamSpanner(|3/28(3)|)
   >>> staff = stafftools.RhythmicStaff([t, u, v])


::

   >>> show(staff)

.. image:: images/index-5.png


The time signatures ``4/28`` and ``3/28`` here have a denominator not
equal to ``4``, ``8``, ``16`` or any other nonnegative integer power of
two. Abjad calls such time signatures **nonbinary meters** and LilyPond
engraves them correctly.

Lilypond models the musical measure correctly
---------------------------------------------

Most engraving packages make the concept of the measure out to be more
important than it should. We see evidence of this wherever an engraving
package makes it difficult for either a long note or the notes of a
tuplet to cross a barline. These difficulties come from working the idea
of measure-as-container deep into object model of the package.

There is a competing way to model the musical measure that we might call
the measure-as-background way of thinking about things. Western notation
pratice started absent any concept of the barline, introduced the idea
gradually, and has since retreated from the necessity of the convention.
Engraving packages that pick out an understanding of the barline from
the 18th or 19th centuries subscribe to the measure-as-container view of
things and oversimplify the problem. One result of this is to render
certain barline-crossing rhythmic figures either an inelegant hack or an
outright impossibility. LilyPond eschews the measure-as-container model
in favor of the measure-as-background model better able to handle both
earlier and later notation practice.
