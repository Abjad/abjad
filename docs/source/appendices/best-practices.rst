Best practices
==============

Incorporate the first group of best practices, below, while you're still learning Abjad.
Incorporate the second and third groups after you've composed a full score.

----

For beginners
-------------

**1. Write your code with a proper text editor.** It doesn't matter which one. But don't
use TextEdit or Notepad because they're not meant for editing code. And don't use Jupyter
notebooks because you'll confuse yourself by evaluating notebook cells out of order.

**2. Keep a test.py file handy at all times to try out small bits of code as you're
working.**

**3. Black the code you write.** Use Python's black module from the beginning. Beginners
spend a lot of time wondering about spacing and layout of code. That time can be cut to
zero by formatting your code automatically with black.

**4. Name all contexts.** 

..  container:: example

    Not so good: ::

        abjad.Voice()
        abjad.Staff()
        abjad.Score()

    Good: ::

        abjad.Voice(name="Upper_Voice")
        abjad.Staff(name="Violin_Staff")
        abjad.Score(name="Score")

**5. Contain notes, rests, chords in voices.** Rather than staves.

..  container:: example

    Not so good: ::

        abjad.Staff("c'4' d' e' f'", name="Violin_Staff")

    Good: ::

        abjad.Voice("c'4 d' e' f'", name="Music_Voice")

**6. Don't try to work with Abjad like GUI software: replace copy-and-paste with object
creation.**

..  container:: example

    Not so good: ::

        upper_voice = abjad.Voice("c'4 d' e' f'", name="Upper_Voice")
        lower_voice = abjad.mutate.copy(upper_voice)
        lower_voice.name = "Lower_Voice"

    Good: ::

        string = "c'4 d' e' f'"
        upper_voice = abjad.Voice(string, name="Upper_Voice")
        lower_voice = abjad.Voice(string, name="Lower_Voice")

**7. Externalize LilyPond markup in a separate file.** Rather than defining them with
Abjad.

..  container:: example

    Not so good: ::

        abjad.Markup(r'\markup \bold italic \font-size #4 "Allegro con moto"')

    Good: ::

        abjad.Markup(r"\my-score-allegro-con-moto")

**8. Externalize LilyPond context, layout, paper settings in a separate file.** Rather
than defining them with Abjad.

..  container:: example

    Not so good: ::

        abjad.setting(score).proportional_notation_duration = "#(ly:make-moment 1 32)"
        abjad.setting(score).spacing_spanner.strict_grace_spacing = True
        abjad.setting(score).spacing_spanner.strict_note_spacing = True
        abjad.setting(score).spacing_spanner.uniform_stretching = True

    Good: ::

        \context {
            \Score
            proportionalNotationDuration = #(ly:make-moment 1 32)
            \override SpacingSpanner.strict-grace-spacing = ##t
            \override SpacingSpanner.strict-note-spacing = ##t
            \override SpacingSpanner.uniform-stretching = ##t
        }

**9. Limit score mutation.** Copying, splitting, meter-rewriting and the like are
computationally expensive. You can do them. But limit how much.

**10. If you do mutate the score, do it early.** For example, rewrite meter before adding
many indicators; add articulations, slurs and the like after meter rewriting is done.

----

For intermediate users
----------------------

**1. Check everything into GitHub.** There's absolutely no good reason to forgo the
safekeeping that repositories provide. Right now the programmerly consensus strongly
favors Git (and GitHub), which we also recommend. However, **limit your use of Git to
four or five extremely simple workflows.** Because Git provides way too much rope with
which you can hang yourself. And because seemingly **no one** has a mental model of how
Git actually works. Many professional programmers seem to enjoy learning and using
advanced Git workflows. But absolutely do not do this. Add, commit, push, pull, clone,
that's it. Keep it as simple as possible.

**2. Log the number of seconds it takes to compile each segment in your score.** This
only takes three or four lines of code. Log how long it takes Abjad to interpret your
score segment. And log how long it takes LilyPond to interpret your score segment. Round
these numbers to the nearest second. Write the results to a file dedicated to the
purpose. Keep one timing file per score segment. Check your timing files into GitHub. You
won't need to check your timing files very often. But if you ever experience a
performance slow-down in your code, your timing files will provide crucial information to
help you debug.

**3. Maintain a library of functions and other tools you use in multiple scores.** Such a
library models parts of your compositional practice that apply across different scores
you compose. Write doctests for every function in your composition library.

**4. Output test your score segments.** Use pytest to check that each segment in your
score writes exactly the same LilyPond file after a code change as before. This is easy
to do. This is also the only way you can refactor your composition library while making
sure that every single note in every single one of your existing scores remains the same.
This is an extremely important practice for intermediate users.

**5. Do not bother typehinting your code when you first start working with Python.** In
fact, it will probably never be worth the effort to typehint your code. Abjad's codebase
is typehinted, it is true. But experience shows that there appears to be almost no
benefit for Abjad users to typehint their own code. This means that mypy is one tool in
the Python ecosystem you can safely ignore.

----

For advanced users
------------------

**1. Limit score segments to 2--4 pages of music.** Performance and debugging will always
be easier. On the other hand, smaller score segments mean that you will have more work to
do managing clefs, key signatures and other persistent indicators across segment
boundaries. But the tradeoff is worth it.

**2. Limit unnecessary object orientation.** The Python language designers have always
advised this. In Java, C++ and other languages, the unit of architecture is the class. In
Python, the unit of architecture is the module: this is why architecting in Python
doesn't mean encapsulating absolutely everything you write in a class. The reason this
works is because Python's idea of a namespace is so incredibly powerful: Python's modules
were already inherently class-like before the addition to classes to the language.
Classes can still play an important role in the way your structure your code in Python,
of course. But the language itself will lead you towards architecting your code in
modules, not least for reasons of the central role played by Python's import mechanism;
see below.

**3. Acknowledge the central role played by Python's import mechanism in the structure of
any system written in Python.** Initially this can be frustrating. If you define classes
A and B in separate modules then A may import B, or B may import A, but never both
without creating a circular dependency between the modules. On the other hand, if you
define classes A and B in the same module, then A and B can do whatever they want to /
with each other. The reason for this asymmetry is entirely to do with the central role
played by Python's import mechanism: Python is designed to import packages once and once
only, and this fact limits collaboration patterns between the classes you write.
Practically, what this means is that you should be ok architecting your code a module
full of code, followed later by another module full of code. Dependencies between modules
then tend to show the chronological order modules were implemented. All these points
manifestly confuse beginners, as questions asked about module reimports on Stackoverflow
show. But these things all result from working in an interpreted, rather than compiled,
language: taking the order of interpretation seriously means constraining the way code is
layed out into modules on the filesystem.

**4. Run the Python profiler on your code every once in a while.** To check the
performance of the code you write. Always profile before you optimize your code.

:author:`[Bača (3.2)]`
