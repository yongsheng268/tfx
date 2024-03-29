# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tfx.utils.channel."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Standard Imports

import tensorflow as tf
from tfx.types import channel_utils
from tfx.types.artifact import Artifact
from tfx.types.channel import Channel


class ChannelUtilsTest(tf.test.TestCase):

  def test_artifact_collection_as_channel(self):
    instance_a = Artifact('MyTypeName')
    instance_b = Artifact('MyTypeName')
    chnl = channel_utils.as_channel([instance_a, instance_b])
    self.assertEqual(chnl.type_name, 'MyTypeName')
    self.assertItemsEqual(chnl.get(), [instance_a, instance_b])

  def test_channel_utils_as_channel_success(self):
    instance_a = Artifact('MyTypeName')
    instance_b = Artifact('MyTypeName')
    chnl_original = Channel('MyTypeName', artifacts=[instance_a, instance_b])
    chnl_result = channel_utils.as_channel(chnl_original)
    self.assertEqual(chnl_original, chnl_result)

  def test_empty_artifact_collection_as_channel_fail(self):
    with self.assertRaises(ValueError):
      channel_utils.as_channel([])

  def test_invalid_source_as_channel_fail(self):
    with self.assertRaises(ValueError):
      channel_utils.as_channel(source='invalid source')

  def test_type_check_success(self):
    chnl = Channel('MyTypeName')
    chnl.type_check('MyTypeName')

  def test_type_check_fail(self):
    chnl = Channel('MyTypeName')
    with self.assertRaises(TypeError):
      chnl.type_check('AnotherTypeName')

  def test_unwrap_channel_dict(self):
    instance_a = Artifact('MyTypeName')
    instance_b = Artifact('MyTypeName')
    channel_dict = {
        'id': Channel('MyTypeName', artifacts=[instance_a, instance_b])
    }
    result = channel_utils.unwrap_channel_dict(channel_dict)
    self.assertDictEqual(result, {'id': [instance_a, instance_b]})


if __name__ == '__main__':
  tf.test.main()
