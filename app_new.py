from flask import Flask, request, jsonify
from logging import FileHandler, WARNING
import json
import localization
import get_altered_AP
import get_altered_AP_list
import get_distinct_location
import os
import classify
app = Flask(__name__)

app.debug=True

@app.route("/", methods=['GET', 'POST'])
def index():
    #value = request.json['V'][1]
    data=request.get_json()
    if data !=None:
        user=classify.modify(data['wifiRssVector'])
        Build,floor=classify.classify(user)
       # floor=data['floor']
        data_string=json.dumps(data)
        location =localization.localization(data_string)
    

    else:
        floor="A"
        location=[123, 456]
    return jsonify({"x":location[0], "y": location[1], "Build":Build, "floor": floor})
    #return jsonify({"return":data})

@app.route("/altered_ap", methods=['GET', 'POST'])
def altered_ap():
    address = request.args.get('mac')
    if address != None:
        data=request.get_json()
        if address == "all_altered_AP":
            location=get_distinct_location.get_distinct_location('all_altered_AP')
        elif address == "all_new_AP":
            location=get_distinct_location.get_distinct_location('all_new_AP')
        else:
            location = get_altered_AP.get_altered_AP(address)

        if (location == None):
            location='Empty'

        return jsonify({"data": {"mac": address, "location": location}})

    else:
        data=request.get_json()
        altered_ap_list = get_altered_AP_list.get_altered_AP_mac()
        return jsonify(altered_ap_list)

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5020)
    #app.run(host=, port=5020)
    from gevent import pywsgi
    app.debug=True
    server = pywsgi.WSGIServer(('10.79.31.159',5020),app)
    server.serve_forever()
  