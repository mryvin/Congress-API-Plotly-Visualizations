from flask import jsonify

def get_member_info_graph():
    return jsonify({"message": "Member Info Graph Here"})

def get_member_name_graph():
    return jsonify({"message": "Member Name Graph Here"})

def get_member_party_graph():
    return jsonify({"message": "Member Party Graph Here"})

def get_member_state_graph():
    return jsonify({"message": "Member State Graph Here"})

def get_member_leg_count_graph():
    return jsonify({"message": "Member Legislation Count Graph Here"})
