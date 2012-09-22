Working with threads
====================


What is a thread?
-----------------

A thread is a structural relationship binding a set of strictly sequential voice-level components.

Threads may be explicitly defined via voice instances:

::

   >>> v = Voice()


Or they may exist implicitly in certain score constructs in the absence of voice containers:

::

   >>> staff = Staff("c'8 d'8 e'8 f'8")


Two contiguous voices must have the same name in order to be part of the same thread.

Here a thread does **not** exist between notes in different voices:

::

   >>> v_one = Voice("c'16 d'16 e'16 f'16")
   >>> v_two = Voice("c'8 d'8")
   >>> staff = Staff([v_one, v_two])
   >>> f(staff)
   \new Staff {
       \new Voice {
           c'16
           d'16
           e'16
           f'16
       }
       \new Voice {
           c'8
           d'8
       }
   }


Here a thread does exist:

::

   >>> v_one.name = 'flute'
   >>> v_two.name = 'flute'
   >>> f(staff)
   \new Staff {
       \context Voice = "flute" {
           c'16
           d'16
           e'16
           f'16
       }
       \context Voice = "flute" {
           c'8
           d'8
       }
   }


What are threads for?
---------------------

Consider the following situation:

.. image:: images/thread-resolution-1.png

Are the two eighth notes in the second half of the measure the continuation
of the ascending line in the first half, or is it the quarter note?
Is the very last *C* the continuation of the top melodic line or is it the *A*?
The stems might suggest an answer, but for Abjad, stem direction is not structural.
What path should Abjad take to traverse this little score from the first note to the last *A*?
This same problem appears when trying to apply spanners to parallel structures.
Thus, threads are important in both score navigation and the application of spanners.
In fact, threads are a requirement for spanner application.

In Abjad, the ambiguity is resolved through the explicit use of named voices.

The musical fragment above is constructed with the following code:

::

   >>> vA = Voice(notetools.make_notes([5, 7, 9, 11], [(1, 8)] * 4))
   >>> vB = Voice(notetools.make_notes([12, 11, 9], [(1, 8), (1, 8), (1, 4)]))
   >>> vC = Voice(Note(12, (1, 4)) * 2)
   >>> mark = marktools.LilyPondCommandMark('voiceOne')(vA[0])
   >>> mark = marktools.LilyPondCommandMark('voiceOne')(vB[0])
   >>> mark = marktools.LilyPondCommandMark('voiceTwo')(vC[0])
   >>> p = Container([vB, vC])
   >>> p.is_parallel = True
   >>> staff = Staff([vA, p])


::

   >>> f(staff)
   \new Staff {
       \new Voice {
           \voiceOne
           f'8
           g'8
           a'8
           b'8
       }
       <<
           \new Voice {
               \voiceOne
               c''8
               b'8
               a'4
           }
           \new Voice {
               \voiceTwo
               c''4
               c''4
           }
       >>
   }


::

   >>> show(staff, docs=True)

.. image:: images/index-1.png


There's a staff that sequentially contains a voice and a parallel container.
The container in turn holds two voices running simultaneously.

It is now clear from the code that the last *A* belongs with the two descending eighth notes.
But there's still no indication about a relationship of continuity between the first voice
in the sequence (`vA`) and any of the two following voices.
Note that, while the LilyPond voice number commands setting may suggest
that vA and vB belong together, this is not the case.
The LilyPond voice number commands simply set the direction of stems in printed output.

To see this more clearly, suppose we want to add a slur spanner starting on the
first note and ending on one of the last simultaneous notes.
To attach the slur spanner to the voices we could try either:

::

   >>> spannertools.SlurSpanner([vA, vB])
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/SlurSpanner/SlurSpanner.py", line 31, in __init__
       DirectedSpanner.__init__(self, components, direction)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/DirectedSpanner/DirectedSpanner.py", line 10, in __init__
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
       Spanner.__init__(self, components)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/Spanner/Spanner.py", line 42, in __init__
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
       self._initialize_components(components)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/Spanner/Spanner.py", line 213, in _initialize_components
       assert componenttools.all_are_thread_contiguous_components(leaves)
   AssertionError


... or ...

::

   >>> spannertools.SlurSpanner([vA, vC])
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/SlurSpanner/SlurSpanner.py", line 31, in __init__
       DirectedSpanner.__init__(self, components, direction)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/DirectedSpanner/DirectedSpanner.py", line 10, in __init__
       Spanner.__init__(self, components)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/Spanner/Spanner.py", line 42, in __init__
       self._initialize_components(components)
     File "/Users/josiah/Documents/Projects/abjad/trunk/abjad/tools/spannertools/Spanner/Spanner.py", line 213, in _initialize_components
       assert componenttools.all_are_thread_contiguous_components(leaves)
   AssertionError


But both raise a contiguity error.
Abjad needs to see an explicit connection between either `vA` and `vB` or between `vA` and `vC`.

Observe the behavior of the
:func:`~abjad.tools.iterationtools.iterate_thread_in_expr`
iterator on the `staff`:

