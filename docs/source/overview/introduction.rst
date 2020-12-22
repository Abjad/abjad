Introduction
============

Because Abjad extends Python, the number of different patterns you can use to create
musical objects is unlimited. If your compositional thinking derives musical phrases from
the multiplication of small cells, you can write code to model that process. If you
compositional thinking superimposes partials to create verticalities, you can write code
to model that process. If your compositional thinking operates in set-theoretic-like ways
on starting collections of pitches, you can write code to model that process. If your
compositional thinking foregrounds (historical or newly-conceived) dissonance handling,
you can write code to model the input/output and rules of your dissonance handling. If
your compositional thinking is informed by 20th-century ideas of mapping data
(statistical distributions, measurements from nature, corpus data from texts) to pitch or
rhythmic structures, you can write code to read different data sources and visualize the
results as notation. And if your compositional thinking involves writing notes one after
the other according to intuition, you can write code to capture the structure of your
intuitions, too.

However you decide to model your compositional thinking, you'll need to master Abjad's
basics of working with notes, rests, chords, tuplets, voices, staves and all the other
objects in a musical score. Broadly, you'll need to understand the interaction of five
core concepts as you learn to model compositional thinking in Abjad:

    * construction
    * inspection
    * iteration
    * encapsulation
    * mutation

You'll use the first three of these --- construction, inspection, iteration --- as the
everyday foundation of all the code you write in Abjad. Encapsulation will become
important as you graduate from making and managing musical objects to modeling your own
compositional thinking. And mutation concerns making powerful (but computationally
expensive) changes to the scores you build. All five concepts are important when you work
with Abjad and, indeed, when you working in any programming language, regardless of
application. The following sections provide an overview of Abjad structured according to
the these five ideas.
