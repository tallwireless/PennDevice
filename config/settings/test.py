from .base import *
from os import path
import saml2
from saml2.saml import NAMEID_FORMAT_PERSISTENT

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

SECRET_KEY = 'sntaoheuswvmaosenuh8aoe9782(*santoeussatnoe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += [ 'hussle.net.isc.upenn.edu' ]

STATIC_ROOT = '/home/charlesr/code/PennDevice/PennDevice/static/'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'penndevice-dev',
        'USER': 'penndevice-dev',
        'PASSWORD': '3c#BmdDCXyp4r!F2',
        'HOST': '127.0.0.1',
        'PORT': '5432', 
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'https://hussle.net.isc.upenn.edu/saml2/metadata/',

  # directory with attribute mapping
  #'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'PennDevice Registration - Testing',
          'name_id_format': NAMEID_FORMAT_PERSISTENT,
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('https://hussle.net.isc.upenn.edu/saml2/acs/',
                   saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ('https://hussle.net.isc.upenn.edu/saml2/ls/',
                   saml2.BINDING_HTTP_REDIRECT),
                  ('https://hussle.net.isc.upenn.edu/saml2/ls/post', saml2.BINDING_HTTP_POST),
                  ],
              },

           # attributes that this project need to identify a user
          'required_attributes': ['sn','givenName','mail','eduPersonPrincipalName'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'https://idp.pennkey.upenn.edu/idp/shibboleth': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://idp.pennkey.upenn.edu/idp/profile/SAML2/Redirect/SSO',
                      saml2.BINDING_HTTP_POST: 'https://idp.pennkey.upenn.edu/idp/profile/SAML2/POST/SSO',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASE_DIR, 'SAML/weblogin.metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # Signing
  'key_file': path.join(BASE_DIR, 'SAML/server.key'),  # private part
  'cert_file': path.join(BASE_DIR, 'SAML/server.crt'),  # public part

  # Encryption
  'encryption_keypairs': [{
  'key_file': path.join(BASE_DIR, 'SAML/server.key'),  # private part
  'cert_file': path.join(BASE_DIR, 'SAML/server.crt'),  # public part
#      'key_file': path.join(BASEDIR, 'SAML/my_encryption_key.key'),  # private part
#      'cert_file': path.join(BASEDIR, 'SAML/my_encryption_cert.pem'),  # public part
  }],

  # own metadata settings
  'contact_person': [
      {'given_name': 'Rumford',
       'sur_name': 'Charles',
       'company': 'UPenn',
       'email_address': 'charlesr@isc.upenn.edu',
       'contact_type': 'technical'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('UPenn', 'en')],
      'display_name': [('Upenn', 'en')],
      'url': [('http://www.upenn.edu', 'en')],
      },
  'valid_for': 24,  # how long is our metadata valid
  }

SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'eduPersonPrincipalName'
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = '__iexact'
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
            'eduPersonPrincipalName': ('username', ),
            'mail': ('email', ),
            'givenName': ('first_name', ),
            'sn': ('last_name', ),
        }
