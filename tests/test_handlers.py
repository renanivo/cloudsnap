# -*- coding: utf-8 -*-
import unittest

from mock import Mock, patch
import webapp2

import main


class BackupHandlerTest(unittest.TestCase):

    @patch('handlers.EC2Account')
    def test_should_create_AMI(self, account_mock):
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


if __name__ == '__main__':
    unittest.main()
