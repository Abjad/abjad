from _write_file_interactive import _write_file_interactive
from make_sphinx_module_listing import make_sphinx_module_listing
import os


def populate_sphinx_directory(root_dir, abjad_subdir, files, interactive):

   # can probably remove modules_visited altogether
   #modules_visited = [ ]

   # make sphinx listing of modules
   for file in files:
      #print file

      #listing = make_sphinx_module_listing('abjad/' + abjad_subdir, file)
      components_path = os.path.join('abjad', abjad_subdir) 
      listing = make_sphinx_module_listing(components_path, file)
      #print listing

      # write no API entry when there is no listing
      if listing is None:
         continue
      
      # write listing to file
      rst_file = file.split('.')[0] + '.rst'
      index = os.path.join(root_dir, rst_file)
      _write_file_interactive(listing, index, interactive)

      # keep track of modules visited
      mod = os.path.join(abjad_subdir, file.split('.')[0])
      #modules_visited.append(mod)