::

   >>> vA_thread_signature = componenttools.component_to_containment_signature(vA)
   >>> notes = iterationtools.iterate_thread_in_expr(staff, Note, vA_thread_signature)
   >>> print list(notes)
   [Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8")]


::

   >>> vB_thread_signature = componenttools.component_to_containment_signature(vB)
   >>> notes = iterationtools.iterate_thread_in_expr(staff, Note, vB_thread_signature)
   >>> print list(notes)
   [Note("c''8"), Note("b'8"), Note("a'4")]


::

   >>> vC_thread_signature = componenttools.component_to_containment_signature(vC)
   >>> notes = iterationtools.iterate_thread_in_expr(staff, Note, vC_thread_signature)
   >>> print list(notes)
   [Note("c''4"), Note("c''4")]


In each case we are passing a different **thread signature** to the
:func:`~abjad.tools.iterationtools.iterate_thread_in_expr`
iterator, so each case returns a different list of notes.

We can see that the thread signature of each voice is indeed different
by printing it:

::

   >>> vA_thread_signature = componenttools.component_to_containment_signature(vA)
   >>> vA_thread_signature
   ContainmentSignature(Voice-25493808, Voice-25493808, Staff-25494192)


::

   >>> vB_thread_signature = componenttools.component_to_containment_signature(vB)
   >>> vB_thread_signature
   ContainmentSignature(Voice-25493936, Voice-25493936, Staff-25494192)


::

   >>> vC_thread_signature = componenttools.component_to_containment_signature(vC)
   >>> vC_thread_signature
   ContainmentSignature(Voice-25494064, Voice-25494064, Staff-25494192)


And by comparing them with the binary equality operator:

::

   >>> vA_thread_signature == vB_thread_signature
   False
   >>> vA_thread_signature == vC_thread_signature
   False
   >>> vB_thread_signature == vC_thread_signature
   False


To allow Abjad to treat the content of, say, voices `vA` and `vB` as belonging together,
we explicitly define a thread between them.
To do this  all we need to do is give both voices the same name:

::

   >>> vA.name = 'piccolo'
   >>> vB.name = 'piccolo'


Now `vA` and `vB` and all their content belong to the same thread:

::

   >>> vA_thread_signature == vB_thread_signature
   False


Note how the thread signatures have changed:

::

   >>> vA_thread_signature = componenttools.component_to_containment_signature(vA)
   >>> print vA_thread_signature
        staff: Staff-25494192
        voice: Voice-'piccolo'
         self: Voice-'piccolo'


::

   >>> vB_thread_signature = componenttools.component_to_containment_signature(vB)
   >>> print vB_thread_signature
        staff: Staff-25494192
        voice: Voice-'piccolo'
         self: Voice-'piccolo'


::

   >>> vC_thread_signature = componenttools.component_to_containment_signature(vC)
   >>> print vC_thread_signature
        staff: Staff-25494192
        voice: Voice-25494064
         self: Voice-25494064


And how the ``iterationtools.iterate_thread_in_expr()`` function returns
all the notes belonging to both `vA` and `vB` when passing it the full staff
and the thread signature of `vA`:

::

   >>> notes = iterationtools.iterate_thread_in_expr(staff, Note, vA_thread_signature)
   >>> print list(notes)
   [Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8"), Note("b'8"), Note("a'4")]


Now the slur spanner can be applied to voices `vA` and `vB`:

::

   >>> spannertools.SlurSpanner([vA, vB])
   SlurSpanner({f'8, g'8, a'8, b'8}, {c''8, b'8, a'4})


or directly to the notes returned by the
:func:`~abjad.tools.iterationtools.iterate_thread_in_expr`
iteration tool, which are the notes belonging to both `vA` and `vB`:

::

   >>> notes = iterationtools.iterate_thread_in_expr(staff, Note, vA_thread_signature)
   >>> spannertools.SlurSpanner(list(notes))
   SlurSpanner(f'8, g'8, a'8, b'8, c''8, b'8, a'4)


::

   >>> show(staff, docs=True)

.. image:: images/index-2.png


Coda
----

We could have constructed this score in a simpler way with only two voices,
one of them starting with a LilyPond skip:

::

   >>> vX = Voice(notetools.make_notes([5, 7, 9, 11, 12, 11, 9], [(1, 8)] * 6 + [(1, 4)]))
   >>> vY = Voice([skiptools.Skip((2, 4))] + Note(12, (1, 4)) * 2)
   >>> mark = marktools.LilyPondCommandMark('voiceOne')(vX[0])
   >>> mark = marktools.LilyPondCommandMark('voiceTwo')(vY[0])
   >>> staff = Staff([vX, vY])
   >>> staff.is_parallel = True


::

   >>> f(staff)
   \new Staff <<
       \new Voice {
           \voiceOne
           f'8
           g'8
           a'8
           b'8
           c''8
           b'8
           a'4
       }
       \new Voice {
           \voiceTwo
           s2
           c''4
           c''4
       }
   >>


::

   >>> show(staff, docs=True)

.. image:: images/index-3.png

