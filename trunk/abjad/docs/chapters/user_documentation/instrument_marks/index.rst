Instrument marks
================

Instrument marks appear as instrument names in the left margin of your score.

Creating instrument marks
-------------------------

Use context tools to create instrument marks:

::

	abjad> violin = contexttools.InstrumentMark('Violin ', 'Vn. ')


::

	abjad> violin
	InstrumentMark('Violin ', 'Vn. ')


Attaching instrument marks
--------------------------

Attach instrument marks like this:

::

	abjad> staff = Staff("c'4 d'4 e'4 f'4")


::

	abjad> violin.attach_mark(staff)


::

	abjad> show(staff)
	abjad> iotools.write_expr_to_ly(staff, 'instrument-marks-1')

.. image:: images/instrument-marks-1.png


Example
-------

Use context tools to add instrument marks:

::

	abjad> flute_staff = Staff("c'8 d'8 e'8 f'8")
	abjad> violin_staff = Staff("c'8 d'8 e'8 f'8")
	abjad> staff_group = scoretools.StaffGroup([flute_staff, violin_staff])
	abjad> score = Score([staff_group])
	abjad> contexttools.InstrumentMark('Flute ', 'Fl. ')(flute_staff)
	abjad> contexttools.InstrumentMark('Violin ', 'Vn. ')(violin_staff)


Instrument marks appear as context settings in LilyPond input:

::

	abjad> f(score)
	\new Score <<
		\new StaffGroup <<
			\new Staff {
				\set Staff.instrumentName = \markup { Flute  }
				\set Staff.shortInstrumentName = \markup { Fl.  }
				c'8
				d'8
				e'8
				f'8
			}
			\new Staff {
				\set Staff.instrumentName = \markup { Violin  }
				\set Staff.shortInstrumentName = \markup { Vn.  }
				c'8
				d'8
				e'8
				f'8
			}
		>>
	>>


Instrument marks appear as instrument names in notational output:

::

	abjad> show(score)

.. image:: images/instrument-marks-2.png
