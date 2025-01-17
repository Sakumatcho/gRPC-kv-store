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

from cmd import Cmd
import logging

import grpc

import kvs_pb2
import kvs_pb2_grpc


class GetCmd(Cmd):
    prompt = "  key?) "
    def __init__(self):
        super(GetCmd, self).__init__()

    def default(self, key):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = kvs_pb2_grpc.KVSStub(channel)
            response = stub.Get(kvs_pb2.GetRequest(key=key))
        self.response = response
        return True


class SetKeyCmd(Cmd):
    prompt = "  key?) "
    def __init__(self):
        super(SetKeyCmd, self).__init__()

    def default(self, key):
        self.key = key
        return True


class SetValueCmd(Cmd):
    prompt = "  value?) "
    def __init__(self):
        super(SetValueCmd, self).__init__()

    def default(self, value):
        self.value = value
        return True


class KVSCmd(Cmd):
    prompt = "kvs: get or set?) "
    def __init__(self):
        super(KVSCmd, self).__init__()

    def do_get(self, _):
        get_command = GetCmd()
        get_command.cmdloop()
        response = get_command.response
        print(f"KVS client received: value={response.value}")

    def do_set(self, _):
        set_key_command = SetKeyCmd()
        set_key_command.cmdloop()
        set_value_command = SetValueCmd()
        set_value_command.cmdloop()

        with grpc.insecure_channel("localhost:50051") as channel:
            stub = kvs_pb2_grpc.KVSStub(channel)
            response = stub.Set(kvs_pb2.SetRequest(key=set_key_command.key, value=set_value_command.value))
        print(f"KVS client received: key={response.key}, value={response.value}")

    def do_bye(self, _):
        return True


if __name__ == "__main__":
    logging.basicConfig()
    KVSCmd().cmdloop()
