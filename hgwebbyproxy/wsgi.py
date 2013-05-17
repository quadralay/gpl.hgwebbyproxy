import cache
import logging
import mercurial.hgweb
import os
import sys
import traceback
import webob.exc
import wsgiref.util


__logger__ = logging.getLogger(__name__)


class HGWebByProxy(object):
    def __init__(self):
        self.__cache = cache.CacheRecent()

    def __call__(self, environ, start_response):
        result = None
    
        __logger__.debug('redirect_app: 1')
    
        try:
            if (('HTTP_PROXY_HG_PATH' in environ) and ('HTTP_PROXY_HG_SCRIPT_NAME' in environ)):
                __logger__.debug('redirect_app: 2')
                proxy_hg_path = environ['HTTP_PROXY_HG_PATH']
                proxy_hg_script_name = environ['HTTP_PROXY_HG_SCRIPT_NAME']
                __logger__.debug('redirect_app: proxy_hg_path == %s' % proxy_hg_path)
                __logger__.debug('redirect_app: proxy_hg_script_name == %s' % proxy_hg_script_name)
    
                __logger__.debug('redirect_app: 3')
                __logger__.debug('proxy_hg_app: PATH_INFO == %s' % environ['PATH_INFO'])
                __logger__.debug('proxy_hg_app: SCRIPT_NAME == %s' % environ['SCRIPT_NAME'])
                while (len(environ['SCRIPT_NAME']) < len(proxy_hg_script_name)):
                    wsgiref.util.shift_path_info(environ)
                __logger__.debug('proxy_hg_app: PATH_INFO == %s' % environ['PATH_INFO'])
                __logger__.debug('proxy_hg_app: SCRIPT_NAME == %s' % environ['SCRIPT_NAME'])
    
                # Check cache
                #
                if (proxy_hg_path in self.__cache):
                    # Found existing hgweb app
                    #
                    hgweb_app = self.__cache[proxy_hg_path]
                    result = hgweb_app(environ, start_response)
                    __logger__.debug('redirect_app: 4 - cache hgweb')
                else:
                    # Need to create hgweb app
                    #
                    __logger__.debug('redirect_app: 5')
                    if (os.path.isdir(proxy_hg_path)):
                        __logger__.debug('redirect_app: 6')
                        # Create Mercurial web application
                        #
                        # [web]
                        # allow_push = *
                        # push_ssl = false
                        #
                        hgweb_app = mercurial.hgweb.hgweb(proxy_hg_path)
    
                        # Cache hgweb app
                        #
                        self.__cache[proxy_hg_path] = hgweb_app
    
                        result = hgweb_app(environ, start_response)
                        __logger__.debug('redirect_app: 7 - created hgweb')
        
            __logger__.debug('redirect_app: 8')
            if (result is None):
                raise webob.exc.HTTPNotFound()
        
        except webob.exc.HTTPException as http_exception:
            __logger__.error('HTTPException...')
            result = http_exception(environ, start_response)
    
        except:
            __logger__.error('Unexpected exception...')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            __logger__.error(message)
    
        return result
