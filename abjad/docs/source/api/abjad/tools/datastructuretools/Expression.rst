.. _abjad--tools--datastructuretools--Expression:

Expression
==========

.. automodule:: abjad.tools.datastructuretools.Expression

.. currentmodule:: abjad.tools.datastructuretools.Expression

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.datastructuretools.Expression

.. autoclass:: Expression

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Expression.__add__

   .. automethod:: Expression.__call__

   .. automethod:: Expression.__copy__

   .. automethod:: Expression.__eq__

   .. automethod:: Expression.__format__

   .. automethod:: Expression.__getattr__

   .. automethod:: Expression.__getitem__

   .. automethod:: Expression.__hash__

   .. automethod:: Expression.__iadd__

   .. automethod:: Expression.__radd__

   .. automethod:: Expression.__repr__

   .. automethod:: Expression.__setitem__

   .. automethod:: Expression.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Expression.append_callback

   .. automethod:: Expression.color

   .. automethod:: Expression.establish_equivalence

   .. automethod:: Expression.get_markup

   .. automethod:: Expression.get_string

   .. automethod:: Expression.label

   .. automethod:: Expression.pitch_class_segment

   .. automethod:: Expression.pitch_set

   .. automethod:: Expression.print

   .. automethod:: Expression.select

   .. automethod:: Expression.sequence

   .. automethod:: Expression.wrap_in_list

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Expression.make_callback

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Expression.argument_count

   .. autoattribute:: Expression.argument_values

   .. autoattribute:: Expression.callbacks

   .. autoattribute:: Expression.evaluation_template

   .. autoattribute:: Expression.force_return

   .. autoattribute:: Expression.has_parentheses

   .. autoattribute:: Expression.is_composite

   .. autoattribute:: Expression.is_initializer

   .. autoattribute:: Expression.is_postfix

   .. autoattribute:: Expression.keywords

   .. autoattribute:: Expression.lone

   .. autoattribute:: Expression.map_operand

   .. autoattribute:: Expression.markup_maker_callback

   .. autoattribute:: Expression.module_names

   .. autoattribute:: Expression.name

   .. autoattribute:: Expression.next_name

   .. autoattribute:: Expression.precedence

   .. autoattribute:: Expression.proxy_class

   .. autoattribute:: Expression.qualified_method_name

   .. autoattribute:: Expression.string_template

   .. autoattribute:: Expression.subclass_hook

   .. autoattribute:: Expression.subexpressions

   .. autoattribute:: Expression.template