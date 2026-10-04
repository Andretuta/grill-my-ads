"""Tests for scripts/ (stdlib unittest).  Run: python -m unittest discover tests"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit_score  # noqa: E402
import budget  # noqa: E402
import policy_lint  # noqa: E402
import roi  # noqa: E402
import utm  # noqa: E402


class SelfTests(unittest.TestCase):
    def test_selftests(self):
        for mod in (audit_score, budget, policy_lint, roi, utm):
            with self.subTest(mod.__name__), redirect_stdout(io.StringIO()):
                mod.selftest()


class Budget(unittest.TestCase):
    def test_cents_rounds_half_up(self):
        self.assertEqual(budget.to_cents("0.005"), 1)
        self.assertEqual(budget.to_cents(19.99), 1999)

    def test_ladder_length_and_growth(self):
        steps = budget.ladder(50, 0.2, 6)
        self.assertEqual(len(steps), 6)
        self.assertEqual(steps[-1], (5, 124.42))


class AuditScore(unittest.TestCase):
    def test_all_na_scores_zero(self):
        total, grade, cats, quick = audit_score.score(
            [{"id": "x", "category": "pixel", "severity": "high", "result": "na"}])
        self.assertEqual((total, grade[0], cats, quick), (0.0, "F", {}, []))

    def test_slow_fix_is_not_quick_win(self):
        checks = [{"id": "a", "category": "pixel", "severity": "critical", "result": "fail", "fix_minutes": 60}]
        self.assertEqual(audit_score.score(checks)[3], [])


class Roi(unittest.TestCase):
    def test_breakeven_rejects_bad_margin(self):
        for m in (0, -0.1, 1.5):
            with self.assertRaises(ValueError):
                roi.breakeven(m)

    def test_num_formats(self):
        self.assertEqual(roi.num(""), 0.0)
        self.assertEqual(roi.num("12,5"), 12.5)

    def test_verdict_watch_band(self):
        self.assertEqual(roi.verdict(None, None, 25, 20), "WATCH")
        self.assertEqual(roi.verdict(None, None, 31, 20), "CUT/FIX")


class PolicyLint(unittest.TestCase):
    def test_platform_endorsement_flagged(self):
        rules = {f["rule"] for f in policy_lint.lint("Instagram approved method")}
        self.assertIn("platform-brand", rules)

    def test_clean_copy_has_no_findings(self):
        self.assertEqual(policy_lint.lint("Frete grátis para todo o Brasil."), [])


class Utm(unittest.TestCase):
    def test_custom_source_and_fragment_kept(self):
        u = utm.build("https://x.com/p#top", source="instagram")
        self.assertIn("utm_source=instagram", u)
        self.assertTrue(u.endswith("#top"))

    def test_bare_domain_gets_root_path(self):
        self.assertTrue(utm.build("x.com").startswith("https://x.com/?"))


if __name__ == "__main__":
    unittest.main()
