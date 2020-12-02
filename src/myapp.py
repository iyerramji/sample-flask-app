from flask import Flask, request, make_response, jsonify
import hashlib
import sys
import psutil
from healthcheck import EnvironmentDump

app = Flask(__name__)


envdump = EnvironmentDump(app, "/metrics", include_python=False, include_os=False,
                          include_process=False, include_config=False)

local_msg_to_sha_cache = {}
local_sha_to_msg_cache = {}


@app.route('/messages', methods=['POST'])
def get_sha_from_message():
    request_json = request.get_json()
    if request_json:
        input_message = request_json['message']
        if input_message in local_msg_to_sha_cache:
            return_sha = local_msg_to_sha_cache.get(input_message)
        else:
            h = hashlib.new('sha256')
            h.update(input_message)
            return_sha = h.hexdigest()
            local_msg_to_sha_cache[input_message] = return_sha
            local_sha_to_msg_cache[return_sha] = input_message
        data = {'digest': return_sha}
        return make_response(jsonify(data), 200)
    return make_response('BAD INPUT FORMAT DETECED', 400)

@app.route('/messages/<hash>', methods=['GET', 'DELETE'])
def get_message_from_sha(hash):
    if request.method == "GET":
        if hash in local_sha_to_msg_cache:
            return_message = local_sha_to_msg_cache[hash]
            data = {'message': return_message}
            return make_response(jsonify(data), 200)
        else:
            data = {'error' : 'unable to find message',
                    'message_sha256' : hash }
            return make_response(jsonify(data), 404)
    if request.method == "DELETE":
        try:
            if hash in local_sha_to_msg_cache:
                message = local_sha_to_msg_cache[hash]
                if message in local_msg_to_sha_cache:
                    del local_msg_to_sha_cache[message]
                del local_sha_to_msg_cache[hash]
            return make_response('OK', 200)
        except:
            return make_response('INTERNAL SERVER ERROR', 500)

def cpu_metric():
    return { "cpu_current_usage" : str(psutil.cpu_percent()) + '%',
             "cpu_load_average_percentage" : [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()] }

envdump.add_section("cpu_metric", cpu_metric)


def memory_metric():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)
    return { "memory_available" : str(available) + 'MB free' , "memory_total":  str(total) + 'MB total', "memory_percent" : str(memory.percent) + '%' }

envdump.add_section("memory_metric", memory_metric)


def disk_metric():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)
    return { "disk_free" : str(free) + 'GB free' , "disk_total" : str(total) + 'GB total', "disk_percent" : str(disk.percent) + '%' }

envdump.add_section("disk_metric", disk_metric)



if __name__ == "__main__":
   app.run(host='0.0.0.0')
