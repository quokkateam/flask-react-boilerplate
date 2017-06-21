class Config(object):
  STUFF = 'stuff'


class TestConfig(Config):
  STUFF = 'test stuff'
  ENVIRONMENT = 'test'
  DATABASE_URL = 'postgresql://username:password@localhost/test_db_name?user=test_user'


class DevelopmentConfig(Config):
  STUFF = 'dev stuff'
  ENVIRONMENT = 'development'
  DATABASE_URL = 'postgresql://username:password@localhost/dev_db_name?user=dev_user'


class ProductionConfig(Config):
  STUFF = 'prod stuff'
  ENVIRONMENT = 'production'
  DATABASE_URL = 'postgresql://username:password@localhost/prod_db_name?user=prod_user'