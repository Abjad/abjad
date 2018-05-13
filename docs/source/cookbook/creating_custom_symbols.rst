Creating custom musical symbols with markup
===========================================

..  abjad::

    import abjad

Building basic shapes with markup
---------------------------------

..  abjad::

    mallet_stick = abjad.Markup.draw_line(0, -6)
    mallet_head = abjad.Markup.filled_box((-1, 1), (-1, 1))
    square_mallet = abjad.Markup.combine([mallet_stick, mallet_head])
    print(format(square_mallet))
    show(square_mallet)

..  abjad::

    mallet_stick = abjad.Markup.draw_line(0, -6)
    mallet_head = abjad.Markup.filled_box((-1, 1), (-1, 1), blot=1)
    square_mallet = abjad.Markup.combine([mallet_stick, mallet_head])
    print(format(square_mallet))
    show(square_mallet)

..  abjad::

    mallet_stick = abjad.Markup.draw_line(0, -6)
    mallet_head = abjad.Markup.draw_circle(2, 0.5)
    round_mallet = abjad.Markup.combine([mallet_stick, mallet_head])
    print(format(round_mallet))
    show(round_mallet)

..  abjad::

    mallet_stick = abjad.Markup.draw_line(0, -5).translate((0, -1))
    mallet_head = abjad.Markup.draw_circle(1, 0.25)
    round_mallet = abjad.Markup.combine([mallet_stick, mallet_head])
    print(format(round_mallet))
    show(round_mallet)

..  abjad::

    boxed_mallet = round_mallet.pad_around(1).box()
    print(format(boxed_mallet))
    show(boxed_mallet)

..  abjad::

    boxed_mallets = abjad.Markup.concat([round_mallet, square_mallet])
    boxed_mallets = boxed_mallets.pad_around(1).box()
    print(format(boxed_mallets))
    show(boxed_mallets)

..  abjad::

    spacing = abjad.Markup.hspace(1)
    boxed_mallets = abjad.Markup.concat([round_mallet, spacing, square_mallet])
    boxed_mallets = boxed_mallets.pad_around(1).box()
    print(format(boxed_mallets))
    show(boxed_mallets)

Fonts and alignment
-------------------

..  abjad::

    flat = abjad.Markup.flat()
    print(format(flat))
    show(flat)

..  abjad::

    flat = abjad.Markup.flat()
    a_flat = abjad.Markup.concat(['A', flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = abjad.Markup('A').fontsize(3)
    flat = abjad.Markup.flat()
    a_flat = abjad.Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = abjad.Markup('A').fontsize(3)
    flat = abjad.Markup.flat().vcenter()
    a_flat = abjad.Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = abjad.Markup('A').fontsize(3).vcenter()
    flat = abjad.Markup.flat().vcenter()
    a_flat = abjad.Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

..  abjad::

    a = abjad.Markup('A').fontsize(3).override(('font-name', 'Arial')).vcenter()
    flat = abjad.Markup.flat().vcenter()
    a_flat = abjad.Markup.concat([a, flat])
    print(format(a_flat))
    show(a_flat)

Working directly with Postscript
--------------------------------

..  abjad::

    postscript = abjad.Postscript()
    postscript = postscript.newpath()
    postscript = postscript.moveto(0, 0)
    postscript = postscript.rlineto(0, 6)
    postscript = postscript.rlineto(10, -2)
    postscript = postscript.rlineto(0, -2)
    postscript = postscript.rlineto(-10, -2)
    postscript = postscript.closepath()
    postscript = postscript.stroke()
    outline = abjad.Markup.postscript(postscript)
    print(format(outline))
    show(outline)

..  abjad::

    show(outline.pad_around(1).box())

..  abjad::

    outline = outline.with_dimensions((0, 10), (0, 6))
    show(outline.pad_around(1).box())

..  abjad::

    text = abjad.Markup('Vib').italic().bold().fontsize(3)
    show(text)

..  abjad::

    diagram = abjad.Markup.combine([text, outline])
    show(diagram)

..  abjad::

    diagram = abjad.Markup.combine([text, outline.vcenter()])
    show(diagram)

..  abjad::

    diagram = abjad.Markup.combine([text.vcenter(), outline])
    show(diagram)

..  abjad::

    diagram = abjad.Markup.combine([text.vcenter(), outline.vcenter()])
    show(diagram)

..  abjad::

    diagram = abjad.Markup.combine([text.vcenter().translate((1, 0)), outline.vcenter()])
    show(diagram)
    print(format(diagram))

Aligning markup on score components
-----------------------------------

..  abjad::

    staff = abjad.Staff(r"\time 2/4 c'2 d'2 e'2")
    for leaf in staff:
        abjad.attach(diagram, leaf)

    show(staff)

..  abjad::

    diagram = abjad.Markup(diagram, Up)
    staff = abjad.Staff(r"\time 2/4 c'2 d'2 e'2")
    for leaf in staff:
        abjad.attach(diagram, leaf)

    show(staff)

..  abjad::

    abjad.override(staff[1]).text_script.self_alignment_X = Center
    abjad.override(staff[2]).text_script.self_alignment_X = Right
    show(staff)

..  abjad::

    for leaf in staff:
        abjad.override(leaf).text_script.parent_alignment_X = Center

    show(staff)
