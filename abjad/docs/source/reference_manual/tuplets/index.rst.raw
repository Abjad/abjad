Tuplets
=======


Making a tuplet from a LilyPond input string
--------------------------------------------

You can create tuplets from a LilyPond input string:

<abjad>
tuplet = Tuplet(Multiplier(2, 3), "c'8 d'8 e'8")
show(tuplet)
</abjad>


Making a tuplet from a list of other components
-----------------------------------------------

You can also make tuplets from a list of other components:

<abjad>
leaves = [Note("fs'8"), Note("g'8"), Rest('r8')]
tuplet = Tuplet(Multiplier(2, 3), leaves)
show(tuplet)
</abjad>


Understanding the interpreter representation of a tuplet
--------------------------------------------------------

The interprer representation of an tuplet contains three parts:

<abjad>
tuplet
</abjad>

``Tuplet`` tells you the tuplet's class.

``Multiplier(2, 3)`` tells you the tuplet's multiplier.

``[fs'8, g'8, r8]`` tells you the top-level components the tuplet contains.


Understanding the string representation of a tuplet
---------------------------------------------------

The string representation of a tuplet contains four parts:

<abjad>
print tuplet
</abjad>

Curly braces ``{`` and ``}`` indicate that the tuplet's music is interpreted
sequentially instead of simultaneously.

The asterisks ``*`` denote a fixed-multiplier tuplet.

``3:2`` tells you the tuplet's ratio.

The remaining arguments show the top-level components of tuplet.


Formatting tuplets
------------------

Use ``format()`` to get the LilyPond format a tuplet:

<abjad>
print format(tuplet, 'lilypond')
</abjad>


Selecting the music in a tuplet
-------------------------------

Select the music in a tuplet like this:

<abjad>
tuplet[:]
</abjad>


Selecting a tuplet's leaves
---------------------------

Use ``select_leaves()`` to get the leaves in a tuplet:

<abjad>
tuplet.select_leaves()
</abjad>


Getting the length of a tuplet
------------------------------

Use ``len()`` to get the length of a tuplet.

The length of a tuplet is defined equal to the number of top-level components
the tuplet contains:

<abjad>
len(tuplet)
</abjad>


Inspecting tuplet duration
--------------------------

Use the inspector to get the duration of a tuplet:

<abjad>
inspect_(tuplet).get_duration()
</abjad>


Understanding rhythmic augmentation and diminution
--------------------------------------------------

A tuplet with a multiplier less than ``1`` constitutes a type of rhythmic
diminution:

<abjad>
tuplet.multiplier
</abjad>

<abjad>
tuplet.is_diminution
</abjad>

A tuplet with a multiplier greater than ``1`` is a type of rhythmic
augmentation:

<abjad>
tuplet.is_augmentation
</abjad>


Getting and setting the multiplier of a tuplet
----------------------------------------------

Get the multiplier of a tuplet like this:

<abjad>
tuplet.multiplier
</abjad>

Set the multiplier of a tuplet like this:

<abjad>
tuplet.multiplier = Multiplier(4, 5)
show(tuplet)
</abjad>


Appending one component to the end of a tuplet
----------------------------------------------

Use ``append()`` to append one component to the end of a tuplet:

<abjad>
tuplet.append(Note("e'4."))
show(tuplet)
</abjad>

You can also use a LilyPond input string:

<abjad>
tuplet.append("bf8")
show(tuplet)
</abjad>


Extending a tuplet with multiple components at once
---------------------------------------------------

Use ``extend()`` to extend a tuplet with multiple components at once:

<abjad>
notes = [Note("fs'32"), Note("e'32"), Note("d'32"), Rest((1, 32))]
tuplet.extend(notes)
show(tuplet)
</abjad>

You can also use a LilyPond input string:

<abjad>
tuplet.extend("gs'8 a8") 
show(tuplet)
</abjad>


Finding the index of a component in a tuplet
--------------------------------------------

Use ``index()`` to find the index of any component in a tuplet:

<abjad>
notes[1]
</abjad>

<abjad>
tuplet.index(notes[1])
</abjad>


Popping a tuplet component by index
-----------------------------------

Use ``pop()`` to remove the last component of a tuplet:

<abjad>
tuplet.pop()
show(tuplet)
</abjad>


Removing a tuplet component by reference
----------------------------------------

Use ``remove()`` to remove any component from a tuplet by reference:

<abjad>
tuplet.remove(tuplet[3])
show(tuplet)
</abjad>


Overriding attributes of the LilyPond tuplet number grob
--------------------------------------------------------

Override attributes of the LilyPond tuplet number grob like this:

<abjad>
string = 'tuplet-number::calc-fraction-text'
scheme = schemetools.Scheme(string)
override(tuplet).tuplet_number.text = scheme
override(tuplet).tuplet_number.color = 'red'
staff = Staff([tuplet])
show(staff)
</abjad>

See LilyPond's documentation for lists of grob attributes available.


Overriding attributes of the LilyPond tuplet bracket grob
---------------------------------------------------------

Override attributes of the LilyPond tuplet bracket grob like this:

<abjad>
override(tuplet).tuplet_bracket.color = 'red'
show(staff)
</abjad>

See LilyPond's documentation for lists of grob attributes available.
