# Copyright 2015 gRPC authors.
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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
from argparse import ArgumentParser

import grpc
import kvs_pb2
import kvs_pb2_grpc


def run(key, value):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = kvs_pb2_grpc.KVSStub(channel)
        response = stub.Set(kvs_pb2.SetRequest(key=key, value=value))
    print(f"KVS client received: key={response.key}, value={response.value}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--key', required=True)
    parser.add_argument('--value', required=True)
    args = parser.parse_args()
    logging.basicConfig()
    run(key=args.key, value=args.value)
