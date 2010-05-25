from _create_subdirs_interactive import _create_subdirs_interactive
from _filter_directories import  _filter_directories
from _filter_files import _filter_files
from populate_sphinx_directory import populate_sphinx_directory
import os


def build_doc_tree(ABJADPATH, api_doc_path, interactive):
   '''Walk entire Abjad codebase and build corresponding Sphinx doc tree.'''

   for current_root, directories, files in os.walk(ABJADPATH):

      _filter_directories(directories)
      _filter_files(files)
      directories.sort( )
      files.sort( )

      ## make subdirectories in docs if needed
      abjad_subdir = current_root.split('abjad')[-1].strip(os.path.sep)
      root_dir = os.path.join(api_doc_path, abjad_subdir)
      _create_subdirs_interactive(root_dir, directories, interactive)

      ## populate sphinx directory with sphinx files
      populate_sphinx_directory(root_dir, abjad_subdir, files, interactive)
      #print ''
