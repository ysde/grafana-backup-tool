import base64
import json
import os
from datetime import datetime
from grafana_backup.commons import load_config

def get_setting(config, section, key, env_name, default, transform=None):
    """
    Priority: Environment Variable > Config File > Default Value.
    Automatic bool to int and int to bool
    """
    val = os.getenv(env_name, config.get(section, {}).get(key, default))
    
    if transform == bool or (isinstance(val, str) and val.lower() in ['true', 'false']):
        return str(val).lower() == 'true'
    if transform == int:
        try:
            return int(val)
        except (ValueError, TypeError):
            return default
    return val

def main(config_path):
    config = load_config(config_path)
    config_dict = {}

    settings_map = [
        # Grafana Core
        ('grafana', 'url', 'GRAFANA_URL', '', None),
        ('grafana', 'token', 'GRAFANA_TOKEN', '', None),
        ('grafana', 'search_api_limit', 'SEARCH_API_LIMIT', 5000, int),
        ('grafana', 'default_user_password', 'DEFAULT_USER_PASSWORD', '00000000', None),
        ('grafana', 'version', 'GRAFANA_VERSION', None, None),
        ('grafana', 'admin_account', 'GRAFANA_ADMIN_ACCOUNT', '', None),
        ('grafana', 'admin_password', 'GRAFANA_ADMIN_PASSWORD', '', None),

        # General Settings
        ('general', 'debug', 'DEBUG', True, bool),
        ('general', 'api_health_check', 'API_HEALTH_CHECK', True, bool),
        ('general', 'api_auth_check', 'API_AUTH_CHECK', True, bool),
        ('general', 'verify_ssl', 'VERIFY_SSL', False, bool),
        ('general', 'client_cert', 'CLIENT_CERT', None, None),
        ('general', 'backup_dir', 'BACKUP_DIR', '_OUTPUT_', None),
        ('general', 'backup_file_format', 'BACKUP_FILE_FORMAT', '%Y%m%d%H%M', None),
        ('general', 'uid_dashboard_slug_suffix', 'UID_DASHBOARD_SLUG_SUFFIX', False, bool),
        ('general', 'pretty_print', 'PRETTY_PRINT', False, bool),
        ('general', 'backup_workers', 'BACKUP_WORKERS', 3, int),

        # AWS S3
        ('aws', 's3_bucket_name', 'AWS_S3_BUCKET_NAME', '', None),
        ('aws', 's3_bucket_key', 'AWS_S3_BUCKET_KEY', '', None),
        ('aws', 'default_region', 'AWS_DEFAULT_REGION', '', None),
        ('aws', 'access_key_id', 'AWS_ACCESS_KEY_ID', '', None),
        ('aws', 'secret_access_key', 'AWS_SECRET_ACCESS_KEY', '', None),
        ('aws', 'endpoint_url', 'AWS_ENDPOINT_URL', None, None),

        # Azure Storage
        ('azure', 'container_name', 'AZURE_STORAGE_CONTAINER_NAME', '', None),
        ('azure', 'connection_string', 'AZURE_STORAGE_CONNECTION_STRING', '', None),

        # GCP Storage
        ('gcp', 'gcs_bucket_name', 'GCS_BUCKET_NAME', '', None),
        ('gcp', 'gcs_bucket_path', 'GCS_BUCKET_PATH', '', None),

        # InfluxDB
        ('influxdb', 'measurement', 'INFLUXDB_MEASUREMENT', 'grafana_backup', None),
        ('influxdb', 'host', 'INFLUXDB_HOST', '', None),
        ('influxdb', 'port', 'INFLUXDB_PORT', 8086, int),
        ('influxdb', 'username', 'INFLUXDB_USERNAME', '', None),
        ('influxdb', 'password', 'INFLUXDB_PASSWORD', '', None),
        ('influxdb', 'database', 'INFLUXDB_DATABASE', '', None),
    ]

    for section, key, env, default, t_type in settings_map:
        config_dict[env] = get_setting(config, section, key, env, default, t_type)

    gcp_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', config.get('gcp', {}).get('google_application_credentials', ''))
    if gcp_creds:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_creds

    extra_headers_raw = os.getenv('GRAFANA_HEADERS', '')
    extra_headers = {}
    if extra_headers_raw:
        extra_headers = dict(h.split(':') for h in extra_headers_raw.split(',') if ':' in h)
    
    token = config_dict.get('GRAFANA_TOKEN')
    http_get = {'Authorization': f'Bearer {token}'} if token else {}
    http_post = {'Content-Type': 'application/json'}
    if token:
        http_post['Authorization'] = f'Bearer {token}'

    http_get.update(extra_headers)
    http_post.update(extra_headers)

    admin_user = config_dict['GRAFANA_ADMIN_ACCOUNT']
    admin_pass = config_dict['GRAFANA_ADMIN_PASSWORD']
    basic_auth = os.getenv('GRAFANA_BASIC_AUTH')

    if not basic_auth and admin_user and admin_pass:
        auth_bytes = f"{admin_user}:{admin_pass}".encode('utf8')
        basic_auth = base64.b64encode(auth_bytes).decode('utf8')

    get_basic = None
    post_basic = None
    if basic_auth:
        get_basic = {**http_get, 'Authorization': f'Basic {basic_auth}'}
        post_basic = {**http_post, 'Authorization': f'Basic {basic_auth}'}

    config_dict.update({
        'GRAFANA_BASIC_AUTH': basic_auth,
        'EXTRA_HEADERS': extra_headers,
        'HTTP_GET_HEADERS': http_get,
        'HTTP_POST_HEADERS': http_post,
        'HTTP_GET_HEADERS_BASIC_AUTH': get_basic,
        'HTTP_POST_HEADERS_BASIC_AUTH': post_basic,
        'TIMESTAMP': datetime.today().strftime(config_dict['BACKUP_FILE_FORMAT'])
    })

    return config_dict