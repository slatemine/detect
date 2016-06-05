__author__ = 'peter.tillotson'

from string import Template
from analysis import Analysis
import datetime, geoip2.database, logging, json, pytz

class Engine:
    logger = logging.getLogger('engine')
    def __init__(self, config):
        self.config = config
        self.geoip_db = {}
        self.geoip_db['city'] = geoip2.database.Reader( self.config['geoip']['db']['city'] )
        self.geoip_db['isp'] = geoip2.database.Reader( self.config['geoip']['db']['isp'] )

    def start(self):
        self.logger.info('Staring')
        nab_root = self.config['nab']['root']

        results={}
        for job in self.config['work']:
            cfg = self.config['defaults']['job'].copy()
            job = merge(cfg, job)
            self.logger.info(json.dumps(job, indent=4))
            filename = job['data']
            self.logger.info('Processing data %s'%(filename))
            filename = Template(filename).substitute( {'nab_root': nab_root} )
            job['data'] = filename
            analysis = Analysis( self.geoip_db )
            method_name = job['analysis']['method']
            method = getattr(analysis, method_name)
            results = method(results, job=job)
            n_res = 0
            if results is not None:
                n_res = len(results)
            if self.logger.isEnabledFor(logging.DEBUG):
                msg = json.dumps(results, indent=4)
                self.logger.debug(msg)
            self.logger.info( 'Job complete')


    def stop(self):
        self.logger.info('Stopping')
        pass

    def close(self):
        self.logger.info('Closing')
        # If they exist
        # Close down maxmind giop db
        databases = ['city', 'isp']
        for db in databases:
            if self.geoip_db[db] is not None:
                self.geoip_db[db].close()



def utc_now():
    now = datetime.datetime.utcnow()
    now= now.replace(tzinfo=pytz.utc)
    return now

def merge(a, b):
    for key, value in b.items():
        if type( value ) == type(dict()):
            a[key] = merge(a[key], value)
        else:
            a[key] = value
    return a
