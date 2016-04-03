#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)

properties = [
    {   
        'type': u'App::PropertyFloat',
        'propertyname': u'BoxSize',
        'description': u'The Size of the box.',
    },
   
]


geometry = [

    {
        'type':'Edge',
        'mincount': 1
    },
    {
        'type':'Face',
        'count': 1
    },

]        

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/surface/api/v1.0/properties', methods=['GET'])
def get_properties():
    return jsonify({'properties': properties})


@app.route('/surface/api/v1.0/path', methods=['POST'])
def get_path():
    path = []
    if not request.json or not 'BoxSize' in request.json:
        abort(400)
    mysize = request.json.get('BoxSize', "")    
    command = {
            'command': 'G0 X0 Y0 F100'
    }
    path.append(command)
    command = {
            'command': 'G1 X' + str(mysize) + " Y0 F100"
    }
    path.append(command)
    command = {
            'command': 'G1 X' + str(mysize) +  " Y" + str(mysize) +  ' F100'
    }
    path.append(command)
    command = {
            'command': 'G1 X0 Y' + str(mysize) +  ' F100'
    }
    path.append(command)
    command = {
            'command': 'G1 X0 Y0 F100'
    }
    path.append(command)
    return jsonify({'path': path}), 201

@app.route('/surface/api/v1.0/acceptable_geometry', methods=['GET'])
def get_geometry():
    return jsonify({'geometry': geometry})

if __name__ == '__main__':
    app.run(debug=True)
