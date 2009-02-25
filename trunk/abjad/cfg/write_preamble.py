from abjad.cfg.write_abjad_header import _write_abjad_header
from abjad.cfg.write_abjad_include import _write_abjad_include
from abjad.cfg.write_environment_includes import _write_environment_includes
from abjad.cfg.write_layout_template import _write_layout_template
from abjad.cfg.write_lilypond_language import _write_lilypond_language
from abjad.cfg.write_lilypond_version import _write_lilypond_version

def _write_preamble(outfile, template):
   _write_abjad_header(outfile)
   _write_lilypond_version(outfile)
   _write_lilypond_language(outfile)
   _write_abjad_include(outfile)
   _write_environment_includes(outfile)
   _write_layout_template(outfile, template)
   outfile.write('\n')
