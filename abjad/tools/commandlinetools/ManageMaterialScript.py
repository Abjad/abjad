# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import traceback
from abjad.tools import systemtools
from abjad.tools.commandlinetools.ScorePackageScript import ScorePackageScript


class ManageMaterialScript(ScorePackageScript):
    '''
    Manages score package materials.

    ..  shell::

        ajv material --help

    '''

    ### CLASS VARIABLES ###

    alias = 'material'
    short_description = 'Manage score package materials.'

    ### PRIVATE METHODS ###

    def _collect_matching_paths(self, names):
        matching_paths = []
        valid_paths = self._list_material_subpackages()
        for name in names:
            if name.startswith('+'):
                name = '*{}*'.format('*'.join(name[1:]))
            for path in sorted(self._materials_path.glob(name)):
                if path not in matching_paths and path in valid_paths:
                    matching_paths.append(path)
        return matching_paths

    def _handle_create(self, material_name, force):
        print('Creating material subpackage {!r} ...'.format(material_name))
        target_path = self._name_to_score_subdirectory_path(
            material_name, 'materials', self._score_package_path)
        if target_path.exists() and not force:
            print('    Path exists: {}'.format(
                target_path.relative_to(self._score_package_path.parent)))
            sys.exit(1)
        metadata = self._read_score_metadata_json(self._score_package_path)
        metadata['score_package_name'] = self._score_package_path.name
        metadata['material_name'] = target_path.name
        source_name = 'example_material'
        source_path = self._get_boilerplate_path().joinpath(source_name)
        suffixes = ('.py', '.tex', '.ly', '.ily')
        for path in self._copy_tree(source_path, target_path):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        print('    Created {!s}/'.format(
            target_path.relative_to(self._score_repository_path)))

    def _handle_edit(self, material_name):
        from abjad import abjad_configuration
        globbable_names = self._collect_globbable_names(material_name)
        print('Edit candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(globbable_names)
        if not matching_paths:
            print('    No matching materials.')
            self._handle_list()
        command = [abjad_configuration.get_text_editor()]
        for path in matching_paths:
            command.append(str(path.joinpath('definition.py')))
        command = ' '.join(command)
        exit_code = self._call_subprocess(command)
        if exit_code:
            sys.exit(exit_code)

    def _handle_illustrate(self, material_name):
        globbable_names = self._collect_globbable_names(material_name)
        print('Illustration candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(globbable_names)
        if not matching_paths:
            print('    No matching materials.')
            self._handle_list()
        for path in matching_paths:
            self._illustrate_one_material(
                material_directory_path=path
                )
            print('    Illustrated {!s}/'.format(
                path.relative_to(self._score_package_path.parent)))
        if not self._in_test:
            for path in matching_paths:
                pdf_path = path.joinpath('illustration.pdf')
                systemtools.IOManager.open_file(str(pdf_path))

    def _handle_list(self):
        print('Available materials:')
        valid_paths = self._list_material_subpackages(self._score_package_path)
        if valid_paths:
            for path in valid_paths:
                print('    {!s}'.format(path.name))
        else:
            print('    No materials available.')
        sys.exit(2)

    def _handle_re_render(self, material_name):
        globbable_names = self._collect_globbable_names(material_name)
        print('Re-rendering candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(globbable_names)
        if not matching_paths:
            print('    No matching materials.')
            self._handle_list()
        for path in matching_paths:
            self._re_render_one_material(
                material_directory_path=path
                )
            print('    Re-rendered {!s}/'.format(
                path.relative_to(self._score_package_path.parent)))
        if not self._in_test:
            for path in matching_paths:
                pdf_path = path.joinpath('illustration.pdf')
                systemtools.IOManager.open_file(str(pdf_path))

    def _illustrate_one_material(self, material_directory_path):
        print('Illustrating {!s}/'.format(
            material_directory_path.relative_to(self._score_package_path.parent)))
        material_import_path = self._path_to_packagesystem_path(
            material_directory_path)
        material_name = material_directory_path.name
        definition_import_path = material_import_path + '.definition'
        try:
            module = self._import_path(
                definition_import_path,
                self._score_repository_path,
                )
            material = getattr(module, material_name)
        except (ImportError, AttributeError):
            traceback.print_exc()
            sys.exit(1)
        if not hasattr(material, '__illustrate__'):
            template = '    Cannot illustrate material of type {}.'
            message = template.format(type(material).__name__)
            print(message)
            sys.exit(1)
        with systemtools.Timer() as timer:
            try:
                lilypond_file = material.__illustrate__()
            except:
                traceback.print_exc()
                sys.exit(1)
        self._report_time(timer, prefix='Abjad runtime')
        ly_path = self._write_lilypond_ly(
            lilypond_file=lilypond_file,
            output_directory_path=material_directory_path,
            )
        self._write_lilypond_pdf(
            ly_path=ly_path,
            output_directory_path=material_directory_path,
            )

    def _re_render_one_material(self, material_directory_path):
        print('Re-rendering {!s}/'.format(
            material_directory_path.relative_to(self._score_package_path.parent)))
        ly_path = material_directory_path.joinpath('illustration.ly')
        if not ly_path.is_file():
            print('    illustration.ly is missing or malformed.')
            sys.exit(1)
        self._write_lilypond_pdf(
            ly_path=ly_path,
            output_directory_path=material_directory_path,
            )

    def _process_args(self, args):
        self._setup_paths(args.score_path)
        if args.edit is not None:
            self._handle_edit(material_name=args.edit)
        if args.illustrate is not None:
            self._handle_illustrate(material_name=args.illustrate)
        if args.list_:
            self._handle_list()
        if args.new:
            self._handle_create(force=args.force, material_name=args.new)
        if args.re_render is not None:
            self._handle_re_render(material_name=args.re_render)

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new',
            help='create a new material',
            metavar='NAME',
            )
        action_group.add_argument(
            '--edit',
            help='edit materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--illustrate',
            help='illustrate materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--re-render',
            help='re-render material illustrations',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--list',
            dest='list_',
            help='list materials',
            action='store_true',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--score-path', '-s',
            metavar='SCORE',
            help='score path or package name',
            default=os.path.curdir,
            )
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
