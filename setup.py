from setuptools import setup, find_packages
# Global variables
requires = [
    'requests',
    'docopt',
    'boto3',
    'python-dotenv',
    'azure-storage-blob',
    'google-cloud-storage',
    'influxdb',
    'packaging'
]
setup(
    name="grafana-backup-tool",
    version="1.4.5",
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'grafana-backup=grafana_backup.cli:main',
        ],
    },
)