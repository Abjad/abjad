# import order: tools, materials, segments.
# makes it possible for materials to import tools.
# makes it possible for segments to import both.
from {score_package_name}.tools import *
from {score_package_name}.materials import *
from {score_package_name} import segments
