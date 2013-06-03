from abjad.tools import markuptools
from experimental.tools.scoremanagertools.proxies.BasicModuleProxy import BasicModuleProxy


class IllustrationBuilderModuleProxy(BasicModuleProxy):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def illustration_ly_file_name(self):
        return self.file_path.replace('.py', '.ly')

    @property
    def illustration_pdf_file_name(self):
        return self.file_path.replace('.py', '.pdf')

    @property
    def is_user_finalized(self):
        return bool(self.import_illustration())

    ### PUBLIC METHODS ###

    # TODO: probably replace with in-place file execution
    def import_illustration(self):
        self.unimport()
        # TODO: port unimport
        #self.unimport_output_material_module()
        illustration = self._safe_import(locals(), self.packagesystem_basename, 'illustration',
            source_parent_package_path=self.parent_directory_packagesystem_path)
        illustration.header_block.title = markuptools.Markup(self.space_delimited_material_package_name)
        return illustration

    def write_stub_to_disk(self, prompt=True):
        self.clear()
        self.setup_statements.append('from abjad import *\n')
        line = 'from {}.output_material import {}\n'.format(
            self.material_package_path, self.material_package_name)
        self.setup_statements.append(line)
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})\n'
        line = line.format(self.material_package_name)
        self.body_lines.append(line)
        self.body_lines.append('illustration = lilypondfiletools.make_basic_lilypond_file(score)\n')
        self.write_to_disk()
        self._io.proceed('stub illustration builder written to disk.', is_interactive=prompt)
