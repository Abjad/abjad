LilyPond command marks
======================

LilyPond command marks allow you to attach arbitrary LilyPond commands
to Abjad score components.


Creating LilyPond command marks
-------------------------------

Use ``marktools`` to create LilyPond command marks:

::

	abjad> lilypond_command_mark = marktools.LilyPondCommandMark('bar "||"', 'after')


::

	abjad> lilypond_command_mark
	LilyPondCommandMark('bar "||"')



Attaching LilyPond command marks to Abjad components
----------------------------------------------------

Use ``attach()`` to attach a LilyPond command mark to any Abjad component:

::

	abjad> import copy
	abjad> staff = Staff([])
	abjad> key_signature = contexttools.KeySignatureMark('f', 'major')
	abjad> key_signature.attach(staff)
	abjad> staff.extend(iotools.parse_lilypond_input_string("d''16 ( c''16 fs''16 g''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("f''16 ( e''16 d''16 c''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("cs''16 ( d''16 f''16 d''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("a'8 b'8"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("d''16 ( c''16 fs''16 g''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("f''16 ( e''16 d''16 c''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("cs''16 ( d''16 f''16 d''16 )"))
	abjad> staff.extend(iotools.parse_lilypond_input_string("a'8 b'8 c''2"))


::

	abjad> lilypond_command_mark.attach(staff[-2])


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-1.png


Getting the LilyPond command marks attached to an Abjad component
-----------------------------------------------------------------

Use ``marktools`` to get the lilypond_command_marks attached to a leaf:

::

	abjad> marktools.get_lilypond_command_marks_attached_to_component(staff[-2])
	(LilyPondCommandMark('bar "||"')(b'8),)



Detaching LilyPond command marks from components one at a time
--------------------------------------------------------------

Use ``detach()`` to detach LilyPond command marks one at a time:

::

	abjad> lilypond_command_mark.detach()


::

	abjad> lilypond_command_mark
	LilyPondCommandMark('bar "||"')


::

	abjad> show(staff)

.. image:: images/lilpond-command-marks-2.png


Detaching all LilyPond command marks attached to a component at once
--------------------------------------------------------------------

Use ``marktools`` to detach all LilyPond command marks attached to a component at once:

::

	abjad> lilypond_command_mark_1 = marktools.LilyPondCommandMark('bar "||"', 'closing')
	abjad> lilypond_command_mark_1.attach(staff[-2])


::

	abjad> lilypond_command_mark_2 = marktools.LilyPondCommandMark('bar "||"', 'closing')
	abjad> lilypond_command_mark_2.attach(staff[-16])


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-3.png

::

	abjad> marktools.detach_lilypond_command_marks_attached_to_component(staff[-16])


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-4.png


Inspecting the component to which a LilyPond command mark is attached
---------------------------------------------------------------------

Use ``start_component`` to inspect the component to which a LilyPond command mark is attached:

::

	abjad> lilypond_command_mark = marktools.LilyPondCommandMark('bar "||"', 'closing')
	abjad> lilypond_command_mark.attach(staff[-2])


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-5.png

::

	abjad> lilypond_command_mark.start_component
	Note("b'8")



Getting and setting the command name of a LilyPond command mark
---------------------------------------------------------------

Set the ``command_name`` of a LilyPond command mark to change the 
LilyPond command a LilyPond command mark prints:

::

	abjad> lilypond_command_mark.command_name = 'bar "|."'


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-9.png


Copying LilyPond commands
-------------------------

Use ``copy.copy()`` to copy a LilyPond command mark:

::

	abjad> import copy


::

	abjad> lilypond_command_mark_copy_1 = copy.copy(lilypond_command_mark)


::

	abjad> lilypond_command_mark_copy_1
	LilyPondCommandMark('bar "|."')


::

	abjad> lilypond_command_mark_copy_1.attach(staff[-1])


::

	abjad> show(staff)

.. image:: images/lilypond-command-marks-10.png

Or use ``copy.deepcopy()`` to do the same thing.


Comparing LilyPond command marks
--------------------------------

LilyPond command marks compare equal with equal command names:

::

	abjad> lilypond_command_mark.command_name
	'bar "|."'


::

	abjad> lilypond_command_mark_copy_1.command_name
	'bar "|."'


::

	abjad> lilypond_command_mark == lilypond_command_mark_copy_1
	True


Otherwise LilyPond command marks do not compare equal.
