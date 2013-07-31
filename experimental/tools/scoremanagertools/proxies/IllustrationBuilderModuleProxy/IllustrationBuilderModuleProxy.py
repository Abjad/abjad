# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from experimental.tools.scoremanagertools.proxies.ModuleProxy \
    import ModuleProxy


class IllustrationBuilderModuleProxy(ModuleProxy):

    ### PUBLIC PROPERTIES ###

    @property
    def illustration_ly_file_name(self):
        return self.filesystem_path.replace('.py', '.ly')

    @property
    def illustration_pdf_file_name(self):
        return self.filesystem_path.replace('.py', '.pdf')

    @property
    def is_user_finalized(self):
        return bool(self.import_illustration())

    ### PUBLIC METHODS ###

    # TODO: probably replace with in-place file execution
    def import_illustration(self):
        self.unimport()
        # TODO: port unimport
        #self.unimport_output_material_module()
        illustration = self._safe_import(
            locals(),
            self.packagesystem_basename,
            'illustration',
            source_parent_package_path=self.parent_directory_packagesystem_path,
            )
        material_package_name = self.packagesystem_path.split('.')[-2]
        material_package_name = material_package_name.replace('_', ' ')
        illustration.header_block.title = \
            markuptools.Markup(material_package_name)
        return illustration

    def write_stub_to_disk(
        self, material_package_path, material_package_name, prompt=True):
        lines = []
        lines.append('from abjad import *\n')
        line = 'from {}.output_material import {}\n'.format(
            material_package_path, material_package_name)
        lines.append(line)
        lines.append('\n')
        lines.append('\n')
        line = 'score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves({})\n'
        line = line.format(material_package_name)
        lines.append(
            'illustration = lilypondfiletools.make_basic_lilypond_file(score)\n')
        file_pointer = file(self.filesystem_path, 'w')
        file_pointer.write(''.join(lines))
        file_pointer.close()
        self.session.io_manager.proceed(
            'stub illustration builder written to disk.', 
            is_interactive=prompt)
