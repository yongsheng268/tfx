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
r"""Tool to generate api_docs for tfx.

# How to run

```shell
python build_docs.py -- \
--out_dir=/tmp/tfx_api
```

Note:
  If duplicate or spurious docs are generated, consider
  blacklisting them via the `private_map` argument below. Or
  `api_generator.doc_controls`
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# Standard Imports
from absl import app
from absl import flags

from tensorflow_docs.api_generator import doc_controls
from tensorflow_docs.api_generator import generate_lib
from tensorflow_docs.api_generator import public_api

# Standard Imports.third_party.tfx as tfx
# pylint: disable=unused-import
from tfx import components
from tfx import orchestration
# pylint: enable=unused-import

flags.DEFINE_string("out_dir", "/tmp/tfx_api", "Where to output the docs")

CODE_URL_PREFIX = "https://github.com/tensorflow/tfx/tree/master/tfx"


def main(_):
  # These make up for the empty __init__.py files.
  public_api.recursive_import_submodules(tfx.orchestration)
  public_api.recursive_import_submodules(tfx.components)

  do_not_generate_docs_for = [
      tfx.utils,
      tfx.proto,
      tfx.dependencies,
      tfx.version]

  for obj in do_not_generate_docs_for:
    doc_controls.do_not_generate_docs(obj)

  doc_generator = generate_lib.DocGenerator(
      root_title="TFX",
      py_modules=[("tfx", tfx)],
      code_url_prefix=CODE_URL_PREFIX,
      search_hints=True,
      site_path="/tfx/",
      private_map={},
      # local_definitions_filter ensures that shared modules are only
      # documented in the location that defines them, instead of every location
      # that impors them.
      callbacks=[public_api.local_definitions_filter])
  doc_generator.build(output_dir=os.path.join(flags.FLAGS.out_dir))


if __name__ == "__main__":
  app.run(main)
