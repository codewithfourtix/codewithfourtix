import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch


with patch.dict(os.environ, ACCESS_TOKEN="test-only", USER_NAME="example"):
    stars_counter = runpy.run_path(str(Path(__file__).parents[1] / "today.py"))["stars_counter"]


class StarsCounterTests(unittest.TestCase):
    def test_missing_repositories_do_not_discard_available_stars(self):
        edges = [
            {"node": {"stargazers": {"totalCount": 3}}},
            None,
            {"node": None},
            {"node": {"stargazers": {"totalCount": 0}}},
            {"node": {"stargazers": {"totalCount": 7}}},
        ]
        self.assertEqual(stars_counter(edges), 10)

    def test_empty_repository_list(self):
        self.assertEqual(stars_counter([]), 0)


if __name__ == "__main__":
    unittest.main()
