Overriding LilyPond grobs
=========================

LilyPond models music notation as a collection of graphic objects or grobs.


Grobs control typography
------------------------

LilyPond grobs control the typographic details of the score:

..  abjad::

    staff = Staff("c'4 ( d'4 ) e'4 ( f'4 ) g'4 ( a'4 ) g'2")

..  abjad::

    print(format(staff))

..  abjad::

    show(staff)

In the example above LilyPond creates a grob for every printed glyph.  This
includes the clef and time signature as well as the note heads, stems and
slurs. If the example included beams, articulations or an explicit key
signature then LilyPond would create grobs for those as well.


Abjad grob-override component plug-ins
--------------------------------------

Abjad lets you work with LilyPond grobs.

All Abjad containers have a grob-override plug-in:

..  abjad::

    staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 g'2")
    show(staff)

..  abjad::

    override(staff).staff_symbol.color = 'blue'

..  abjad::

    show(staff)

All Abjad leaves have a grob-override plug-in, too:

..  abjad::

    leaf = staff[-1]

..  abjad::
    
    override(leaf).note_head.color = 'red'
    override(leaf).stem.color = 'red'

..  abjad::

    show(staff)

And so do Abjad spanners:

..  abjad::

    slur = Slur()
    attach(slur, staff[:])
    override(slur).slur.color = 'red'

..  abjad::

    show(staff)


Nested Grob properties can be overriden
---------------------------------------

In the above example, `staff_symbol`, `note_head` and `stem` correspond to the
LilyPond grobs `StaffSymbol`, `NoteHead` and `Stem`, while `color` in each case
is the color properties of that graphic object.

It is not uncommon in LilyPond scores to see more complex overrides, consisting
of a grob name and a list of two or more property names:

::

    \override StaffGrouper #'staff-staff-spacing #'basic-distance = #7

To achieve the Abjad equivalent, simply concatenate the property names with
double-underscores:

..  abjad::

    staff = Staff()
    override(staff).staff_grouper.staff_staff_spacing__basic_distance = 7
    print(format(staff))

Abjad will explode the double-underscore delimited Python property into a
LilyPond property list.


Check the LilyPond docs
-----------------------

New grobs are added to LilyPond from time to time.

For a complete list of LilyPond grobs see the `LilyPond documentation
<http://lilypond.org/doc/v2.13/Documentation/internals/all-layout-objects>`__.
