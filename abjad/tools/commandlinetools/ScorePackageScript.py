# -*- coding: utf-8 -*-
from __future__ import print_function
import abc
import collections
import importlib
import json
import os
import re
import shutil
import sys
import subprocess
import traceback
from abjad.tools import systemtools
from abjad.tools import stringtools
from abjad.tools.commandlinetools.CommandlineScript import CommandlineScript
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


class ScorePackageScript(CommandlineScript):
    '''
    Abstract base class for score-package scripts.
    '''

    ### CLASS VARIABLES ###

    _name_re = re.compile('^[a-z][a-z0-9_]*$')

    ### INITIALIZER ###

    def __init__(self):
        CommandlineScript.__init__(self)
        self._cwd = self._get_current_working_directory()
        self._score_package_path = None
        self._score_repository_path = None
        self._root_parent_path = None
        self._build_path = None
        self._segments_path = None
        self._materials_path = None

    ### PRIVATE METHODS ###

    def _call_subprocess(self, command):
        '''Trivial wrapper for mocking purposes.'''
        return subprocess.call(command, shell=True)

    def _collect_globbable_names(self, input_names):
        validated_names = []
        for input_name in input_names:
            if not self._name_is_valid_globbable(input_name):
                print('Cannot glob {!r}'.format(input_name))
                sys.exit(1)
            validated_names.append(input_name)
        return validated_names

    @classmethod
    def _copy_tree(cls, source_directory, target_directory, recurse=True):
        copied_paths = []
        source_paths = [_ for _ in source_directory.glob('*')]
        if not target_directory.exists():
            target_directory.mkdir(parents=True)
        for source_path in source_paths:
            if source_path.name == '__pycache__':
                continue
            elif source_path.suffix == '.pyc':
                continue
            source_name = source_path.relative_to(source_directory)
            target_path = target_directory.joinpath(source_name)
            if source_path.is_dir() and recurse:
                copied_paths.extend(
                    cls._copy_tree(source_path, target_path, recurse=True)
                    )
            elif source_path.is_file():
                shutil.copyfile(str(source_path), str(target_path))
            copied_paths.append(target_path)
        return copied_paths

    def _create_build_target(
        self,
        name,
        score_path,
        paper_size,
        orientation,
        force=False,
        ):
        from abjad import abjad_configuration
        target_path = self._name_to_score_subdirectory_path(
            name, 'build', score_path)
        if target_path.exists() and not force:
            print('    Path exists: {!s}'.format(
                target_path.relative_to(self._score_package_path.parent)))
            sys.exit(1)
        metadata = self._read_score_metadata_json(score_path)
        metadata['score_package_name'] = score_path.name
        if orientation == 'portrait':
            rotation = 0
            width, height = self.paper_sizes[paper_size]
        else:
            rotation = -90
            height, width = self.paper_sizes[paper_size]
        metadata['rotation'] = rotation
        metadata['orientation'] = orientation
        metadata['paper_size'] = paper_size
        metadata['height'] = height[0]
        metadata['width'] = width[0]
        metadata['unit'] = height[1]
        metadata['global_staff_size'] = 12
        metadata['uppercase_composer_name'] = metadata['composer_name'].upper()
        metadata['uppercase_title'] = metadata['title'].upper()
        metadata['lilypond_version'] = \
            abjad_configuration.get_lilypond_version_string()
        source_name = 'example_build_target'
        source_path = self._get_boilerplate_path().joinpath(source_name)
        suffixes = ('.py', '.tex', '.ly', '.ily')
        for path in self._copy_tree(source_path, target_path):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        return target_path

    @classmethod
    def _get_boilerplate_path(cls):
        import abjad
        return pathlib.Path(abjad.__path__[0]).joinpath('boilerplate')

    @classmethod
    def _get_current_working_directory(self):
        return pathlib.Path('.').absolute()

    def _import_all_materials(self, verbose=True):
        materials = collections.OrderedDict()
        for path in self._list_material_subpackages():
            name = path.name
            material = self._import_material(path, verbose=verbose)
            materials[name] = material
        return materials

    def _import_material(self, material_directory_path, verbose=True):
        material_import_path = self._path_to_packagesystem_path(
            material_directory_path)
        material_name = material_directory_path.name
        definition_import_path = material_import_path + '.definition'
        try:
            module = self._import_path(
                definition_import_path,
                self._score_repository_path,
                verbose=verbose,
                )
            material = getattr(module, material_name)
        except (ImportError, AttributeError):
            traceback.print_exc()
            sys.exit(1)
        return material

    def _import_path(self, path, score_root_path, verbose=True):
        if verbose:
            print('    Importing {!s}'.format(path))
        with systemtools.TemporaryDirectoryChange(str(score_root_path)):
            try:
                importlib.invalidate_caches()
            except:
                pass
            try:
                return importlib.import_module(path)
            except ImportError:
                traceback.print_exc()
                raise SystemExit(1)
            except Exception:
                traceback.print_exc()
                raise SystemExit(1)

    def _list_material_subpackages(self, score_path=None):
        materials_path = self._materials_path
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
            materials_path = score_path.joinpath('materials')
        paths = [
            path for path in materials_path.glob('*')
            if path.is_dir() and path.joinpath('__init__.py').exists()
            ]
        return sorted(paths)

    def _list_segment_subpackages(self, score_path=None):
        segments_path = self._segments_path
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
            segments_path = score_path.joinpath('segments')
        paths = [
            path for path in segments_path.glob('*')
            if path.is_dir() and path.joinpath('__init__.py').exists()
            ]
        return sorted(paths)

    @classmethod
    def _name_is_valid_globbable(cls, name):
        if '..' in name:
            return False
        elif '**' in name:
            return False
        elif '/' in name:
            return False
        return True

    def _name_to_score_subdirectory_path(self, name, section, score_path):
        score_path = self._path_to_score_package_path(score_path)
        name = stringtools.to_accent_free_snake_case(name)
        path = score_path.joinpath(section, name)
        return path

    def _path_to_packagesystem_path(self, path):
        score_package_path = self._path_to_score_package_path(path)
        relative_path = path.relative_to(score_package_path)
        parts = [score_package_path.name]
        parts.extend(relative_path.parts)
        return '.'.join(parts)

    def _path_to_score_package_path(self, path):
        if isinstance(path, str):
            # Is `path` an importable name? Use its module path.
            if self._name_re.match(path):
                try:
                    importlib.invalidate_caches()
                    module = importlib.import_module(path)
                    path = getattr(module, '__file__',  # A module.
                        getattr(module, '__path__'))  # A package.
                    if hasattr(path, '_path'):  # A local import.
                        path = path._path
                    if not isinstance(path, str):  # If it's a package...
                        path = path[0]  # Get the first path in the list.
                except:
                    traceback.print_exc()
            # Make sure to expand any home variables.
            path = pathlib.Path(os.path.expanduser(path))
        path = path.absolute()
        if not path.exists():
            print("Couldn locate or import score matching {!r}.".format(path))
            sys.exit(1)
        # Convert to directory.
        if path.is_file():
            path = path.parent
        # Check for parent package if not actually inside a package.
        # E.g.:
        #   - score_root
        #   - score_root/score/build/build_target
        #   - score_root/score/etc
        if not path.joinpath('__init__.py').exists():
            if path.joinpath(path.name, '__init__.py').exists():
                pass
            elif path.parent.joinpath('__init__.py').exists():
                path = path.parent
            elif path.parent.parent.joinpath('__init__.py').exists():
                path = path.parent.parent
        # Drill down as long as we're inside a Python package.
        while path.joinpath('__init__.py').exists():
            path = path.parent
        path = path.joinpath(path.name)
        # Make sure the directory even exists.
        if not path.exists():
            print('No score matching {!r} exists.'.format(path))
            sys.exit(1)
        # Check for mandatory files and subdirectories.
        if (
            not path.joinpath('__init__.py').exists() or
            not path.joinpath('materials').exists() or
            not path.joinpath('segments').exists() or
            not path.joinpath('build').exists() or
            not path.joinpath('tools').exists()
            ):
            print('Score directory {!r} is malformed.'.format(path))
            sys.exit(1)
        return path

    def _read_json(self, path, strict=False, verbose=True):
        if verbose:
            message = '    Reading {!s} ... '
            path_to_print = path.relative_to(self._score_package_path.parent)
            print(message.format(path_to_print), end='')
        if not path.exists():
            if verbose:
                print('JSON does not exist.')
            if strict:
                sys.exit(1)
            return {}
        try:
            with open(str(path), 'r') as file_pointer:
                expr = json.loads(file_pointer.read())
        except:
            if verbose:
                print('JSON is corrupted.')
            if strict:
                sys.exit(1)
            return {}
        if verbose:
            print('OK!')
        return expr

    def _read_score_metadata_json(self, score_path=None, verbose=True):
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
        else:
            score_path = self._score_package_path
        metadata_path = score_path.joinpath('metadata.json')
        metadata = self._read_json(metadata_path, verbose=verbose)
        assert isinstance(metadata, dict)
        return metadata

    def _read_segments_list_json(self, score_path=None, verbose=True):
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
        else:
            score_path = self._score_package_path
        listing_path = score_path.joinpath('segments', 'metadata.json')
        segment_paths = self._list_segment_subpackages(score_path)
        valid_segment_names = [_.name for _ in segment_paths]
        expr = self._read_json(listing_path, verbose=verbose)
        segment_names = expr.get('segments', [])
        if not isinstance(segment_names, list):
            if verbose:
                print('    Segments listing is malformed.')
            return []
        segment_names = [_ for _ in segment_names if _ in valid_segment_names]
        return segment_names

    def _report_time(self, timer, prefix='Runtime'):
        message = '        {}: {} {}'
        total_time = int(timer.elapsed_time)
        identifier = stringtools.pluralize('second', total_time)
        message = message.format(prefix, total_time, identifier)
        print(message)

    @abc.abstractmethod
    def _setup_argument_parser(self, parser):
        parser.add_argument(
            '-s', '--score-path',
            metavar='SCORE_PATH',
            default=os.path.curdir,
            )

    def _setup_paths(self, score_path):
        score_package_path = self._path_to_score_package_path(score_path)
        self._score_package_path = score_package_path
        self._score_repository_path = score_package_path.parent
        self._root_parent_path = self._score_repository_path.parent
        self._build_path = self._score_package_path.joinpath('build')
        self._distribution_path = self._score_package_path.joinpath('distribution')
        self._segments_path = self._score_package_path.joinpath('segments')
        self._materials_path = self._score_package_path.joinpath('materials')

    @classmethod
    def _template_file(cls, file_path, **kwargs):
        file_path = str(file_path)
        with open(file_path, 'r') as file_pointer:
            template = file_pointer.read()
        try:
            completed_template = template.format(**kwargs)
        except (IndexError, KeyError):
            #traceback.print_exc()
            lines = template.splitlines()
            for i, line in enumerate(lines):
                try:
                    lines[i] = line.format(**kwargs)
                except (KeyError, IndexError, ValueError):
                    pass
            completed_template = '\n'.join(lines)
        with open(file_path, 'w') as file_pointer:
            file_pointer.write(completed_template)

    def _write_json(self, expr, path, verbose=True):
        if verbose:
            message = '    Writing {!s}'
            path_to_print = path.relative_to(self._score_repository_path)
            print(message.format(path_to_print))
        contents = json.dumps(
            expr,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            )
        should_write = True
        if path.exists():
            with open(str(path), 'r') as file_pointer:
                if file_pointer.read() == contents:
                    should_write = False
        if should_write:
            with open(str(path), 'w') as file_pointer:
                file_pointer.write(contents)

    def _write_lilypond_ly(
        self,
        lilypond_file,
        output_directory_path,
        ):
        ly_path = output_directory_path.joinpath('illustration.ly')
        message = '    Writing {!s} ... '
        message = message.format(ly_path.relative_to(self._score_repository_path))
        print(message, end='')
        try:
            lilypond_format = format(lilypond_file)
        except:
            print('Failed!')
            traceback.print_exc()
            sys.exit(1)
        with open(str(ly_path), 'w') as file_pointer:
            file_pointer.write(lilypond_format)
        print('OK!')
        return ly_path

    def _write_lilypond_pdf(
        self,
        ly_path,
        output_directory_path,
        ):
        from abjad import abjad_configuration
        pdf_path = output_directory_path.joinpath('illustration.pdf')
        message = '    Writing {!s} ... '
        message = message.format(pdf_path.relative_to(self._score_repository_path))
        print(message, end='')
        command = '{} -dno-point-and-click -o {} {}'.format(
            abjad_configuration.get('lilypond_path', 'lilypond'),
            str(ly_path).replace('.ly', ''),
            str(ly_path),
            )
        with systemtools.Timer() as timer:
            with systemtools.TemporaryDirectoryChange(str(ly_path.parent)):
                exit_code = subprocess.call(command, shell=True)
        if exit_code:
            print('Failed!')
            sys.exit(1)
        print('OK!')
        self._report_time(timer, prefix='LilyPond runtime')

    def _write_score_metadata_json(self, score_path=None, verbose=True, **kwargs):
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
        else:
            score_path = self._score_package_path
        metadata_path = score_path.joinpath('metadata.json')
        self._write_json(kwargs, metadata_path, verbose=verbose)

    def _write_segments_list_json(self, segment_names, score_path=None, verbose=True):
        if score_path:
            score_path = self._path_to_score_package_path(score_path)
        else:
            score_path = self._score_package_path
        listing_path = score_path.joinpath('segments', 'metadata.json')
        segment_paths = self._list_segment_subpackages(score_path)
        valid_segment_names = set(_.name for _ in segment_paths)
        segment_names = [_ for _ in segment_names if _ in valid_segment_names]
        expr = {'segments': segment_names}
        self._write_json(expr, listing_path, verbose=verbose)
