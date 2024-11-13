import os
import logging
import shutil
import hashlib

logger = logging.getLogger(__name__)

class key:
    def __init__(self) -> None:
        pass
    def api_key(self):
        """Print REST API Key."""
        if os.environ.get('MOBSF_API_KEY'):
            logger.info('\nAPI Key read from environment variable')
            return os.environ['MOBSF_API_KEY']
    
        secret_file = os.path.join('/Users/zone/.MobSF/', 'secret')
        if self.is_file_exists(secret_file):
            try:
                _api_key = open(secret_file).read().strip()
                return self.gen_sha256_hash(_api_key)
            except Exception:
                logger.exception('Cannot Read API Key')
    
    def is_file_exists(self,file_path):
        if os.path.isfile(file_path):
            return True
        # This fix situation where a user just typed "adb" or another executable
        # inside settings.py/config.py
        if shutil.which(file_path):
            return True
        else:
            return False
    
    def gen_sha256_hash(self,msg):
        """Generate SHA 256 Hash of the message."""
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        hash_object = hashlib.sha256(msg)
        return hash_object.hexdigest()

