# -*- coding: utf-8 -*-
import unittest
import datetime

from mock import Mock, patch
import webapp2

import main


class BackupHandlerTest(unittest.TestCase):

    @patch('handlers.EC2Account')
    def test_should_create_a_backup(self, account_mock):
        instance_mock = Mock(spec='boto.ec2.instance.Instance')
        instance_mock.id = 0

        account_mock.get_instances.return_value = [instance_mock]
        account_mock.backup_instance.return_value = 99
        account_mock.return_value = account_mock

        request = webapp2.Request.blank('/backup')
        response = request.get_response(main.app)

        self.assertEqual('0 backed up on image 99', response.body)
        account_mock.get_instances.assert_called_once()
        account_mock.backup_instance.assert_called_once_with(instance_mock)

    @patch('boto.ec2.image.Image')
    @patch('boto.ec2.image.Image')
    @patch('handlers.EC2Account')
    def test_should_delete_backups_older_than_one_day(self,
                                                      account_mock,
                                                      current_backup,
                                                      old_backup):
        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        current_backup.id = 1
        current_backup.tags = {
            "created_by": "cloudsnap",
            "created_at": today,
            }
        current_backup.block_device_mapping.current_value.snapshot_id = 10
        old_backup.id = 2
        old_backup.tags = {
            "created_by": "cloudsnap",
            "created_at": yesterday
            }
        current_backup.block_device_mapping.current_value.snapshot_id = 20

        account_mock.get_backups.return_value = [current_backup, old_backup]

        request = webapp2.Request.blank('/cleanup')
        response = request.get_response(main.app)

        self.assertEqual("image 1 deregistered and snapshot 10 deleted",
                         response.body)
        account_mock.get_backups.assert_called_once()
        account_mock.delete_backup.assert_called_once_with(old_backup.id)


if __name__ == '__main__':
    unittest.main()
