import unittest
import sys
import boto3
from moto import mock_s3

sys.path.insert(0, '/home/kiwichi/WEATHERAPI/packages/')
from packages import mod

class TestMod(unittest.TestCase):

    def test_intersection(self):

        self.assertEqual(mod.intersection([1,2,3], [2,3,4]), [2,3])
        self.assertEqual(mod.intersection([1,2,3], [1,2,3]), [1,2,3])
        self.assertEqual(mod.intersection([1,2,3], [5,6,7]), [])

    @mock_s3
    def test_upload_data(self):
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket='test_bucket',CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        mod.upload_data("testing","test_bucket","ES","aaaaaa")


if __name__ == '__main__':
    unittest.main()