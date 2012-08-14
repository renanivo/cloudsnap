import unittest
from mock import patch

from filters import filter_backups_by_tags


class FiltersTest(unittest.TestCase):

    @patch("boto.ec2.image.Image")
    @patch("boto.ec2.image.Image")
    @patch("boto.ec2.image.Image")
    def setUp(self, backup_mock1, backup_mock2, backup_mock3):
        backup_mock1.tags = {"foo": "bar"}
        backup_mock2.tags = {"foo": "foo"}
        backup_mock3.tags = {"foo": "baz"}

        self.backup_list = [backup_mock1, backup_mock2, backup_mock3]

    def test_should_filter_a_backup_list_by_equal_values(self):
        filtered_list = filter_backups_by_tags(self.backup_list,
                                               {"foo": "bar"})

        self.assertEqual(1, len(filtered_list))
        self.assertIn(self.backup_list[0], filtered_list)

    def test_should_filter_a_backup_list_by_not_equal_values(self):
        filtered_list = filter_backups_by_tags(self.backup_list,
                                               tags_not_equal={"foo": "bar"})

        self.assertEqual(2, len(filtered_list))
        self.assertIn(self.backup_list[1], filtered_list)
        self.assertIn(self.backup_list[2], filtered_list)
