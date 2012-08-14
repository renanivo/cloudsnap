import unittest
import datetime
from mock import MagicMock, Mock, patch

from ec2adapters import EC2Account

from settings import AWS


class EC2AccountTest(unittest.TestCase):

    def _get_instance_mock(self, id, tags={}):
        instance_mock = MagicMock(spec='boto.ec2.instance.Instance')
        instance_mock.id = id
        instance_mock.tags = tags

        return instance_mock

    @patch('ec2adapters.EC2Connection')
    def test_should_create_a_connection_when_not_given(self, connection_mock):
        EC2Account()
        connection_mock.assert_called_once_with(AWS['key'],
                                                AWS['secret'],
                                                is_secure=AWS['use_safe_connection'])

    @patch('ec2adapters.EC2Connection')
    def test_should_get_an_instance_list(self, connection_mock):

        reservation_mock1 = Mock(spec='boto.ec2.instance.Reservation')
        reservation_mock2 = Mock(spec='boto.ec2.instance.Reservation')

        instance_mock1 = Mock(spec='boto.ec2.instance.Instance')
        instance_mock2 = Mock(spec='boto.ec2.instance.Instance')

        reservation_mock1.instances = [instance_mock1]
        reservation_mock2.instances = [instance_mock2]

        connection_mock.get_all_instances.return_value = [reservation_mock1,
                                                          reservation_mock2]

        a = EC2Account(connection_mock)
        instances = a.get_instances()

        self.assertEqual(1, connection_mock.get_all_instances.call_count)
        self.assertEqual(2, len(instances))
        self.assertIn(instance_mock1, instances)
        self.assertIn(instance_mock2, instances)

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_backup_an_instance_and_get_the_AMI_id(self, connection_mock):
        connection_mock.create_image.return_value = 99
        instance_mock = self._get_instance_mock(11, {"Name": "instance_name"})

        account = EC2Account(connection_mock)

        self.assertEqual(99, account.backup_instance(instance_mock))

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_use_boto_to_backup_an_instance(self, connection_mock):
        instance_mock = self._get_instance_mock(11, {"Name": "instance_name"})

        account = EC2Account(connection_mock)

        account.backup_instance(instance_mock)
        connection_mock.create_image.assert_called_once_with(11, "%s-%s" % (datetime.date.today(),
                                                                            "instance_name"))

    @patch('ec2adapters.AMI_NAME_TEMPLATE', '{{ today }}-{{ name }}')
    @patch('ec2adapters.EC2Connection')
    def test_should_backup_an_instance_with_time_and_instance_id_on_tags(self, connection_mock):
        connection_mock.create_image.return_value = 99
        instance_mock = self._get_instance_mock(11, {"Name": "instance_name"})

        account = EC2Account(connection_mock)

        account.backup_instance(instance_mock)
        connection_mock.create_tags.assert_called_once_with([99], {"instance": 11,
                                                                   "created_at": datetime.date.today(),
                                                                   "created_by": "cloudsnap"})

    @patch('boto.ec2.image.Image')
    @patch('boto.ec2.EC2Connection')
    def test_should_get_a_list_of_backups(self, connection_mock, image_mock):
        image_mock.tags = {"created_by": "cloudsnap"}
        connection_mock.get_all_images.return_value = [image_mock]

        account = EC2Account(connection_mock)
        backups = account.get_backups()

        self.assertEqual(1, len(backups))
        self.assertIn(image_mock, backups)
        connection_mock.get_all_images.assert_called_once()

    @patch('boto.ec2.EC2Connection')
    def test_should_not_get_AMIs_not_created_by_it(self, connection_mock):
        image_mock1 = MagicMock("boto.ec2.image.Image")
        image_mock2 = MagicMock("boto.ec2.image.Image")

        image_mock1.tags = {}
        image_mock2.tags = {"created_by": ""}

        connection_mock.get_all_images.return_value = [image_mock1,
                                                       image_mock2]

        account = EC2Account(connection_mock)
        backups = account.get_backups()

        connection_mock.assert_called_once()
        self.assertEqual(0, len(backups))

    @patch('boto.ec2.image.Image')
    @patch('boto.ec2.EC2Connection')
    def test_should_delete_a_backup(self, connection_mock, image_mock):
        account = EC2Account(connection_mock)
        image_mock.id = 10

        account.delete_backup(image_mock)

        connection_mock.deregister_image.assert_called_once_with(image_mock.id,
                                                                 True)


if __name__ == '__main__':
    unittest.main()
