"""Route and matching tests for Campus Roomfit.

Run from the repository folder: python -m unittest -v test_main
Requires Drafter to be installed.
"""
import os
import unittest
from unittest.mock import patch

os.environ["DRAFTER_SKIP"] = "1"
import main


class CampusRoomfitTests(unittest.TestCase):
    """Test each route and core matching functionality."""

    def setUp(self):
        """Create two sample students without writing to local storage."""
        self.first = main.Profile(
            "Alex", "Roommate", "Early bird", "Very tidy", "Quiet",
            "Yes", "No", "Student", "id-a",
        )
        self.second = main.Profile(
            "Morgan", "Roommate", "Early bird", "Very tidy", "Quiet",
            "Yes", "No", "Student", "id-b",
        )
        self.state = main.State(self.first, [self.first, self.second])
        self.refresh_patch = patch.object(main, "refresh", lambda state: None)
        self.save_patch = patch.object(main, "save_profiles", lambda state: None)
        self.refresh_patch.start()
        self.save_patch.start()
        self.addCleanup(self.refresh_patch.stop)
        self.addCleanup(self.save_patch.stop)

    def test_index(self):
        self.assertIsInstance(main.index(self.state), main.Page)

    def test_create_profile(self):
        self.state.editing_id = "id-a"
        self.assertIsInstance(main.create_profile(self.state), main.Page)
        self.assertEqual(self.state.editing_id, "")

    def test_edit_profile(self):
        self.assertIsInstance(main.edit_profile(self.state), main.Page)
        self.assertEqual(self.state.editing_id, "id-a")

    def test_save_profile(self):
        page = main.save_profile(
            self.state, "New", "Night owl", "Relaxed", "Some noise",
            "Study partner", False, True, "Likes group studying",
        )
        self.assertIsInstance(page, main.Page)
        self.assertEqual(self.state.current_profile.name, "New")
        self.assertEqual(len(self.state.profiles), 3)

    def test_select_profile(self):
        self.assertIsInstance(main.select_profile(self.state, "id-b | Morgan"), main.Page)
        self.assertEqual(self.state.current_profile.profile_id, "id-b")

    def test_confirm_delete(self):
        self.assertIsInstance(main.confirm_delete(self.state), main.Page)

    def test_delete_profile(self):
        self.assertIsInstance(main.delete_profile(self.state), main.Page)
        self.assertEqual(len(self.state.profiles), 1)

    def test_results(self):
        self.assertIsInstance(main.results(self.state), main.Page)

    def test_show_same_goal(self):
        self.state.match_filter = "All profiles"
        self.assertIsInstance(main.show_same_goal(self.state), main.Page)
        self.assertEqual(self.state.match_filter, "Same goal")

    def test_show_all_matches(self):
        self.assertIsInstance(main.show_all_matches(self.state), main.Page)
        self.assertEqual(self.state.match_filter, "All profiles")

    def test_all_profiles(self):
        self.assertIsInstance(main.all_profiles(self.state), main.Page)

    def test_about(self):
        self.assertIsInstance(main.about(self.state), main.Page)

    def test_compatibility(self):
        self.assertEqual(main.compatibility(self.first, self.second), 100)

    def test_find_matches(self):
        self.assertEqual(main.find_matches(self.first, self.state.profiles), [self.second])

    def test_missing_name_is_rejected(self):
        main.save_profile(
            self.state, " ", "Night owl", "Relaxed", "Some noise",
            "Roommate", False, False, "",
        )
        self.assertEqual(len(self.state.profiles), 2)


if __name__ == "__main__":
    unittest.main()
