from fastapi_auth0 import Auth0

auth = Auth0(domain='pexl.us.auth0.com',
             api_audience='mmbe.planetexpresslabs.io',
             scopes={'read': 'read'})
