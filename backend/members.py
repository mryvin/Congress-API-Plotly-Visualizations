from flask import jsonify

# Return message indicating that the member info graph would be here.
def get_member_info_graph():
    return jsonify({"message": "Member Info Graph Here"})

# Return message indicating that the member name graph would be here.
def get_member_name_graph():
    return jsonify({"message": "Member Name Graph Here"})

# Return message indicating that the member party graph would be here.
def get_member_party_graph():
    return jsonify({"message": "Member Party Graph Here"})

# Return message indicating that the member state graph would be here.
def get_member_state_graph():
    return jsonify({"message": "Member State Graph Here"})

# Return message indicating that the member legislation count graph would be here.
def get_member_leg_count_graph():
    return jsonify({"message": "Member Legislation Count Graph Here"})
