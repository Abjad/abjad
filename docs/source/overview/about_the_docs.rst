About the docs
==============

Abjad isn't a stand-alone application so much as an extension to an existing programming
language: learning Abjad doesn't mean mastering a reference manual; learning Abjad means
leveraging the techniques of programming to create PDFs of music notation. If your
compositional thinking derives musical phrases from the multiplication of small cells,
you can write code to model that process. If your compositional thinking superimposes
partials to create verticalities, you can write code to model that process. If your
compositional thinking operates in set-theoretic-like ways on starting collections of
pitches, you can write code to model that process. If your compositional thinking
foregrounds (historical or newly-conceived) dissonance handling, you can write code to
model the input/output and rules of your dissonance handling. If your compositional
thinking is informed by 20th-century ideas of mapping data (statistical distributions,
measurements from nature, corpus data from texts) to pitch or rhythmic structures, you
can write code to read different data sources and visualize the results as notation. And
if your compositional thinking involves writing notes according to intuition, you can
write code to capture the outlines of that process, too.

However you decide to model your compositional thinking, you'll need to master the basics
of notes, rests, chords, tuplets, voices, staves, scores in Abjad. You'll also need to
develop an understanding of five concepts:

    * construction
    * inspection
    * iteration
    * encapsulation
    * mutation

You'll use the first three of these --- construction, inspection, iteration --- as the
everyday basics of the code you write. Encapsulation becomes important when you start to
model compositional procedures you do on a repeated basis --- when you move from writing
code to architecting code. Mutation concerns making broad, but computationally expensive,
changes to your work. The sections of the overview that follow are organized according to
these ideas.

----

**Prerequisites.** Abjad's docs assume an understanding of both LilyPond and Python. If
you become serious about composing with Abjad, make sure you've worked completely through
both systems' tutorials:

https://lilypond.org/doc/v2.20/Documentation/learning/tutorial 

https://docs.python.org/3/tutorial/

----

**LilyPond settings.** LilyPond examples in Abjad's docs are styled in a particular way:
notes, rests, chords are spaced proportionally; there are no bar numbers; tuplet numbers
are cleaned up; and so on. If you want to style in this same way the examples you try out
while reading Abjad's docs, download Abjad's default stylesheet and include it in the
examples you create:

https://github.com/Abjad/abjad/tree/master/docs/source/_stylesheets/default.ily
