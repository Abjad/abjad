Articulations
=============

Articulations model staccati, marcati, tenuti and other symbols.
Articulations attach notes, rests or chords.


Creating articulations
----------------------

Use ``marktools`` to create articulations:

::

	articulation = marktools.Articulation('marcato')


::

	abjad> articulation
	Articulation('marcato', '-')



Attaching articulations to leaves
---------------------------------

Use ``attach()`` to attach any articulation to a leaf:

::

	abjad> staff = Staff("c'4 d'4 e'4 f'4")


::

	abjad> articulation.attach(staff[0])


::

	abjad> show(staff)

.. image:: images/articulations-1.png


Getting the articulations attached to a leaf
--------------------------------------------

Use ``marktools`` to get the articulations attached to a leaf:

::

	abjad> marktools.get_articulations_attached_to_component(staff[0])
	(Articulation('marcato', '-')(c'4),)



Detaching articulations from a leaf one at a time
-------------------------------------------------

Detach articulations by hand with ``detach_mark()``:

::

	abjad> articulation.detach_mark()


::

	abjad> articulation
	-\marcato


::

	abjad> show(staff)

.. image:: images/articulations-2.png


Detaching all articulations attached to a leaf at once
------------------------------------------------------

Use ``marktools`` to detach all articulations attached to a leaf at once:

::

	abjad> articulation_1 = marktools.Articulation('marcato')
	abjad> articulation_1.attach(staff[0])


::

	abjad> articulation_2 = marktools.Articulation('staccato')
	abjad> articulation_2.attach(staff[0])


::

	abjad> show(staff)

.. image:: images/articulations-3.png

::

	abjad> marktools.detach_articulations_attached_to_component(staff[0])


::

	abjad> show(staff)

.. image:: images/articulations-4.png


Inspecting the leaf to which an articulation is attached
--------------------------------------------------------

Use ``start_component`` to inspect the component to which an articulation is attached:

::

	abjad> articulation = marktools.Articulation('marcato')
	abjad> articulation.attach(staff[0])


::

	abjad> show(staff)

.. image:: images/articulations-5.png

::

	abjad> articulation.start_component
	Note("c'4")



Controling whether an articulation appears above or below the staff
-------------------------------------------------------------------

Set ``direction_string`` to ``'^'`` to force an articulation to appear
above the staff:

::

	abjad> articulation.direction_string = '^'


::

	abjad> show(staff)

.. image:: images/articulations-6.png

Set ``direction_string`` to ``'_'`` to force an articulation to appear
above the staff:

::

	abjad> articulation.direction_string = '_'


::

	abjad> show(staff)

.. image:: images/articulations-7.png

Set ``direction_string`` to ``'-'`` to allow LilyPond to position
an articulation automatically:

::

	abjad> articulation.direction_string = '-'


::

	abjad> show(staff)

.. image:: images/articulations-8.png


Getting and setting articulation name
-------------------------------------

Set the ``name_string`` of an articulation to change the symbol an articulation prints:

::

	abjad> articulation.name_string = 'staccatissimo'


::

	abjad> show(staff)

.. image:: images/articulations-9.png


Copying articulations
---------------------

Use ``copy.copy()`` to copy an articulation:

::

	abjad> import copy


::

	abjad> articulation_copy_1 = copy.copy(articulation)


::

	abjad> articulation_copy_1
	Articulation('staccatissimo', '-')


::

	abjad> articulation_copy_1.attach(staff[1])


::

	abjad> show(staff)

.. image:: images/articulations-10.png

Or use ``copy.deepcopy()`` to do the same thing:

::

	abjad> articulation_copy_2 = copy.deepcopy(articulation)


::

	abjad> articulation_copy_2
	Articulation('staccatissimo', '-')


::

	abjad> articulation_copy_2.attach(staff[2])


::

	abjad> show(staff)

.. image:: images/articulations-11.png


Comparing articulations
-----------------------

Articulations compare equal with equal direction name strings and direction strings:

::

	abjad> articulation.name_string
	'staccatissimo'
	abjad> articulation.direction_string
	'-'


::

	abjad> articulation_copy_1.name_string
	'staccatissimo'
	abjad> articulation_copy_1.direction_string
	'-'


::

	abjad> articulation == articulation_copy_1
	True


Otherwise articulations do not compare equal.
