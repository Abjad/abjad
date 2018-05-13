.. _abjadext--book--CodeBlock:

CodeBlock
=========

.. automodule:: abjadext.book.CodeBlock

.. currentmodule:: abjadext.book.CodeBlock

.. container:: svg-container

   .. inheritance-diagram:: abjadext
      :lineage: abjadext.book.CodeBlock

.. autoclass:: CodeBlock

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: CodeBlock.__copy__

   .. automethod:: CodeBlock.__eq__

   .. automethod:: CodeBlock.__format__

   .. automethod:: CodeBlock.__hash__

   .. automethod:: CodeBlock.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: CodeBlock.as_docutils

   .. automethod:: CodeBlock.as_latex

   .. automethod:: CodeBlock.filter_output_proxies

   .. automethod:: CodeBlock.flush

   .. automethod:: CodeBlock.graph

   .. automethod:: CodeBlock.interpret

   .. automethod:: CodeBlock.play

   .. automethod:: CodeBlock.print

   .. automethod:: CodeBlock.push_asset_output_proxy

   .. automethod:: CodeBlock.push_code_output_proxy

   .. automethod:: CodeBlock.push_line_to_console

   .. automethod:: CodeBlock.quit

   .. automethod:: CodeBlock.setup_capture_hooks

   .. automethod:: CodeBlock.show

   .. automethod:: CodeBlock.write

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: CodeBlock.from_docutils_abjad_import_block

   .. automethod:: CodeBlock.from_docutils_abjad_input_block

   .. automethod:: CodeBlock.from_docutils_literal_block

   .. automethod:: CodeBlock.from_latex_abjad_block

   .. automethod:: CodeBlock.from_latex_abjadextract_block

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: CodeBlock.code_block_specifier

   .. autoattribute:: CodeBlock.current_lines

   .. autoattribute:: CodeBlock.document_source

   .. autoattribute:: CodeBlock.executed_lines

   .. autoattribute:: CodeBlock.image_layout_specifier

   .. autoattribute:: CodeBlock.image_render_specifier

   .. autoattribute:: CodeBlock.input_file_contents

   .. autoattribute:: CodeBlock.output_proxies

   .. autoattribute:: CodeBlock.starting_line_number