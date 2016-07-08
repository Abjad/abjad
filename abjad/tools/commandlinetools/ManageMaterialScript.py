# -*- coding: utf-8 -*-
from __future__ import print_function
import inspect
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
        print('    Created {path!s}{sep}'.format(
            path=target_path.relative_to(self._score_repository_path),
            sep=os.path.sep))

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
            print('    Illustrated {path!s}{sep}'.format(
                path=path.relative_to(self._score_package_path.parent),
                sep=os.path.sep))
        for path in matching_paths:
            pdf_path = path.joinpath('illustration.pdf')
            systemtools.IOManager.open_file(str(pdf_path))

    def _handle_list(self):
        from abjad.tools import abctools
        basic_bases = (
            abctools.AbjadObject,
            abctools.AbjadValueObject,
            object,
            )
        print('Available materials:')
        all_materials = self._import_all_materials(verbose=False)
        if not all_materials:
            print('    No materials available.')
            sys.exit(2)
        materials = {}
        for material_name, material in all_materials.items():
            class_ = type(material)
            base = class_.__bases__[0]
            attrs = {attr.name: attr for attr in
                inspect.classify_class_attrs(class_)}
            if any(_ in class_.__bases__ for _ in basic_bases):
                base = class_
            elif getattr(class_, '__is_terminal_ajv_list_item__', False) and \
                attrs['__is_terminal_ajv_list_item__'].defining_class is class_:
                base = class_
            materials.setdefault(base, []).append((material_name, class_))
        #valid_paths = self._list_material_subpackages(self._score_package_path)
        materials = sorted(materials.items(), key=lambda pair: pair[0].__name__)
        for base, material_names in materials:
            print('    {}:'.format(base.__name__))
            for material_name, class_ in material_names:
                print('        {} [{}]'.format(material_name, class_.__name__))
        sys.exit(2)

    def _handle_render(self, material_name):
        globbable_names = self._collect_globbable_names(material_name)
        print('Rendering candidates: {!r} ...'.format(
            ' '.join(globbable_names)))
        matching_paths = self._collect_matching_paths(globbable_names)
        if not matching_paths:
            print('    No matching materials.')
            self._handle_list()
        for path in matching_paths:
            self._render_one_material(
                material_directory_path=path
                )
            print('    Rendered {path!s}{sep}'.format(
                path=path.relative_to(self._score_package_path.parent),
                sep=os.path.sep))
        for path in matching_paths:
            pdf_path = path.joinpath('illustration.pdf')
            systemtools.IOManager.open_file(str(pdf_path))

    def _illustrate_one_material(self, material_directory_path):
        print('Illustrating {path!s}{sep}'.format(
            path=material_directory_path.relative_to(self._score_package_path.parent),
            sep=os.path.sep))
        material = self._import_material(material_directory_path)
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
        if args.render is not None:
            self._handle_render(material_name=args.render)

    def _render_one_material(self, material_directory_path):
        print('Rendering {path!s}{sep}'.format(
            path=material_directory_path.relative_to(self._score_package_path.parent),
            sep=os.path.sep))
        ly_path = material_directory_path.joinpath('illustration.ly')
        if not ly_path.is_file():
            print('    illustration.ly is missing or malformed.')
            sys.exit(1)
        self._write_lilypond_pdf(
            ly_path=ly_path,
            output_directory_path=material_directory_path,
            )

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new material',
            metavar='NAME',
            )
        action_group.add_argument(
            '--edit', '-E',
            help='edit materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--illustrate', '-I',
            help='illustrate materials',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--render', '-R',
            help='render material illustrations',
            metavar='PATTERN',
            nargs='+',
            )
        action_group.add_argument(
            '--list', '-L',
            dest='list_',
            help='list materials',
            action='store_true',
            )
#        action_group.add_argument(
#            '--copy', '-Y',
#            help='copy material',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--rename', '-M',
#            help='rename material',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--delete', '-D',
#            help='delete material',
#            metavar='NAME',
#            )
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
