From Abjad's developers
=======================

We are composers `Trevor Bača <http://www.trevorbaca.com>`_, `Josiah Wolf
Oberholtzer <http://www.josiahwolfoberholtzer.com>`_ and `Víctor Adán
<http://www.victoradan.net>`_, creators of Abjad, and our earliest
collaborative work dates back to shared undergraduate years in Austin. It was
the mid- to late-90s and we found ourselves interested in ways of building up
ever larger sets of musical materials in our scores, with ever greater amounts
of musical information.

Our work then began with pitch formalization, creating materials in C and then
writing the results as MIDI to hear what we'd created. Turns out that this is a
fairly common gateway into materials generation for many composers, and so it
was for us. Probably this was, and is, due to the ever present availability of
MIDI and, to a lesser extent, CSound.  But even back then it was clear to us to
finding ways to embody other aspects of the musical score -- from nested
rhythms to the different approaches to the musical measure to the arbitrarily
complex structures possible with overlapping musical voices -- would require a
wholly different level of consideration, and different development techniques
as well.

As an example, consider flat lists of floating-point values. This basic data
structure, together with the constant need some type of quantification or
rounding, feeds much of most composers' work with CSound, pd and the like. It
is a good thing, therefore, that essentially all modern programming languages
include tools for manipulating flat lists of floats out of the box, or in the
standard library. But what happens when you want to think of pitch as something
much more than integers for core values with, perhaps, floats for microtones?
What if you want to work with pitches as fully-fledged objects? Objects capable
of carrying arbitrarily large sets of attributes and values? Objects that might
group together, first into sets, and then into larger assemblages, and then
into still larger complexes of pitch information loaded, or even overloaded,
with cross-relationships or textural implications? Carrying this surplus of
information about pitch, or the potential uses of pitch, in data structures
limited to, or centered around, the list-of-floats paradigm then becomes a
burden.

And what of working with rhythms not only as offset values, as implied by the
list-of-floats approach, but as arbitrarily nested, stretched, compressed and
stacked sets of values, as allowed by the tupletting and measure structures of
conventional score? A different approach is needed.

There was, and still is, no reason to believe that general purpose programming
languages and development tools should come readily supplied with the objects
and methods most suitable for composerly applications.  And this means that the
attributes of a domain-specific language that will best meet the needs of
composes interested in working formally with the full complement of
capabilities in traditional score remains an open question.

We continued our work in score formalization independently until 2005, Trevor in
a system that would come to be called Lascaux, and Víctor in a system dubbed
Cuepatlahto. We experimented with C, Mathematica and Matlab as the core
programming languages driving our systems before settling independently on
Python, Víctor out of experienece at MIT, where he was working on his masters at
the Media Lab with Berry Vercoe, and Trevor out of the working necessities of a
professional developer and engineer.

We passed through independent experiences using Finale, Sibelius, Leland Smith's
SCORE, and even Adobe Illustrator as the notational rendering engines for
Lascaux and Cuepatlahto. Through all of this, both systems were designed to
tackle a shared set of problems. These included:

1. The difficulty involved in transcribing larger scale and highly
   parameterized gestures and textures into traditional Western notation.

2. The general inflexibility of closed, commercial music notation
   software packages.

3. The relative inability of objects on the printed page in conventional
   score to point to each other — or, indeed, to other objects or
   ideas outside the printed page — in ways rich enough to help capture,
   model and develop long-range, nonlocal relationships throughout our scores.

After collaborating on a joint paper describing the two systems, and after
discussing collaborative design and implementation at length, both online and
in weekends' long review of our respective code-bases, we decided to combine our
efforts into a single, unified project. That project is now Abjad.

In our work on Abjad we strive to develop a powerful and flexible symbolic
system. We picked the phrase *formalized score control*, or *FSC*, as a nod to
Xenakis, who was so far ahead in so many ways, and also to highlight our
primary project goal: to bring the full power of modern programming languages,
and tools in mathematics, text processing, pattern recognition, and modular,
iterative and incremental development to bear on all parts of the compositional
process.
