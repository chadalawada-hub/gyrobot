import subprocess
import json

proc = subprocess.Popen(["python", "server.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def call(method: str, params: dict):
    request_data = json.dumps({"method": method, "params": params, "jsonrpc": "2.0", "id": 1})
    proc.stdin.write(request_data + "\n")
    proc.stdin.flush()
    response = proc.stdout.readline().strip()
    return json.loads(response)

print(call("convert_currency", {"currency_code": "EUR", "date_str": "2026-01-01"}))
print(call("prime_rates", {"date_str": "2026-01-01"}))  
