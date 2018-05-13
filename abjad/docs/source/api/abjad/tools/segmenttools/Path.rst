.. _abjad--tools--segmenttools--Path:

Path
====

.. automodule:: abjad.tools.segmenttools.Path

.. currentmodule:: abjad.tools.segmenttools.Path

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.segmenttools.Path

.. autoclass:: Path

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Path.__bytes__

   .. automethod:: Path.__call__

   .. automethod:: Path.__enter__

   .. automethod:: Path.__eq__

   .. automethod:: Path.__exit__

   .. automethod:: Path.__fspath__

   .. automethod:: Path.__ge__

   .. automethod:: Path.__gt__

   .. automethod:: Path.__hash__

   .. automethod:: Path.__le__

   .. automethod:: Path.__lt__

   .. automethod:: Path.__new__

   .. automethod:: Path.__repr__

   .. automethod:: Path.__rtruediv__

   .. automethod:: Path.__str__

   .. automethod:: Path.__truediv__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Path.absolute

   .. automethod:: Path.activate

   .. automethod:: Path.add_buildspace_metadatum

   .. automethod:: Path.add_metadatum

   .. automethod:: Path.as_posix

   .. automethod:: Path.as_uri

   .. automethod:: Path.chmod

   .. automethod:: Path.coerce

   .. automethod:: Path.count

   .. automethod:: Path.deactivate

   .. automethod:: Path.exists

   .. automethod:: Path.expanduser

   .. automethod:: Path.extern

   .. automethod:: Path.get_asset_type

   .. automethod:: Path.get_files_ending_with

   .. automethod:: Path.get_identifier

   .. automethod:: Path.get_measure_profile_metadata

   .. automethod:: Path.get_metadata

   .. automethod:: Path.get_metadatum

   .. automethod:: Path.get_name_predicate

   .. automethod:: Path.get_next_package

   .. automethod:: Path.get_next_score

   .. automethod:: Path.get_part_identifier

   .. automethod:: Path.get_preamble_time_signatures

   .. automethod:: Path.get_previous_package

   .. automethod:: Path.get_previous_score

   .. automethod:: Path.get_time_signature_metadata

   .. automethod:: Path.get_title

   .. automethod:: Path.glob

   .. automethod:: Path.global_rest_identifiers

   .. automethod:: Path.global_skip_identifiers

   .. automethod:: Path.group

   .. automethod:: Path.instrument_to_staff_identifiers

   .. automethod:: Path.is__assets

   .. automethod:: Path.is__segments

   .. automethod:: Path.is_absolute

   .. automethod:: Path.is_block_device

   .. automethod:: Path.is_build

   .. automethod:: Path.is_builds

   .. automethod:: Path.is_buildspace

   .. automethod:: Path.is_char_device

   .. automethod:: Path.is_contents

   .. automethod:: Path.is_dir

   .. automethod:: Path.is_distribution

   .. automethod:: Path.is_etc

   .. automethod:: Path.is_external

   .. automethod:: Path.is_fifo

   .. automethod:: Path.is_file

   .. automethod:: Path.is_illustrationspace

   .. automethod:: Path.is_introduction_segment

   .. automethod:: Path.is_library

   .. automethod:: Path.is_material

   .. automethod:: Path.is_material_or_segment

   .. automethod:: Path.is_materials

   .. automethod:: Path.is_materials_or_segments

   .. automethod:: Path.is_part

   .. automethod:: Path.is_parts

   .. automethod:: Path.is_reserved

   .. automethod:: Path.is_score_build

   .. automethod:: Path.is_score_package_path

   .. automethod:: Path.is_scores

   .. automethod:: Path.is_segment

   .. automethod:: Path.is_segments

   .. automethod:: Path.is_socket

   .. automethod:: Path.is_stylesheets

   .. automethod:: Path.is_symlink

   .. automethod:: Path.is_test

   .. automethod:: Path.is_tools

   .. automethod:: Path.is_wrapper

   .. automethod:: Path.iterdir

   .. automethod:: Path.joinpath

   .. automethod:: Path.lchmod

   .. automethod:: Path.list_paths

   .. automethod:: Path.list_secondary_paths

   .. automethod:: Path.lstat

   .. automethod:: Path.match

   .. automethod:: Path.mkdir

   .. automethod:: Path.open

   .. automethod:: Path.owner

   .. automethod:: Path.part_to_identifiers

   .. automethod:: Path.read_bytes

   .. automethod:: Path.read_text

   .. automethod:: Path.relative_to

   .. automethod:: Path.remove

   .. automethod:: Path.remove_metadatum

   .. automethod:: Path.rename

   .. automethod:: Path.replace

   .. automethod:: Path.resolve

   .. automethod:: Path.rglob

   .. automethod:: Path.rmdir

   .. automethod:: Path.samefile

   .. automethod:: Path.score_skeleton

   .. automethod:: Path.segment_number_to_path

   .. automethod:: Path.stat

   .. automethod:: Path.symlink_to

   .. automethod:: Path.to_part

   .. automethod:: Path.touch

   .. automethod:: Path.trim

   .. automethod:: Path.unlink

   .. automethod:: Path.update_order_dependent_segment_metadata

   .. automethod:: Path.with_name

   .. automethod:: Path.with_parent

   .. automethod:: Path.with_score

   .. automethod:: Path.with_suffix

   .. automethod:: Path.write_bytes

   .. automethod:: Path.write_metadata_py

   .. automethod:: Path.write_text

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Path.cwd

   .. automethod:: Path.global_rest_identifier

   .. automethod:: Path.home

   .. automethod:: Path.is_segment_name

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Path.anchor

   .. autoattribute:: Path.build

   .. autoattribute:: Path.builds

   .. autoattribute:: Path.contents

   .. autoattribute:: Path.distribution

   .. autoattribute:: Path.drive

   .. autoattribute:: Path.etc

   .. autoattribute:: Path.materials

   .. autoattribute:: Path.name

   .. autoattribute:: Path.parent

   .. autoattribute:: Path.parents

   .. autoattribute:: Path.parts

   .. autoattribute:: Path.root

   .. autoattribute:: Path.scores

   .. autoattribute:: Path.segments

   .. autoattribute:: Path.stem

   .. autoattribute:: Path.stylesheets

   .. autoattribute:: Path.suffix

   .. autoattribute:: Path.suffixes

   .. autoattribute:: Path.test

   .. autoattribute:: Path.tools

   .. autoattribute:: Path.wrapper