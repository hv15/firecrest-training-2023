class Config:
    '''Base configuration class for the Flask app'''


class DevConfig(Config):
    '''Class for development configuration'''
    DEBUG = True
    OIDC_CLIENT_ID = "FILL ME IN"
    OIDC_CLIENT_SECRET = "FILL ME IN"
    OIDC_AUTH_REALM = "firecrest-clients"
    OIDC_AUTH_BASE_URL = "https://auth.cscs.ch"
    SECRET_KEY = 'Sk9WiTSWqgwOrpXZ'
    SESSION_TYPE = "filesystem"
    FIRECREST_URL='https://firecrest.cscs.ch'
    SYSTEM_NAME='daint'
    SYSTEM_PARTITIONS=['normal', 'xfer']
    SYSTEM_RESERVATION=None
    USER_GROUP='FILL ME IN'
    SYSTEM_CONSTRAINTS=['mc', 'gpu', 'ssd']
    PROBLEM_SUBDIR = "f7t_training"
    PROBLEM_FILES = []
    SBATCH_TEMPLATE = "demo.sh.tmpl"
    POST_TEMPLATE = "demo_post.sh.tmpl"
    CLIENT_PORT = 9090
    # SSL configuration
    USE_SSL = False
