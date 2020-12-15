Xenakis Example
---------------

Creation of Xenakisian pitch sieve in `Jonchaies`:

Initialize periodic patterns and create union:

::

    >>> import abjad
    >>> x17_0 = abjad.Pattern(indices=[0], period=17)
    >>> x17_1 = abjad.Pattern(indices=[1], period=17)
    >>> x17_4 = abjad.Pattern(indices=[4], period=17)
    >>> x17_5 = abjad.Pattern(indices=[5], period=17)
    >>> x17_7 = abjad.Pattern(indices=[7], period=17)
    >>> x17_11 = abjad.Pattern(indices=[11], period=17)
    >>> x17_12 = abjad.Pattern(indices=[12], period=17)
    >>> x17_16 = abjad.Pattern(indices=[16], period=17)
    >>> sieve = x17_0 | x17_1 | x17_4 | x17_5 | x17_7 | x17_11 | x17_12 | x17_16

Iterate through boolean vector to create pitch list:

::

    >>> pitches = []
    >>> length = 56
    >>> indices = [_ for _ in range(length)]
    >>> vector = sieve.get_boolean_vector(total_length=length)
    >>> for index, boolean_value in zip(indices, vector):
    ...     if boolean_value:
    ...         pitches.append(abjad.NumberedPitch(index))
    ...

Initialize note objects from pitch list:

::

    >>> staff = abjad.Staff([abjad.Note(_ - 15, (1, 16)) for _ in pitches])
    >>> abjad.attach(abjad.Clef("bass"), staff[0])
    >>> abjad.attach(abjad.Clef("treble"), staff[7])
    >>> abjad.ottava(staff[21:])
    >>> abjad.override(staff).BarLine.stencil = "##f"
    >>> abjad.override(staff).Beam.stencil = "##f"
    >>> abjad.override(staff).Flag.stencil = "##f"
    >>> abjad.override(staff).Stem.stencil = "##f"
    >>> abjad.override(staff).TimeSignature.stencil = "##f"
    >>> abjad.setting(staff).proportional_notation_duration = abjad.SchemeMoment((1, 25))

Show file of chart scores:

::

    >>> abjad.show(staff)
