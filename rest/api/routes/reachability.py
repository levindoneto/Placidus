from flask import Blueprint

reachability_route = Blueprint("reachability_route", __name__)

@reachability_route.route("/reachability", methods=["GET"])
def get_ips():
    ips = Mininet.getHosts()
    return jsonify({"ips": ips})