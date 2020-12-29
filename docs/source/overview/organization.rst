:orphan:

**Organization.** Abjad isn't a stand-alone application so much as an extension to an
existing programming language: learning Abjad doesn't mean mastering a reference manual;
learning Abjad means leveraging the techniques of programming to create PDFs of music
notation. If your compositional thinking derives musical phrases from the multiplication
of small cells, you can write code to model that process. If your compositional thinking
superimposes partials to create verticalities, you can write code to model that process.
If your compositional thinking operates in set-theoretic-like ways on starting
collections of pitches, you can write code to model that process. If your compositional
thinking foregrounds (historical or newly-conceived) dissonance handling, you can write
code to model the input/output and rules of your dissonance handling. If your
compositional thinking is informed by 20th-century ideas of mapping data (statistical
distributions, measurements from nature, corpus data from texts) to pitch or rhythmic
structures, you can write code to read different data sources and visualize the results
as notation. And if your compositional thinking involves writing notes according to
intuition, you can write code to capture the outlines of that process, too.

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
