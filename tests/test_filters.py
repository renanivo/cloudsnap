import unittest
from mock import patch

from filters import filter_backups_by_tags


class FiltersTest(unittest.TestCase):

    @patch("boto.ec2.image.Image")
    @patch("boto.ec2.image.Image")
    @patch("boto.ec2.image.Image")
    def test_should_filter_a_backup_list_by_the_tags_it_contains(self,
                                                                 backup_mock1,
                                                                 backup_mock2,
                                                                 backup_mock3):
        backup_mock1.tags = {"foo": "bar"}
        backup_mock2.tags = {"foo": "foo"}
        backup_mock3.tags = {"foo": "baz"}
        backup_list = [backup_mock1, backup_mock2, backup_mock3]

        filtered_list = filter_backups_by_tags(backup_list, {"foo": "bar"})

        self.assertEqual(1, len(filtered_list))
        self.assertIn(backup_mock1, filtered_list)
