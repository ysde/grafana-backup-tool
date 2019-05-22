import sys

def print_horizontal_line():
    print('')
    print("########################################")
    print('')

def log_response(resp):
    status_code = resp.status_code
    print("[debug] status: {0}".format(status_code))
    print("[debug] body: {0}".format(resp.json()))
    return resp

def toPython2And3CompatibleString(someString):
    if sys.version_info[0] > 2:
        return someString
    else:
        return someString.encode('utf8')
