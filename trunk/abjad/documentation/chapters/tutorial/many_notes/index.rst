Making many notes
=================

Abjad overloads the Python multiplication `*` operator to copy notes,
rests and other system objects.

.. sourcecode:: python

    
    abjad> my_notes = Note(0, (1, 8)) * 4


The `my_notes` variable is now bound to a Python list of four Abjad
notes.

.. sourcecode:: python

    
    abjad> my_notes
    [Note(c', 8), Note(c', 8), Note(c', 8), Note(c', 8)]


These four notes are all truly different from one another. [#f2]_

All the usual Python list operations are available.

.. sourcecode:: python

    
    abjad> len(my_notes)
    4






.. [#f2] By "truly different" we mean that each of the four notes in the example above have a separate ID in the Abjad interpreter. You can see this by asking, for example, for `id(my_notes[0])` and `id(my_notes[1])`. Different IDs will come back in each case. This is important for two reasons. First, the usual Python multiplication operator acts to multiply references, rather than deep copying instances as happens here. Second, as you build more complex musical expressions, it will be important that notes, rests and all components be unique throughout complex score structure to prevent accidental aliasing of elements.
