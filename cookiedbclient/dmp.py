# Copyright 2023 Jaedson Silva
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DMP - Database Manipulation Protocol
# 
# Protocol Request Structure:
# ACTION PATH:<DATABASE NAME> (required if requested "action" is GET, ADD, DEL, or UPD)
# <datatype> <data (required if requested "action" is GET, ADD, DEL, or UPD)>
# 
# Protocol Response Structure:
# STATUS MESSAGE
# <datatype> <data (required if requested "action" is GET, ADD, DEL, or UPD)>

import json
import struct


class DMP:
    @staticmethod
    def parse_response(response: bytes) -> dict:
        parsed_response = {}
        split_response = response.split(b'\n')

        header = split_response[0]
        status, = struct.unpack(f'4s', header[:4])
        message, = struct.unpack(f'{len(header[4:])}s', header[4:])

        parsed_response['status'] = status.decode()
        parsed_response['message'] = message.decode()

        if len(split_response) == 2:
            data = split_response[1]
            datatype, = struct.unpack('4s', data[:4])
            rdata = data[4:]

            if datatype == b'json':
                _data = json.loads(rdata)
            elif datatype == b'intg':
                _data = int.from_bytes(rdata, byteorder='big')
            elif datatype == b'flot':
                _data, = struct.unpack('f', rdata)
            elif datatype == b'stri':
                _data = rdata.decode()
            elif datatype == b'bool':
                _data, = struct.unpack('?', rdata)

            parsed_response['data'] = _data

        return parsed_response

    @staticmethod
    def make_request(request: dict) -> bytes:
        action = request['action']
        path = request['path']

        packed = struct.pack(f'3s {len(path)}s', action.encode(), path.encode())
        data = request.get('data')

        if data is not None:
            if isinstance(data, (list, dict, tuple)):
                json_data = json.dumps(data, separators=(',', ':'))
                datatype = struct.pack('4s', b'json')
                _encoded_data = json_data.encode()
            elif isinstance(data, str):
                datatype = struct.pack('4s', b'stri')
                _encoded_data = data.encode()
            elif isinstance(data, bool):
                datatype = struct.pack('4s', b'bool')
                _encoded_data = struct.pack('?', data)
            elif isinstance(data, int):
                datatype = struct.pack('4s', b'intg')
                _encoded_data = data.to_bytes(2, byteorder='big')
            elif isinstance(data, float):
                datatype = struct.pack('4s', b'flot')
                _encoded_data = struct.pack('f', data)

            packed += b'\n'
            packed += datatype + _encoded_data

        return packed
