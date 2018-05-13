.. _abjad--tools--lilypondparsertools--SchemeParser:

SchemeParser
============

.. automodule:: abjad.tools.lilypondparsertools.SchemeParser

.. currentmodule:: abjad.tools.lilypondparsertools.SchemeParser

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.lilypondparsertools.SchemeParser

.. autoclass:: SchemeParser

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SchemeParser.__call__

   .. automethod:: SchemeParser.__format__

   .. automethod:: SchemeParser.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SchemeParser.p_boolean__BOOLEAN

   .. automethod:: SchemeParser.p_constant__boolean

   .. automethod:: SchemeParser.p_constant__number

   .. automethod:: SchemeParser.p_constant__string

   .. automethod:: SchemeParser.p_data__EMPTY

   .. automethod:: SchemeParser.p_data__data__datum

   .. automethod:: SchemeParser.p_datum__constant

   .. automethod:: SchemeParser.p_datum__list

   .. automethod:: SchemeParser.p_datum__symbol

   .. automethod:: SchemeParser.p_datum__vector

   .. automethod:: SchemeParser.p_error

   .. automethod:: SchemeParser.p_expression__QUOTE__datum

   .. automethod:: SchemeParser.p_expression__constant

   .. automethod:: SchemeParser.p_expression__variable

   .. automethod:: SchemeParser.p_form__expression

   .. automethod:: SchemeParser.p_forms__EMPTY

   .. automethod:: SchemeParser.p_forms__forms__form

   .. automethod:: SchemeParser.p_list__L_PAREN__data__R_PAREN

   .. automethod:: SchemeParser.p_list__L_PAREN__data__datum__PERIOD__datum__R_PAREN

   .. automethod:: SchemeParser.p_number__DECIMAL

   .. automethod:: SchemeParser.p_number__HEXADECIMAL

   .. automethod:: SchemeParser.p_number__INTEGER

   .. automethod:: SchemeParser.p_program__forms

   .. automethod:: SchemeParser.p_string__STRING

   .. automethod:: SchemeParser.p_symbol__IDENTIFIER

   .. automethod:: SchemeParser.p_variable__IDENTIFIER

   .. automethod:: SchemeParser.p_vector__HASH__L_PAREN__data__R_PAREN

   .. automethod:: SchemeParser.t_BOOLEAN

   .. automethod:: SchemeParser.t_DECIMAL

   .. automethod:: SchemeParser.t_HASH

   .. automethod:: SchemeParser.t_HEXADECIMAL

   .. automethod:: SchemeParser.t_IDENTIFIER

   .. automethod:: SchemeParser.t_INTEGER

   .. automethod:: SchemeParser.t_L_PAREN

   .. automethod:: SchemeParser.t_R_PAREN

   .. automethod:: SchemeParser.t_anything

   .. automethod:: SchemeParser.t_error

   .. automethod:: SchemeParser.t_newline

   .. automethod:: SchemeParser.t_quote

   .. automethod:: SchemeParser.t_quote_440

   .. automethod:: SchemeParser.t_quote_443

   .. automethod:: SchemeParser.t_quote_446

   .. automethod:: SchemeParser.t_quote_456

   .. automethod:: SchemeParser.t_quote_error

   .. automethod:: SchemeParser.t_whitespace

   .. automethod:: SchemeParser.tokenize

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SchemeParser.debug

   .. autoattribute:: SchemeParser.lexer

   .. autoattribute:: SchemeParser.lexer_rules_object

   .. autoattribute:: SchemeParser.logger

   .. autoattribute:: SchemeParser.logger_path

   .. autoattribute:: SchemeParser.output_path

   .. autoattribute:: SchemeParser.parser

   .. autoattribute:: SchemeParser.parser_rules_object

   .. autoattribute:: SchemeParser.pickle_path