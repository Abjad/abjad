# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        Wrangler.__init__(self, session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        superclass = super(PackageWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'new': self.make_asset,
            'ren': self.rename,
            })
        return result

    ### PRIVATE METHODS ###

    def _find_git_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=True,
            repository='git',
            )
        return manager

    def _find_svn_manager(self, inside_score=True, must_have_file=False):
        manager = self._find_up_to_date_manager(
            inside_score=inside_score,
            must_have_file=must_have_file,
            system=False,
            repository='svn',
            )
        return manager

    def _find_up_to_date_manager(
        self, 
        inside_score=True,
        must_have_file=False,
        system=True,
        repository='git',
        ):
        import scoremanager
        abjad_library = False
        abjad_score_packages = False
        user_library = False
        user_score_packages = False
        if system and inside_score:
            abjad_score_packages = True
        elif system and not inside_score:
            abjad_library = True
        elif not system and inside_score:
            user_score_packages = True
        elif not system and not inside_score:
            user_library = True
        else:
            Exception
        asset_paths = self._list_asset_paths(
            abjad_library=abjad_library,
            abjad_score_packages=abjad_score_packages,
            user_library=user_library,
            user_score_packages=user_score_packages,
            )
        session = scoremanager.core.Session()
        for asset_path in asset_paths:
            manager = self._asset_manager_class(
                path=asset_path,
                session=session,
                )
            if (repository == 'git' and
                manager._is_git_versioned() and 
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager
            elif (repository == 'svn' and
                manager._is_svn_versioned() and
                manager._is_up_to_date() and
                (not must_have_file or manager._find_first_file_name())):
                return manager

    def _get_view_from_disk(self):
        package_manager = self._current_package_manager
        if not package_manager:
            return
        view_name = package_manager._get_metadatum('view_name')
        if not view_name:
            return
        view_inventory = self._read_view_inventory_from_disk()
        if not view_inventory:
            return
        view = view_inventory.get(view_name)
        return view

    def _initialize_asset_manager(self, path):
        assert os.path.sep in path, repr(path)
        manager = self._asset_manager_class(
            path=path, 
            session=self._session,
            )
        return manager

    def _is_valid_directory_entry(self, expr):
        superclass = super(PackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_asset(self, path):
        assert os.path.sep in path
        package_name = os.path.basename(path)
        assert stringtools.is_snake_case_package_name(package_name)
        os.mkdir(path)
        package_manager = self._initialize_asset_manager(path)
        package_manager.fix(prompt=False)

    ### PUBLIC METHODS ###

    def get_available_path(
        self, 
        storehouse_path=None,
        prompt_string=None,
        ):
        r'''Gets available path in `storehouse_path`.

        Sets `storehouse_path` equal to current storehouse path when
        `storehouse_path` is none.

        Returns string.
        '''
        storehouse_path = storehouse_path or self._current_storehouse_path
        while True:
            prompt_string = prompt_string or 'package name'
            getter = self._io_manager.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string(prompt_string)
            with self._backtrack:
                name = getter._run()
            if self._exit_io_method():
                return
            name = stringtools.string_to_accent_free_snake_case(name)
            path = os.path.join(storehouse_path, name)
            if os.path.exists(path):
                line = 'path already exists: {!r}.'
                line = line.format(path)
                self._io_manager.display([line, ''])
            else:
                return path

    def make_asset(self):
        r'''Makes asset.

        Returns none.
        '''
        with self._backtrack:
            path = self.get_available_path()
        if self._exit_io_method():
            return
        self._make_asset(path)

    def rename(self):
        r'''Renames asset.

        Returns none.
        '''
        with self._backtrack:
            asset_package_path = self.select_asset_package_path(
                infinitival_phrase='to rename',
                )
        if self._exit_io_method():
            return
        asset_manager = self._initialize_asset_manager(asset_package_path)
        asset_manager.rename()

    def select_asset_package_path(self, infinitival_phrase=None):
        '''Selects asset package path.

        Returns string.
        '''
        with self._controller_context:
            while True:
                name = '_human_readable_target_name'
                human_readable_target_name = getattr(self, name, None)
                breadcrumb = self._make_asset_selection_breadcrumb(
                    human_readable_target_name=human_readable_target_name,
                    infinitival_phrase=infinitival_phrase,
                    )
                menu = self._make_asset_selection_menu(
                    packages_instead_of_paths=True,
                    )
                result = menu._run()
                if self._exit_io_method():
                    break
                elif not result:
                    continue
                else:
                    break
            return result