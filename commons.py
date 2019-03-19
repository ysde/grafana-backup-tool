def print_horizontal_line():
    print('')
    print("########################################")
    print('')

def log_response(resp):
    status_code = resp.status_code
    print("status: {0}".format(status_code))
    print("body: {0}".format(resp.content.decode('utf8')))
    return resp
