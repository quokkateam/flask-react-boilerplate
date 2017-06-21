import os
import re
from api.configs import vars

env = os.environ.get('ENV') or 'development'

config_vars_class = getattr(vars, '{}Config'.format(env.capitalize()))()


def get_config(key):
  if not hasattr(config_vars_class, key):
    return None
  
  val = getattr(config_vars_class, key)
  
  if val and re.match('true', val, re.I):
    val = True
  elif val and re.match('false', val, re.I):
    val = False
  
  return val
