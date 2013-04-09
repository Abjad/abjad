import os
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from abjad.tools import stringtools
from scftools.core.SCFObject import SCFObject
from scftools.proxies.PackageProxy import PackageProxy


class AssetWrangler(SCFObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    def __init__(self,
        score_external_asset_container_importable_names=None,
        score_internal_asset_container_importable_name_infix=None,
        session=None,
        user_asset_container_importable_names=None,
        user_asset_container_path_names=None):
        SCFObject.__init__(self, session=session)
        if score_external_asset_container_importable_names:
            assert all([stringtools.is_underscore_delimited_lowercase_package_name(x)
                for x in score_external_asset_container_importable_names])
        if score_internal_asset_container_importable_name_infix:
            assert stringtools.is_underscore_delimited_lowercase_package_name(
                score_internal_asset_container_importable_name_infix)
        self._score_external_asset_container_importable_names = \
            score_external_asset_container_importable_names or []
        self._score_internal_asset_container_importable_name_infix = \
            score_internal_asset_container_importable_name_infix
        self._user_asset_container_importable_names = \
            user_asset_container_importable_names or []
        self._user_asset_container_path_names = \
            user_asset_container_path_names or []

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.list_score_external_asset_container_importable_names() == \
                other.list_score_external_asset_container_importable_names():
                if self.score_internal_asset_container_importable_name_infix == \
                    other.score_internal_asset_container_importable_name_infix:
                    return True
        return False

    def __repr__(self):
        parts = []
        parts.extend(self.list_score_external_asset_container_importable_names())
        if self.score_internal_asset_container_importable_name_infix:
            parts.append(self.score_internal_asset_container_importable_name_infix)
        parts = ', '.join([repr(part) for part in parts])
        return '{}({})'.format(self.class_name, parts)

    ### READ-ONLY PUBLIC PROPERTIES ###

    # asset class #

    @abstractproperty
    def asset_class(self):
        pass

    @property
    def asset_class_human_readable_name(self):
        return self.change_string_to_human_readable_string(self.asset_class.__name__)

    @property
    def asset_class_plural_human_readable_name(self):
        return self.pluralize_string(self.asset_class_human_readable_name)

    @property
    def asset_container_class(self):
        return PackageProxy

    # current asset container #

    @property
    def current_asset_container_human_readable_name(self):
        return self.path_name_to_human_readable_base_name(self.current_asset_container_path_name)

    @property
    def current_asset_container_importable_name(self):
        if self.session.is_in_score:
            return self.dot_join([
                self.session.current_score_package_short_name,
                self.score_internal_asset_container_importable_name_infix])
        elif self.list_score_external_asset_container_importable_names():
            return self.list_score_external_asset_container_importable_names()[0]

    @property
    def current_asset_container_path_name(self):
        return self.package_importable_name_to_path_name(
            self.current_asset_container_importable_name)

    @property
    def current_asset_container_proxy(self):
        return self.asset_container_class(self.current_asset_container_importable_name)

    # infix #

    @property
    def score_internal_asset_container_importable_name_infix(self):
        return self._score_internal_asset_container_importable_name_infix

    # temporary asset #

    @property
    def temporary_asset_human_readable_name(self):
        return self.path_name_to_human_readable_base_name(self.temporary_asset_path_name)

    @property
    def temporary_asset_path_name(self):
        return os.path.join(self.current_asset_container_path_name, self.temporary_asset_short_name)

    @property
    def temporary_asset_proxy(self):
        return self.get_asset_proxy(self.temporary_asset_importable_name)

    @abstractproperty
    def temporary_asset_short_name(self):
        pass

    ### PUBLIC METHODS ###

    def conditionally_make_asset_container_packages(self, is_interactive=False):
        self.conditionally_make_score_external_asset_container_package()
        self.conditionally_make_score_internal_asset_container_packages()
        self.proceed('missing packages created.', is_interactive=is_interactive)

    def conditionally_make_score_external_asset_container_package(self):
        for importable_name in self.list_score_external_asset_container_importable_names():
            self.conditionally_make_empty_package(importable_name)

    def conditionally_make_score_internal_asset_container_packages(self, head=None):
        for score_internal_asset_container_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            self.conditionally_make_empty_package(score_internal_asset_container_importable_name)

    def fix_visible_assets(self, is_interactive=True):
        results = []
        for asset_proxy in self.list_visible_asset_proxies():
            results.append(asset_proxy.fix(is_interactive=is_interactive))
            if is_interactive:
                asset_proxy.profile()
        return results

    def get_asset_proxy(self, asset_full_name):
        return self.asset_class(asset_full_name, session=self.session)

    @abstractmethod
    def handle_main_menu_result(self, result):
        pass

    # asset containers (all) #

    def list_asset_container_human_readable_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_human_readable_names(head=head))
        result.extend(self.list_score_internal_asset_container_human_readable_names(head=head))
        return result

    def list_asset_container_importable_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_importable_names(head=head))
        result.extend(self.list_score_internal_asset_container_importable_names(head=head))
        return result

    def list_asset_container_path_names(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_path_names(head=head))
        result.extend(self.list_score_internal_asset_container_path_names(head=head))
        return result

    def list_asset_container_proxies(self, head=None):
        result = []
        result.extend(self.list_score_external_asset_container_proxies(head=head))
        result.extend(self.list_score_internal_asset_container_proxies(head=head))
        return result

    # assets (all) #

    def list_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_asset_path_names(self, head=None):
        result = []
        if head in (None,) + self.score_external_package_importable_names:
            result.extend(self.list_score_external_asset_path_names(head=head))
        result.extend(self.list_score_internal_asset_path_names(head=head))
        result.extend(self.list_user_asset_path_names(head=head))
        return result

    def list_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # score-external asset containers #

    def list_score_external_asset_container_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_container_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_external_asset_container_importable_names(self, head=None):
        result = []
        for importable_name in self._score_external_asset_container_importable_names:
            if head is None or importable_name.startswith(head):
                result.append(importable_name)
        return result

    def list_score_external_asset_container_path_names(self, head=None):
        result = []
        for importable_name in self.list_score_external_asset_container_importable_names(head=head):
            result.append(self.package_importable_name_to_path_name(importable_name))
        return result

    def list_score_external_asset_container_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_external_asset_container_importable_names(head=head):
            asset_container_proxy = self.asset_container_class(importable_name)
            result.append(asset_container_proxy)
        return result

    # score-external assets #

    def list_score_external_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_external_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_score_external_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    def list_score_external_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_score_external_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    # score-internal asset containers #

    def list_score_internal_asset_container_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_container_human_readable_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_internal_asset_container_importable_names(self, head=None):
        result = []
        for score_package_short_name in self.list_score_package_short_names(head=head):
            parts = [score_package_short_name]
            if self.score_internal_asset_container_importable_name_infix:
                parts.append(self.score_internal_asset_container_importable_name_infix)
            score_internal_score_package_importable_name = self.dot_join(parts)
            result.append(score_internal_score_package_importable_name)
        return result

    def list_score_internal_asset_container_path_names(self, head=None):
        result = []
        for package_importable_name in \
            self.list_score_internal_asset_container_importable_names(head=head):
            result.append(self.package_importable_name_to_path_name(package_importable_name))
        return result

    def list_score_internal_asset_container_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_internal_asset_container_importable_names(head=head):
            asset_container_proxy = self.asset_container_class(importable_name)
            result.append(asset_container_proxy)
        return result

    # score-internal assets #

    def list_score_internal_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_score_internal_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_score_internal_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    def list_score_internal_asset_proxies(self, head=None):
        result = []
        for importable_name in self.list_score_internal_asset_importable_names(head=head):
            asset_proxy = self.asset_class_name(importable_name)
            result.append(asset_proxy)
        return result

    ### BEGIN NEW ###

    # user asset containers #

    def list_user_asset_container_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_user_asset_container_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_user_asset_container_importable_names(self, head=None):
        result = []
        for importable_name in self._user_asset_container_importable_names:
            if head is None or importable_name.startswith(head):
                result.append(importable_name)
        return result

    def list_user_asset_container_path_names(self, head=None):
        #result = []
        #for importable_name in self.list_user_asset_container_importable_names(head=head):
        #    result.append(self.package_importable_name_to_path_name(importable_name))
        #return result
        return self._user_asset_container_path_names[:]

    def list_user_asset_container_proxies(self, head=None):
        result = []
        for importable_name in self.list_user_asset_container_importable_names(head=head):
            asset_container_proxy = self.asset_container_class(importable_name)
            result.append(asset_container_proxy)
        return result

    # user assets #

    def list_user_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_user_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_user_asset_path_names(self, head=None):
        result = []
        for path_name in self.list_user_asset_container_path_names(head=head):
            for name in os.listdir(path_name):
                if name[0].isalpha():
                    result.append(os.path.join(path_name, name))
        return result

    def list_user_asset_proxies(self, head=None):
        result = []
        for asset_path_name in self.list_user_asset_path_names(head=head):
            asset_proxy = self.get_asset_proxy(asset_path_name)
            result.append(asset_proxy)
        return result

    ### END NEW ###

    # visible assets #

    def list_visible_asset_human_readable_names(self, head=None):
        result = []
        for path_name in self.list_visible_asset_path_names(head=head):
            result.append(self.path_name_to_human_readable_base_name(path_name))
        return result

    def list_visible_asset_path_names(self, head=None):
        return self.list_asset_path_names(head=head)

    def list_visible_asset_proxies(self, head=None):
        return self.list_asset_proxies(head=head)

    # other #

    def make_asset(self, asset_short_name):
        assert stringtools.is_underscore_delimited_lowercase_string(asset_short_name)
        asset_path_name = os.path.join(self.current_asset_container_path_name, asset_short_name)
        asset_proxy = self.get_asset_proxy(asset_path_name)
        asset_proxy.write_stub_to_disk()

    @abstractmethod
    def make_asset_interactively(self):
        pass

    def make_asset_selection_breadcrumb(self, infinitival_phrase=None):
        if infinitival_phrase:
            return 'select {} {}:'.format(self.asset_class.generic_class_name, infinitival_phrase)
        else:
            return 'select {}:'.format(self.asset_class.generic_class_name)

    def make_asset_selection_menu(self, head=None):
        menu, section = self.make_menu(where=self.where(), is_keyed=False, is_parenthetically_numbered=True)
        section.tokens = self.make_visible_asset_menu_tokens(head=head)
        #self.debug(section.tokens, 'TOKENS')
        section.return_value_attribute = 'key'
        return menu

    @abstractmethod
    def make_main_menu(self):
        pass

    def make_visible_asset_menu_tokens(self, head=None):
        keys = self.list_visible_asset_path_names(head=head)
        bodies = self.list_visible_asset_human_readable_names(head=head)
        return zip(keys, bodies)

    def profile_visible_assets(self):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.profile()

    # TODO: write test
    def remove_assets_interactively(self, head=None):
        getter = self.make_getter(where=self.where())
        argument_list = self.list_visible_asset_path_names(head=head)
        getter.append_argument_range(self.asset_class_plural_human_readable_name, argument_list)
        result = getter.run()
        if self.backtrack():
            return
        asset_indices = [asset_number - 1 for asset_number in result]
        total_assets_removed = 0
        for asset_number in result:
            asset_index = asset_number - 1
            asset_path_name = argument_list[asset_index]
            asset_proxy = self.get_asset_proxy(asset_path_name)
            asset_proxy.remove()
            total_assets_removed += 1
        self.proceed('{} asset(s) removed.'.format(total_assets_removed))

    # TODO: write test
    def rename_asset_interactively(self, head=None):
        self.push_backtrack()
        asset_importable_name = self.select_asset_importable_name_interactively(
            head=head, infinitival_phrase='to rename')
        self.pop_backtrack()
        if self.backtrack():
            return
        asset_proxy = self.get_asset_proxy(asset_importable_name)
        asset_proxy.rename_interactively()

    def run(self, cache=False, clear=True, head=None, rollback=None, user_input=None):
        self.assign_user_input(user_input=user_input)
        breadcrumb = self.pop_breadcrumb(rollback=rollback)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu(head=head)
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack():
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.push_breadcrumb(breadcrumb=breadcrumb, rollback=rollback)
        self.restore_breadcrumbs(cache=cache)

    def select_asset_importable_name_interactively(
        self, clear=True, cache=False, head=None, infinitival_phrase=None, user_input=None):
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb(self.make_asset_selection_breadcrumb(infinitival_phrase=infinitival_phrase))
            menu = self.make_asset_selection_menu(head=head)
            result = menu.run(clear=clear)
            if self.backtrack():
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            else:
                break
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)
        return result

    def svn_add(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_add(is_interactive=False)
        self.proceed(is_interactive=is_interactive)

    def svn_ci(self, is_interactive=True):
        getter = self.make_getter(where=self.where())
        getter.append_string('commit message')
        commit_message = getter.run()
        if self.backtrack():
            return
        line = 'commit message will be: "{}"\n'.format(commit_message)
        self.display(line)
        if not self.confirm():
            return
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_ci(commit_message=commit_message, is_interactive=False)
        self.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_st(is_interactive=False)
        self.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        for asset_proxy in self.list_visible_asset_proxies():
            asset_proxy.svn_up(is_interactive=False)
        self.proceed(is_interactive=is_interactive)
