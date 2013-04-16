from abjad.tools import markuptools
from experimental.tools.scoremanagementtools.proxies.BasicModuleProxy import BasicModuleProxy
from experimental.tools.scoremanagementtools.helpers import safe_import


class IllustrationBuilderModuleProxy(BasicModuleProxy):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def illustration_ly_file_name(self):
        return self.path_name.replace('.py', '.ly')

    @property
    def illustration_pdf_file_name(self):
        return self.path_name.replace('.py', '.pdf')

    @property
    def is_user_finalized(self):
        return bool(self.import_illustration())

    ### PUBLIC METHODS ###

    # TODO: probably replace with in-place file execution
    def import_illustration(self):
        self.unimport()
        # TODO: port unimport
        #self.unimport_output_material_module()
        illustration = safe_import(locals(), self.module_short_name, 'illustration',
            source_parent_package_importable_name=self.parent_package_importable_name)
        illustration.header_block.title = markuptools.Markup(self.material_spaced_name)
        return illustration

    def write_stub_to_disk(self, prompt=True):
        self.clear()
        self.setup_statements.append('from abjad import *\n')
        line = 'from {}.output_material import {}\n'.format(
            self.material_package_importable_name, self.material_underscored_name)
        self.setup_statements.append(line)
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})\n'
        line = line.format(self.material_underscored_name)
        self.body_lines.append(line)
        self.body_lines.append('illustration = lilypondfiletools.make_basic_lilypond_file(score)\n')
        self.write_to_disk()
        self.proceed('stub illustration builder written to disk.', is_interactive=prompt)
