from flask import Blueprint

from api.schemas import DashboardTileSchema, DashboardTileDataSchema
from api.utils import jsonify_data, get_jwt, get_json, set_tile, get_tile_model
import api.utils
dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
#    return jsonify_data([])

    tile_modules = [
        ['Security Check Status',  # title
         'markdown',  # tile_type
         ['SecValidation'],  # tags
         'Security Check Status',  # short_description
         'Security Check Status',  # description
         'security_validation',  # id
         ['last_hour'],  # periods
         'last_hour'],  # default_period
    ]
    tiles = []
    for t in tile_modules:
        tiles.append(set_tile(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]))

    return jsonify_data(tiles)


@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    _ = get_json(DashboardTileSchema())
    return jsonify_data({})


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    auth = get_jwt()
    req = get_json(DashboardTileDataSchema())
    req_id = req['tile_id']
    period = req['period']
    if req_id == 'security_validation':
        return jsonify_data(get_sec_validation(period))

    else:
        return jsonify_data({})


def get_sec_validation(period):
#    period = 'last_24_hours'
    response = api.utils.get_tile_model()

    import subprocess, json, datetime

    rr = subprocess.check_output('nslookup -type=txt securex_validation.anyconnect.me'.split()).decode("utf-8")
    rr = rr[rr.find('text = "') + 8:]
    rr = rr[:rr.find(']') + 1]
    rr = rr.replace('\\', "")
    rr = json.loads(rr)
    umb_result = [0, 0]
    amp_result = [0, 0]
    if 'umb' in rr:
        umb_result = rr[rr.index('umb') + 1: rr.index('umb') + 3]
        umb_result[1] = datetime.datetime.fromtimestamp(umb_result[1]).strftime("%d-%m-%Y %H:%M:%S ") + str(
            datetime.datetime.now().astimezone().tzinfo)
    if 'amp' in rr:
        amp_result = rr[rr.index('amp') + 1: rr.index('amp') + 3]
        amp_result[1] = datetime.datetime.fromtimestamp(amp_result[1]).strftime("%d-%m-%Y %H:%M:%S ") + str(
            datetime.datetime.now().astimezone().tzinfo)
    result_status = [('❌', 'Failed'),
                     ('✅', 'Successful')]

    response['data'].append("|   |   |   |   |")
    response['data'].append("| - | - | - | - |")
#    response['data'].append("| [Umbrella DNS Checks](https://umbrella.cisco.com/) | ✅ | Successful |")
#    response['data'].append("| [AMP Malware Checks](https://console.apjc.amp.cisco.com/) | ❌ | Failed |")

    response['data'].append("| [Umbrella DNS Checks](https://umbrella.cisco.com/) | %s | %s | %s |"
                            % (result_status[umb_result[0]][0], result_status[umb_result[0]][1], umb_result[1]))
    response['data'].append("| [AMP Malware Checks](https://console.apjc.amp.cisco.com/) | %s | %s | %s |"
                            % (result_status[amp_result[0]][0], result_status[amp_result[0]][1], amp_result[1]))

    return response



