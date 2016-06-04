Creating custom musical symbols with markup
===========================================

Building basic shapes with markup
---------------------------------

..  abjad::

    mallet_stick = Markup.draw_line(0, -6)
    mallet_head = Markup.filled_box((-1, 1), (-1, 1))
    square_mallet = Markup.combine(mallet_stick, mallet_head)
    print(format(square_mallet))
    show(square_mallet)

..  abjad::

    mallet_stick = Markup.draw_line(0, -6)
    mallet_head = Markup.filled_box((-1, 1), (-1, 1), blot=1)
    square_mallet = Markup.combine(mallet_stick, mallet_head)
    print(format(square_mallet))
    show(square_mallet)

..  abjad::

    mallet_stick = Markup.draw_line(0, -6)
    mallet_head = Markup.draw_circle(2, 0.5)
    round_mallet = Markup.combine(mallet_stick, mallet_head)
    print(format(round_mallet))
    show(round_mallet)

..  abjad::

    mallet_stick = Markup.draw_line(0, -5).translate((0, -1))
    mallet_head = Markup.draw_circle(1, 0.25)
    round_mallet = Markup.combine(mallet_stick, mallet_head)
    print(format(round_mallet))
    show(round_mallet)

..  abjad::

    boxed_mallet = round_mallet.pad_around(1).box()
    print(format(boxed_mallet))
    show(boxed_mallet)

..  abjad::

    boxed_mallets = Markup.concat([round_mallet, square_mallet])
    boxed_mallets = boxed_mallets.pad_around(1).box()
    print(format(boxed_mallets))
    show(boxed_mallets)

..  abjad::

    spacing = Markup.hspace(1)
    boxed_mallets = Markup.concat([round_mallet, spacing, square_mallet])
    boxed_mallets = boxed_mallets.pad_around(1).box()
    print(format(boxed_mallets))
    show(boxed_mallets)

Fonts and alignment
-------------------

..  abjad::

    flat = Markup.flat()
    print(format(flat))
    show(flat)

..  abjad::

    flat = Markup.flat()
    a_flat = Markup.concat(['A', flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = Markup('A').fontsize(3)
    flat = Markup.flat()
    a_flat = Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = Markup('A').fontsize(3)
    flat = Markup.flat().vcenter()
    a_flat = Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = Markup('A').fontsize(3).vcenter()
    flat = Markup.flat().vcenter()
    a_flat = Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = Markup('A').fontsize(3).override(('font-name', 'Arial')).vcenter()
    flat = Markup.flat().vcenter()
    a_flat = Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

Working directly with Postscript
--------------------------------

..  abjad::

    postscript = markuptools.Postscript()
    postscript = postscript.newpath()
    postscript = postscript.moveto(0, 0)
    postscript = postscript.rlineto(0, 6)
    postscript = postscript.rlineto(10, -2)
    postscript = postscript.rlineto(0, -2)
    postscript = postscript.rlineto(-10, -2)
    postscript = postscript.closepath()
    postscript = postscript.stroke()
    outline = Markup.postscript(postscript)
    print(format(outline))
    show(outline)

..  abjad::

    show(outline.pad_around(1).box())

..  abjad::

    outline = outline.with_dimensions((0, 10), (0, 6))
    show(outline.pad_around(1).box())

..  abjad::

    text = Markup('Vib').italic().bold().fontsize(3)
    show(text)

..  abjad::

    diagram = Markup.combine(text, outline)
    show(diagram)

..  abjad::

    diagram = Markup.combine(text, outline.vcenter())
    show(diagram)

..  abjad::

    diagram = Markup.combine(text, outline.vcenter())
    show(diagram)

..  abjad::

    diagram = Markup.combine(text.vcenter(), outline.vcenter())
    show(diagram)

..  abjad::

    diagram = Markup.combine(text.vcenter().translate((1, 0)), outline.vcenter())
    show(diagram)
    print(format(diagram))

Aligning markup on score components
-----------------------------------

..  abjad::

    staff = Staff(r"\time 2/4 c'2 d'2 e'2")
    for leaf in staff:
        attach(diagram, leaf)

    show(staff)

..  abjad::

    diagram = Markup(diagram, Up)
    staff = Staff(r"\time 2/4 c'2 d'2 e'2")
    for leaf in staff:
        attach(diagram, leaf)

    show(staff)

..  abjad::

    override(staff[1]).text_script.self_alignment_X = Center
    override(staff[2]).text_script.self_alignment_X = Right
    show(staff)

..  abjad::

    for leaf in staff:
        override(leaf).text_script.parent_alignment_X = Center

    show(staff)
