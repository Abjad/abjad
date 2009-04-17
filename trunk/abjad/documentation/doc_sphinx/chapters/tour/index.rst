Start here
==========

Work through the examples here to learn how to start Abjad and to make
notes, rests and chords. After you know the basics you can move on to
more advanced examples.


1. Start Abjad
--------------

To start Abjad, type `abj` at any shell prompt. [1] The Abjad
intepreter appears.

.. sourcecode:: python

    
    abjad> 


That's all there is to starting Abjad! Notice that all you have to
type are the three letters `abj` rather than the full five letters in
the name of the system.

What if the Abjad interpreter doesn't start? See the page on making
sure Abjad is installed correctly; link to be provided soon.



2. Make one note
----------------
To create one note, type code like the following and hit return.

.. sourcecode:: python

    
    abjad> Note(13, (1, 4))
    Note(c'', 4)

Abjad responds by showing you the note you have created. Here we've
created a C-sharp in the octave just above middle C with a duration of
a quarter note. (Abjad pitch numbers are equal to the IRCAM / MIDI
pitch numbers minus 60.) It's probably easiest to save the new note
that you've created to a variable name. You can do this with the
special Python `_` underscore character.

.. sourcecode:: python

    
    abjad> my_note = _

Python interpreters the special `_` underscore character to mean "the
last thing just returned from the interpreter". Here the `my_note`
variable now equals the C-sharp we created earlier. Any time we type
`my_note` followed by return, Abjad will show us this note.

.. sourcecode:: python

    
    abjad> my_note
    Note(cs'', 4)

Of course you can also combine the two steps we've gone through above
into a single step.

.. sourcecode:: python

    
    abjad> my_note = Note(13, (1, 4))

Abjad instantiates the C-sharp on the right-hand side of the equals
sign and then binds the newly-created note to the variable `my_note`
on the left-hand side of the equals sign. The equals sign `=` is the
Python assignment operator. And, as before, any time we type `my_note`
followed by return, Abjad will show us this note.

.. sourcecode:: python

    
    abjad> my_note
    Note(cs'', 4)


Why is it useful to assign notes, rests and other Abjad objects that
you create to variable names? Because once you have assigned a note,
rest or other Abjad object to a variable name, you can inspect the
different attributes of that object and use that object to build more
complex musical expressions.

.. sourcecode:: python

    
    abjad> my_note.pitch
    Pitch(cs, 5)


Here we ask for the pitch of `my_note` and find out that `my_note` has
a pitch equal to C-sharp in the octave above middle C.

.. sourcecode:: python

    
    abjad> my_note.pitch.accidental
    Accidental(s)


Here we ask for the accidental attaching to the pitch of `my_note`. We
find out that the accidental attaching to the pitch of `my_note` is a
sharp sign, here denoted by the string `'s'`.

.. sourcecode:: python

    
    abjad> my_note.duration.written
    Rational(1, 4)


And here we ask for the written duration of `my_note`. We find out
that the written duration of `my_note` is 1/4 .

In this section we've learned how to create one note and assign that
note to a variable name. We've also looked at just a few of the many
dozen different structural attributes that Abjad makes available for
the different objects in the system. In the next section we'll look at
a few ways to make many notes at once.



3. Make many notes
------------------

Abjad overloads the Python multiplication `*` operator to copy notes,
rests and other system objects.

.. sourcecode:: python

    
    abjad> my_notes = Note(0, (1, 8)) * 4


The `my_notes` variable is now bound to a Python list of four Abjad
notes.

.. sourcecode:: python

    
    abjad> my_notes
    [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]


These four notes are all truly different from one another. [2]

All the usual Python list operations are available.

.. sourcecode:: python

    
    abjad> len(my_notes)
    4


And you can use the Abjad `f( )` helper to look at all four notes
formatted as LilyPond input.

.. sourcecode:: python

    
    abjad> f(my_notes)
    c'8
    c'8
    c'8
    c'8


You can not, however, use the Abjad `show( )` helper to show a Python
list of notes. Try putting these notes in an Abjad staff first. This
is the subject of the next section.



Comments
^^^^^^^^

1: On Mac OS X you can get a shell prompt using the Terminal
application. The terminal application lives at
`/Applications/Utilities`. It's probably a good a idea to drag the
Terminal application to your dock so that the application is easy to
get to and easy to start. Once you've found the Terminal application,
click it and type `abj` to start Abjad.

2: By "truly different" we mean that each of the four notes in the
example above have a separate ID in the Abjad interpreter. You can see
this by asking, for example, for `id(my_notes[0])` and
`id(my_notes[1])`. Different IDs will come back in each case. This is
important for two reasons. First, the usual Python multiplication
operator acts to multiply references, rather than deep copying
instances as happens here. Second, as you build more complex musical
expressions, it will be important that notes, rests and all components
be unique throughout complex score structure to prevent accidental
aliasing of elements.


