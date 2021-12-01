import os
from glob import iglob
from typing import Iterable, List, Set


class FileMatcher(object):
    """[summary]"""

    def __init__(
        self,
        root_path: str,
        include: List[str],
        exclude: List[str] = None,
        recursive: bool = True,
    ):
        """[summary]

        Args:
            root_path (str): [description]
            include (List[str]): [description]
            exclude (List[str], optional): [description]. Defaults to None.
            recursive (bool, optional): [description]. Defaults to True.
        """
        self.root_path = root_path
        self.include = include
        self.exclude = exclude
        self.recursive = recursive

    def __iter__(self) -> Iterable[str]:
        """[summary]

        Returns:
            Iterable[str]: [description]
        """
        include_files = self.match_files(self.include)
        exclude_files = self.match_files(self.exclude) \
            if self.exclude is not None \
            else set()

        return iter(sorted(include_files - exclude_files))

    def match_files(self, patterns: List[str]) -> Set[str]:
        """[summary]

        Args:
            patterns (List[str]): [description]

        Returns:
            Set[str]: [description]
        """
        all_matches = set()

        for pattern in patterns:
            matches = iglob(
                pathname=f"{self.root_path}/{pattern}",
                recursive=self.recursive,
            )

            all_matches.update(
                os.path.relpath(path, self.root_path)
                for path in matches
                if os.path.isfile(path)
            )

        return all_matches


if __name__ == '__main__':
    matcher = FileMatcher(
        root_path='/home/jakob/projects/EnergyTrackTrace/ett-platform-utils/src',
        include=['**/*.py'],
        exclude=['**/__init__.py'],
        recursive=True,
    )

    for f in matcher:
        print(f)
