# Micromange Backend server

This handles both the websocket connections to clients and handling of information to clients.

### Things to note:
 - Tenants belong to an organization, multiple can be in each org.
 - Tenants are sometimes refered to sites. That is a legacy thing, and all mentions should be refactored.

### Things to do:
 - Maybe split websocket and frontend api to separate microservices to allow for easier scaling.
 - Docker!!!
