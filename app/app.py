#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)

properties = [
    {
        'type': u'App::PropertyFloat',
        'propertyname': u'SampleInterval',
        'description': u'The Sample Interval.  Small values can cause excessive wait.',
    },
    {
        'type': u'App::PropertyFloat',
        'propertyname': u'SampleInterval',
        'description': u'The Sample Interval.  Small values can cause excessive wait.',
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

def _waterline(self, obj, s, bb):
    import ocl
    from PathScripts.PathUtils import depth_params, fmt
    import time

    # def drawLoops(loops):
    #     nloop = 0
    #     waterlinestring = ""
    #     waterlinestring += "(waterline begin)"
    #     for loop in loops:
    #         p = loop[0]
    #         loopstring = "(loop begin)" + "\n"
    #         loopstring += "G0 Z" + str(obj.SafeHeight.Value) + "\n"
    #         loopstring += "G0 X" + \
    #             str(fmt(p.x)) + " Y" + str(fmt(p.y)) + "\n"
    #         loopstring += "G1 Z" + str(fmt(p.z)) + "\n"
    #         for p in loop[1:]:
    #             loopstring += "G1 X" + \
    #                 str(fmt(p.x)) + " Y" + str(fmt(p.y)) + \
    #                 " Z" + str(fmt(p.z)) + "\n"
    #             zheight = p.z
    #         p = loop[0]
    #         loopstring += "G1 X" + \
    #             str(fmt(p.x)) + " Y" + str(fmt(p.y)) + \
    #             " Z" + str(fmt(zheight)) + "\n"
    #         loopstring += "(loop end)" + "\n"
    #         print "    loop ", nloop, " with ", len(loop), " points"
    #         nloop = nloop + 1
    #         waterlinestring += loopstring
    #     waterlinestring += "(waterline end)" + "\n"
    #     return waterlinestring

    # depthparams = depth_params(obj.ClearanceHeight.Value, obj.SafeHeight.Value,
    #                             obj.StartDepth.Value, obj.StepDown, obj.FinishDepth.Value, obj.FinalDepth.Value)
    # # stlfile = "../../stl/gnu_tux_mod.stl"
    # # surface = STLSurfaceSource(stlfile)
    # surface = s

    # t_before = time.time()
    # zheights = depthparams.get_depths()
    # wl = ocl.Waterline()
    # # wl = ocl.AdaptiveWaterline() # this is slower, ca 60 seconds on i7
    # # CPU
    # wl.setSTL(surface)
    # diam = 0.5
    # length = 10.0
    # # any ocl MillingCutter class should work here
    # cutter = ocl.BallCutter(diam, length)
    # wl.setCutter(cutter)
    # # this should be smaller than the smallest details in the STL file
    # wl.setSampling(obj.SampleInterval)
    # # AdaptiveWaterline() also has settings for minimum sampling interval
    # # (see c++ code)
    # all_loops = []
    # for zh in zheights:
    #     print "calculating Waterline at z= ", zh
    #     wl.reset()
    #     wl.setZ(zh)  # height for this waterline
    #     wl.run()
    #     all_loops.append(wl.getLoops())
    # t_after = time.time()
    # calctime = t_after - t_before
    # n = 0
    # output = ""
    # for loops in all_loops:  # at each z-height, we may get many loops
    #     print "  %d/%d:" % (n, len(all_loops))
    #     output += drawLoops(loops)
    #     n = n + 1
    # print "(" + str(calctime) + ")"
    # return output



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/surface/api/v1.0/properties', methods=['GET'])
def get_properties():
    return jsonify({'properties': properties})

@app.route('/surface/api/v1.0/depths', methods=['POST'])
def echo_depths():
    d = request.json.get('Depths', "[10, 8, 5, 0,0]")
    return d, 201

@app.route('/surface/api/v1.0/path', methods=['POST'])
def get_path():
    path = []
    if not request.json or not 'SampleInterval' in request.json:
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
