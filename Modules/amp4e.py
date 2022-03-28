from __main__ import app
import json
from pypsrp.client import Client
from flask import request, Response

@app.route('/api/powershell', methods=['GET', 'POST'])
def remotePowershell():
    data = json.loads(request.data)
    try:
        with Client(data["host"], ssl=False, username=data["username"], password=data["password"]) as client:
            stdout, stderr, rc = client.execute_cmd("powershell.exe gci $pwd")
            sanitised_stderr = client.sanitise_clixml(stderr)
            path = "c:\\temp"
            output, streams, had_errors = client.execute_ps('''$path = "%s"
                if (Test-Path -Path $path) {
                    Remove-Item -Path $path -Force -Recurse
                }
                New-Item -Path $path -ItemType Directory''' % path)
            output, streams, had_errors = client.execute_ps("New-Item -Path C:\\temp\\folder -ItemType Directory")
            output, streams, had_errors = client.execute_ps("Set-Content -Path C:\\temp\\folder\eicar.txt -Value 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'")
            client.close()
    except:
        return Response('{"PowerShell":"Failed to run on Host", "IP":"%s"}' % (data["host"]), status=404, mimetype='application/json')
    return Response('{"PowerShell":"Success to run on Host", "IP":"%s"}' % (data["host"]), status=200, mimetype='application/json')
