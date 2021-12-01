"""
Functionality to look through a folder, optionally recursively, to find
certain class-definitions in any Python module within the folder.
"""
import os
import sys
import inspect
import importlib.util
from types import ModuleType
from contextlib import contextmanager
from typing import Iterable, Type, Optional, Union, Iterator

from .files import FileMatcher


@contextmanager
def add_sys_path(path: Union[str, os.PathLike]) -> Iterator[None]:
    """
    Temporary add given path to `sys.path`
    """
    path = os.fspath(path)
    try:
        sys.path.insert(0, path)
        yield
    finally:
        sys.path.remove(path)


def find_modules(
        path: str,
        root: Optional[str] = None,
        recursive: bool = True,
) -> Iterable[ModuleType]:
    """
    Searches through a folder an its sub-folders recursively to find
    and import all Python modules (*.py files).

    :param path: The path to look in
    :param recursive: Whether or not to search folder recursively
    :returns: An iterable of unique modules found
    """

    if root is None:
        root = os.path.join(path, '..')

    with add_sys_path(root):
        matches = FileMatcher(
            root_path=path,
            include=['**/*.py'],
            exclude=['**/__init__.py'],
            recursive=recursive,
        )

        for relative_path in matches:
            absolute_path = os.path.join(path, relative_path)

            import_name = relative_path \
                .replace(os.sep, '.') \
                .replace('.py', '')

            spec = importlib.util.spec_from_file_location(
                name=import_name,
                location=absolute_path,
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            yield module


def find_classes(**kwargs) -> Iterable[Type]:
    """
    Searches through a folder an its sub-folders recursively to find
    all class definitions.

    :param kwargs: **kwargs for `find_modules()`
    :returns: An iterable of unique classes found
    """
    return (
        cls
        for module in find_modules(**kwargs)
        for name, cls in inspect.getmembers(module, inspect.isclass)
    )


def find_inherited_classes(base: Type, **kwargs) -> Iterable[Type]:
    """
    Searches through a folder an its sub-folders recursively to find
    all class definitions that inherits from a certain base-class.
    Does not include the base-class itself.

    :param base: The base class which classes much subclass
    :param kwargs: **kwargs for `find_classes()`
    :returns: An iterable of unique classes that inherits from base
    """
    return (
        cls for cls in find_classes(**kwargs)
        if issubclass(cls, base)
        and cls is not base
    )


if __name__ == '__main__':
    # path = '/home/jakob/projects/EnergyTrackTrace/ett-auth/src'
    path = '/home/jakob/projects/EnergyTrackTrace/ett-platform-utils/src'

    print('Modules:')

    # for module in find_modules(path):
    #     print(module)

    # list(find_classes(path=path))
    x = list(find_classes(path=path))
    y = set(x)

    print(f'x: {len(x)}')
    print(f'y: {len(y)}')

    # for cls in x:
    #     print(cls)

    # for module in find_inherited_classes(path=path, base=Endpoint):
    #     print(module)
