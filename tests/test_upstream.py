from pathlib import Path
import runpy
import unittest


upstream = runpy.run_path(str(Path(__file__).parents[1] / "upstream.py"))

CONFIG = {
    "user": "me",
    "landed": {"org/copybara#2": "merged via Copybara"},
    "coauthored": {"org/folded#3": "org/folded#9"},
    "organizations": [
        {"name": "Org", "repos": ["org/"], "logo": None},
        {"name": "Pending", "repos": ["pending/"], "logo": None},
        {"name": "Absent", "repos": ["absent/"], "logo": None},
    ],
    "highlights": [{"pr": "org/copybara#2", "says": "Fixed the copybara case."}],
}


def pr(repo, number, state="open", merged=False):
    return {"repo": repo, "number": number, "title": f"Title {number}", "url": f"https://github.com/{repo}/pull/{number}",
            "state": state, "merged": merged}


def classified(prs):
    for item in prs:
        item["status"] = upstream["status"](item, CONFIG)
    return prs


class StatusTests(unittest.TestCase):
    def test_merges_github_does_not_record_count_as_landed(self):
        statuses = [item["status"] for item in classified([
            pr("org/merged", 1, "closed", merged=True),
            pr("org/copybara", 2, "closed"),
            pr("org/folded", 3, "closed"),
            pr("org/open", 4),
            pr("org/closed", 5, "closed"),
        ])]
        self.assertEqual(statuses, ["merged", "landed", "co-authored", "open", "closed"])


class OrganizationRowsTests(unittest.TestCase):
    def test_merged_organizations_come_first_and_list_only_merged_work(self):
        rows = upstream["organization_rows"](classified([
            pr("pending/tool", 7),
            pr("org/copybara", 2, "closed"),
            pr("org/open", 4),
        ]), CONFIG)
        self.assertEqual([(row["name"], row["merged"]) for row in rows], [("Org", True), ("Pending", False)])
        self.assertEqual(rows[0]["refs"], ["copybara #2"])
        self.assertEqual(rows[0]["says"], "Fixed the copybara case.")
        self.assertEqual(rows[1]["says"], "Title 7")

    def test_closed_work_alone_does_not_add_a_row(self):
        rows = upstream["organization_rows"](classified([pr("absent/repo", 1, "closed")]), CONFIG)
        self.assertEqual(rows, [])


class LayoutTests(unittest.TestCase):
    def test_busy_repositories_are_counted_instead_of_listed(self):
        refs = upstream["repo_refs"]("Org", [pr("org/busy", n) for n in range(1, 5)] + [pr("org/quiet", 9)])
        self.assertEqual(refs, ["busy 4 pull requests", "quiet #9"])

    def test_wrapped_lines_fit_and_keep_every_word(self):
        text = "Stopped garak's AI safety judge from losing the question it was grading in long prompts."
        for width in (120, 240, 544):
            lines = upstream["wrap"](text, "body", 21, width)
            self.assertEqual(" ".join(lines), text)
            for line in lines:
                if " " in line:
                    self.assertLessEqual(upstream["text_width"](line, "body", 21), width)


class ReadmeTests(unittest.TestCase):
    def test_every_pull_request_is_linked_in_the_log(self):
        prs = classified([pr("org/copybara", 2, "closed"), pr("pending/tool", 7), pr("me/own", 1, "closed", True)])
        rows = upstream["organization_rows"](prs, CONFIG)
        section = upstream["readme_section"](prs, CONFIG, rows)
        for item in prs:
            self.assertIn(f"]({item['url']})", section)
        self.assertTrue(section.startswith(upstream["START"]) and section.endswith(upstream["END"]))


if __name__ == "__main__":
    unittest.main()
