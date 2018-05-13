.. _abjadext--book--SphinxDocumentHandler:

SphinxDocumentHandler
=====================

.. automodule:: abjadext.book.SphinxDocumentHandler

.. currentmodule:: abjadext.book.SphinxDocumentHandler

.. container:: svg-container

   .. inheritance-diagram:: abjadext
      :lineage: abjadext.book.SphinxDocumentHandler

.. autoclass:: SphinxDocumentHandler

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SphinxDocumentHandler.__format__

   .. automethod:: SphinxDocumentHandler.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SphinxDocumentHandler.collect_abjad_input_blocks

   .. automethod:: SphinxDocumentHandler.collect_python_literal_blocks

   .. automethod:: SphinxDocumentHandler.get_default_stylesheet

   .. automethod:: SphinxDocumentHandler.interpret_input_blocks

   .. automethod:: SphinxDocumentHandler.rebuild_document

   .. automethod:: SphinxDocumentHandler.register_error

   .. automethod:: SphinxDocumentHandler.unregister_error

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: SphinxDocumentHandler.cleanup_graphviz_svg

   .. automethod:: SphinxDocumentHandler.find_target_file_paths

   .. automethod:: SphinxDocumentHandler.get_file_base_name

   .. automethod:: SphinxDocumentHandler.get_image_directories

   .. automethod:: SphinxDocumentHandler.get_source_extension

   .. automethod:: SphinxDocumentHandler.install_lightbox_static_files

   .. automethod:: SphinxDocumentHandler.interpret_code_blocks

   .. automethod:: SphinxDocumentHandler.interpret_image_source

   .. automethod:: SphinxDocumentHandler.on_autodoc_process_docstring

   .. automethod:: SphinxDocumentHandler.on_build_finished

   .. automethod:: SphinxDocumentHandler.on_builder_inited

   .. automethod:: SphinxDocumentHandler.on_doctree_read

   .. automethod:: SphinxDocumentHandler.on_env_updated

   .. automethod:: SphinxDocumentHandler.parse_rst

   .. automethod:: SphinxDocumentHandler.postprocess_image_target

   .. automethod:: SphinxDocumentHandler.render_png_image

   .. automethod:: SphinxDocumentHandler.render_svg_image

   .. automethod:: SphinxDocumentHandler.render_thumbnails

   .. automethod:: SphinxDocumentHandler.setup_sphinx_extension

   .. automethod:: SphinxDocumentHandler.should_ignore_document

   .. automethod:: SphinxDocumentHandler.visit_abjad_import_block

   .. automethod:: SphinxDocumentHandler.visit_abjad_input_block

   .. automethod:: SphinxDocumentHandler.visit_abjad_output_block_html

   .. automethod:: SphinxDocumentHandler.visit_abjad_output_block_latex

   .. automethod:: SphinxDocumentHandler.visit_abjad_reveal_block

   .. automethod:: SphinxDocumentHandler.visit_abjad_thumbnail_block_html

   .. automethod:: SphinxDocumentHandler.visit_abjad_thumbnail_block_latex

   .. automethod:: SphinxDocumentHandler.write_image_source

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: SphinxDocumentHandler.errored