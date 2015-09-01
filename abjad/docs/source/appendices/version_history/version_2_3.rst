:orphan:

Abjad 2.3
---------

Released 2011-09-04. Built from r4747.

Filled out the API for working with marks::

    indicatortools.attach_articulations_to_components_in_expr()
    indicatortools.detach_articulations_attached_to_component()
    indicatortools.get_articulations_attached_to_component()
    indicatortools.get_articulation_attached_to_component()
    indicatortools.is_component_with_articulation_attached()

These five type of functions are now implemented for the following marks::

    indicatortools.Annotation
    indicatortools.Articulation
    indicatortools.LilyPondCommand
    indicatortools.LilyPondComment
    indicatortools.StemTremolo

The same type of functions are likewise implemented for the following context marks::

    indicatortools.Clef
    indicatortools.Dynamic
    indicatortools.InstrumentMark
    indicatortools.KeySignature
    indicatortools.StaffChange
    indicatortools.Tempo
    indicatortools.TimeSignature

* Extended ``Container.extend()`` to allow for LilyPond input strings. You can now say ``container.extend("c'4 d'4 e'4 f'4")``.

* Added public ``parent`` attribute to all components. You can now say ``note.parent``. The attribute is read-only.
* Added ``cfgtools.list_package_dependency_version()``.
* Added ``pytest`` and ``Sphinx`` dependencies to the Abjad package.
* Added LilyPond command mark chapter to reference manual

* Renamed ``cfgtools`` to ``configurationtools``.
* Renamed ``durtools`` to ``durationtools``.
* Renamed ``metertools`` to ``metertools``.
* Renamed ``seqtools`` to ``sequencetools``.
* Renamed ``Mark.attach_mark()`` to ``Mark.attach()``.
* Renamed ``Mark.detach_mark()`` to ``Mark.detach()``.
* Renamed ``indicatortools.Comment`` to ``indicatortools.LilyPondComment``. This matches ``indicatortools.LilyPondCommand``.
* Removed ``indicatortools.TimeSignature(3, 8)`` initialization. You must now say ``indicatortools.TimeSignature((3, 8))`` instead. This parallels the initialization syntax for rests, skips and measures.
