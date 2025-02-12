# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-725
import unittest

from ansiblelint.rules import RulesCollection
from ansiblelint.rules.MetaMainHasInfoRule import MetaMainHasInfoRule
from ansiblelint.testing import RunFromText

NO_GALAXY_INFO = """
author: the author
description: this meta/main.yml has no galaxy_info
"""

MISSING_INFO = """
galaxy_info:
  # author: the author
  description: Testing if meta contains values
  company: Not applicable

  license: MIT

  # min_ansible_version: 2.5

  platforms:
  - name: Fedora
    versions:
    - 25
  - missing_name: No name
    versions:
    - 25
"""

BAD_TYPES = """
galaxy_info:
  author: 007
  description: ['Testing meta']
  company: Not applicable

  license: MIT

  min_ansible_version: 2.5

  platforms: Fedora
"""

PLATFORMS_LIST_OF_STR = """
galaxy_info:
  author: '007'
  description: 'Testing meta'
  company: Not applicable

  license: MIT

  min_ansible_version: 2.5

  platforms: ['Fedora', 'EL']
"""


class TestMetaMainHasInfo(unittest.TestCase):
    collection = RulesCollection()
    collection.register(MetaMainHasInfoRule())

    def setUp(self) -> None:
        self.runner = RunFromText(self.collection)

    def test_no_galaxy_info(self) -> None:
        results = self.runner.run_role_meta_main(NO_GALAXY_INFO)
        assert len(results) == 1
        assert "No 'galaxy_info' found" in str(results)

    def test_missing_info(self) -> None:
        results = self.runner.run_role_meta_main(MISSING_INFO)
        assert len(results) == 3
        assert "Role info should contain author" in str(results)
        assert "Role info should contain min_ansible_version" in str(results)
        assert "Platform should contain name" in str(results)

    def test_bad_types(self) -> None:
        results = self.runner.run_role_meta_main(BAD_TYPES)
        assert len(results) == 3
        assert "author should be a string" in str(results)
        assert "description should be a string" in str(results)
        assert "Platforms should be a list of dictionaries" in str(results)

    def test_platform_list_of_str(self) -> None:
        results = self.runner.run_role_meta_main(PLATFORMS_LIST_OF_STR)
        assert len(results) == 1
        assert "Platforms should be a list of dictionaries" in str(results)
