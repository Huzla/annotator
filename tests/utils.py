import json

def make_json_post(client, action, body):
    return client.post(action, data=json.dumps(body), headers={ "Content-Type": "application/json" })

def check_error(body_str, message):
    err = json.dumps(body_str)
    return isinstance(err, dict) and "msg" in err and err.msg == message

def array_check(arr, constraint):
    return next(( value for value in arr if constraint(value) ), None) != None

def check_dict_field(dict, field, value):
    return field in dict and dict[field] == value
