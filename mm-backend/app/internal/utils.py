from fastapi_auth0 import Auth0

auth = Auth0(domain='dev-hx0dlu6f.us.auth0.com',
             api_audience='testing',
             scopes={'read': 'read'})
