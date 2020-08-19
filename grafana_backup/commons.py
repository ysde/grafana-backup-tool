import sys, json


def left_ver_newer_than_right_ver(current_version, specific_version):
    def convertVersion(ver):
        return int(''.join(ver.split("-")[0].split(".")))
    return convertVersion(current_version) > convertVersion(specific_version)


def print_horizontal_line():
    print('')
    print("########################################")
    print('')


def log_response(resp):
    status_code = resp.status_code
    print("[DEBUG] status: {0}".format(status_code))
    print("[DEBUG] body: {0}".format(resp.json()))
    return resp


def to_python2_and_3_compatible_string(some_string):
    if sys.version_info[0] > 2:
        return some_string
    else:
        return some_string.encode('utf8')


def load_config(path=None):
    config = None

    try:
        with open(path, 'r') as f:
            config = json.load(f)
        f.closed
    except IOError as e:
        print(str(e))
        sys.exit(2)

    return config
