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
    print("[DEBUG] resp status: {0}".format(status_code))
    print("[DEBUG] resp body: {0}".format(resp.json()))
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


def save_json(file_name, data, folder_path, extension, pretty_print):
    file_path = folder_path + '/' + file_name + '.' + extension
    with open(u"{0}".format(file_path), 'w') as f:
        if pretty_print:
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            f.write(json.dumps(data))
    # Return file_path for showing in the console message
    return file_path
