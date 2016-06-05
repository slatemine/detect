__author__ = 'peter.tillotson'

from engine import Engine
import logging, os, yaml

cwd = os.getcwd()
if cwd.endswith('src'):
    os.chdir('..')
config = yaml.load( open('config.yml') )
levels = {
    'debug': logging.DEBUG,
    'critical' : logging.CRITICAL,
    'error': logging.ERROR,
    'info' : logging.INFO,
    'warn' : logging.WARN
}
level = levels.get(config['defaults']['logging']['level'].strip().lower())
format = config['defaults']['logging']['format']
logging.basicConfig(level=level, format=format)
engine = Engine( config )
try:
    engine.start()
    engine.stop()
except Exception as e:
    logging.exception(e)

finally:
    engine.close()
