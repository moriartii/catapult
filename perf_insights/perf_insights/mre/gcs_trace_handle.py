# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import os

from perf_insights import cloud_storage
from perf_insights.mre import trace_handle


class GCSTraceHandle(trace_handle.TraceHandle):
  def __init__(self, url, display_name, metadata, cache_directory):
    super(GCSTraceHandle, self).__init__(url, display_name, metadata)
    file_name = url.split('/')[-1]
    self.cache_file = os.path.join(
        cache_directory, file_name + '.gz')

  def Open(self):
    if not os.path.exists(self.cache_file):
      try:
        cloud_storage.Copy(self._url, self.cache_file)
      except cloud_storage.CloudStorageError:
        return None
    return open(self.cache_file, 'r')
