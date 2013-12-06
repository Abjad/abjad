Designing Abjad 2.14
====================

Top-level functions, system protocol, parameterized tests
---------------------------------------------------------


Trevor: How visible do you think the new code in 2.14 will be for composers
already using Abjad?

Josiah: It's a good question. We've moved a lot of code around in 2.14.  The
``componenttools``, ``leaftools``, ``notetools``, ``resttools``, ``chordtools``
and ``tuplettools`` packages have all been merged into ``scoretools``.
package.

Trevor: Which means ``Note``, ``Rest``, ``Chord`` and so on are all now housed
in a single package.

Josiah: And we've replaced ``iterationtools`` with the new ``iterate()``
function.

Trevor: And ``iotools`` with ``persist()``.

Josiah: Those changes will probably be more noticeable to existing users
because most scores probably involve iteration. So users will have to change
from thinking ``iterationtools.iterate_notes_in_expr(voice)`` to
``iterate(voice).iterate_by_class(Note)``. Which is a cleaner way of getting to
the core iteration functionality anyway.

Trevor: Same with ``mutate()`` and ``inspect()``. Just those two functions
offer up a tremendous amount of functionality.

Josiah: We should highlight ``InspectionAgent``, ``IterationAgent``,
``MutationAgent`` and ``PersistenceAgent``. I feel pretty good about all of
these changes, actually. I feel like this is a release of the system is really
solid.

Trevor: We're almost there. We've removed something like 500 classes from
public view in 2.13 and 2.14. And almost as many function.  The learnability of
the API is now dramatically higher than it's even been before.

Josiah: Even the typographic details of the code are better 2.14. I think we've
implemented almost everywhere the pattern of putting everything on its own line
and putting commas after every single expression. The The diffs are smaller and
easier to read if you're watching the commits come into the repository during
development.

Trevor: Also, the illustration protocol is really cool.

Josiah: Almost everything implements ``__illustrate__()`` now.

Trevor: Previously you could only ``show(note)`` and ``show(tuplet)`` and
``show(score)``. But now you can ``show(named_pitch)`` and ``show(markup)`` and
even ``show(clef_inventory)``. It's powerful to be able to view so many parts
of the system as music notation.

Josiah: I started adding those sorts of things into the ``pitchtools``
collection classes when I was cleaning up the classes for this release.
(Classes like ``pitchtools.Set`` and ``pitchtools.Segment``.) It just makes
sense that you'd want to be able to see the pitches and pitch-classes that
you're working with as you build up sets and segments.

Trevor: Just like it makes sense to be able to see notation corresponding to
the clefs, range and name markup of all the different instruments. It took
awhile to llustrate all the instrument classes. But the ``instrumenttools`` API
is better because of it.

Josiah: We've got a number of different types of protocol in the system now.

Josiah: The illustration protocol. The copy protocol.

Trevor: The persistence protocol. The attachment protocol.

Josiah: The iteration protocol. The override protocol. The format protocol.

Trevor: The make-new protocol.

Josiah: The make-new protocol is a good one. We'll have to starting working the
top-level ``new()`` function into examples. So that users can start to see it
in action.

Trevor: All the functions in ``topleveltools`` deserve some attention:
``attach()`` and ``detach()`` to stick clefs and time signatures to the side of
things; ``show()`` to show most things in the system; ``mutate()`` to make big
changes to the score.

Josiah: ``persist()`` to write all sorts of objects to disk; ``new()`` to make
new objects with optional changes.

Trevor: ``graph()`` to look at Graphviz pictures of things.

Josiah: The system has evolved to a point where a number of protocols are
pretty important for how we do things.  Essentially the entire formatting
regime is protocol. I guess we didn’t notice this upfront because the idea of a
protocol is pretty unique to Python.

Trevor: I like that we've extended the Abjad initializer so that functions in
``topleveltools`` are all loaded into the global namespace now by default. You
can just say ``attach()``, ``detach()``, ``graph()``, ``new()``, ``persist()``
and so on without having to import anything from anywhere.

Josiah: Same with ``Articulation``, ``Clef``, ``KeySignature`` and
``TimeSignature``. It's really nice to be able to say ``Clef('bass')`` without
having to worry about first importing ``Clef`` from somewhere.

Trevor: Right.

Josiah: The protocols are really helping write tests, too. I remember you put
in an issue recently: Shouldn’t we have a parameterized test that looks at
everything that has a storage format and tries to make it write the storage
format out, read the storage format back in and compare the equality of the two
things?

Trevor: Exactly.

Josiah: Those tests exist now.

Trevor: Thanks to the ``pytest`` team giving us the
``@pytest.mark.parameterize`` decorator. 

Josiah: Which is what makes all the new tests in the ``tools/tests`` directory
work.

Trevor: Right.

Josiah: Have you given any thought to the new keyword-only arguments
available in Python 3.0? Seems like many of the classes and functions now
implemented in Abjad could benefit from being made keyword-only when we migrate
to Python 3.0 later next year.

Trevor: I agree. Many of the more powerful classes in the system -- the
rhythm-makers, the quantizer, the instrument classes -- allow for a number of
input parameters. It makes sense to document the names of the input parameters
everywhere. And the keyword-only arguments in Python 3.0 can help us enforce
the pattern completely cleanly. It seems like a reasonable path would be to
migrate all examples, all tests and all parts of the reference manual to
keyword only sometime during the development of a major release in 2014. And
then to enforce keyword-only arguments in the following major release.

Josiah: To show how the arguments will work in the documentation one
release before requiring composers to start following the pattern.

[December 2013]
