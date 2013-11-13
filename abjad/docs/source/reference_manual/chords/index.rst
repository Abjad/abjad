Chords
======

Making chords from a LilyPond input string
------------------------------------------

You can make chords from a LilyPond input string:

::

   >>> chord = Chord("<c' d' bf'>4")
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError



Making chords from numbers
--------------------------

You can also make chords from pitch numbers and duration:

::

   >>> chord = Chord([0, 2, 10], Duration(1, 4))
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError



Getting all the written pitches of a chord at once
--------------------------------------------------

You can get all the written pitches of a chord at one time:

::

   >>> chord.written_pitches
   (NamedPitch("c'"), NamedPitch("d'"), NamedPitch("bf'"))


Abjad returns a read-only tuple of named pitches.


Getting the written pitches of a chord one at a time
----------------------------------------------------

You can get the written pitches of a chord one at a time:

::

   >>> chord.written_pitches[0]
   NamedPitch("c'")


Chords index the pitch they contain starting from ``0``, just like tuples and
lists.


Adding one note head to a chord at a time
-----------------------------------------

Use ``append()`` to add one note head to a chord.

You can add a note head to a chord with a pitch number:

::

   >>> chord.note_heads.append(9)
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError


Or you can add a note head to a chord with a pitch name:

::

   >>> chord.note_heads.append("df''")
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError


Chords sort their note heads every time you add a new one.

This means you can add note heads to your chord in any order.


Adding many pitches to a chord at once
--------------------------------------

Use ``extend()`` to add many note heads to a chord.

You can use pitch numbers:

::

   >>> chord.note_heads.extend([3, 4, 14])
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError


Or you can use pitch names:

::

   >>> chord.note_heads.extend(["g''", "af''"])
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError



Deleting pitches from a chord
-----------------------------

Delete note heads from a chord with ``del()``:

::

   >>> del(chord.note_heads[0])
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError


Negative indices work too:

::

   >>> del(chord.note_heads[-1])
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError



Tweaking note heads
-------------------

You can tweak note heads like this:

::

   >>> chord.note_heads[2].tweak.color = 'red'
   >>> chord.note_heads[3].tweak.color = 'blue'
   >>> chord.note_heads[4].tweak.color = 'green'
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError



Working with empty chords
-------------------------

Abjad allows empty chords:

::

   >>> chord = Chord([], Duration(1, 4))
   >>> chord
   Chord('<>4')


But if you pass empty chords to ``show()`` LilyPond will complain
because empty chords don't constitute valid LilyPond input.

When you are done working with an empty chord you can add pitches back
into it chord in any of the ways described above:

::

   >>> chord.note_heads.extend(["gf'", "df''", "g''"])
   >>> show(chord)

::

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/trevorbaca/Documents/abjad/abjad/tools/agenttools/PersistenceAgent.py", line 81, in as_ly
       assert ly_filepath.endswith('.ly')
   AssertionError

