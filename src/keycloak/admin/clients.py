import json
from keycloak.admin import KeycloakAdminBase
from keycloak.utils import to_camel_case 
from collections import OrderedDict
from .clientroles import ClientRoles

__all__ = ('Client', 'Clients',)

# https://www.keycloak.org/docs-api/8.0/rest-api/index.html#_clientrepresentation
CLIENTS_KWARGS = [
    'access',
    'adminUrl',
    'attributes',
    'authenticationFlowBindingOverrides',
    'authorizationServicesEnabled',
    'authorizationSettings',
    'baseUrl',
    'bearerOnly',
    'clientAuthenticatorType',
    'clientId',
    'consentRequired',
    'defaultClientScopes',
    'defaultRoles',
    'description',
    'directAccessGrantsEnabled',
    'enabled',
    'frontchannelLogout',
    'fullScopeAllowed',
    'id',
    'implicitFlowEnabled',
    'name',
    'nodeReRegistrationTimeout',
    'notBefore',
    'optionalClientScopes',
    'origin',
    'protocol',
    'protocolMappers',
    'publicClient',
    'redirectUris',
    'registeredNodes',
    'registrationAccessToken',
    'rootUrl',
    'secret',
    'serviceAccountsEnabled',
    'standardFlowEnabled',
    'surrogateAuthRequired',
    'webOrigins',
]


class Clients(KeycloakAdminBase):
    _realm_name = None
    _paths = {
        'collection': '/auth/admin/realms/{realm}/clients'
    }

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Clients, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            )
        )

    def by_id(self, id):
        return Client(client=self._client, realm_name=self._realm_name, id=id)

    def create(self, *args, **kwargs):
        payload = OrderedDict()
        for key in kwargs:
            _key = to_camel_case(key)
            if _key in CLIENTS_KWARGS:
                payload[_key] = kwargs[key]


        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            ),
            data=json.dumps(payload)
        )



class Client(KeycloakAdminBase):
    _id = None
    _realm_name = None
    _paths = {
        'single': '/auth/admin/realms/{realm}/clients/{id}'
    }

    def __init__(self, realm_name, id, *args, **kwargs):
        self._id = id
        self._realm_name = realm_name
        super(Client, self).__init__(*args, **kwargs)

    @property
    def roles(self):
        return ClientRoles(client=self._client, client_id=self._id,
                           realm_name=self._realm_name)

    def update(self, *args, **kwargs):
        payload = OrderedDict()
        for key in kwargs:
            _key = to_camel_case(key)
            if _key in CLIENTS_KWARGS:
                payload[_key] = kwargs[key]


        return self._client.put(
            url=self._client.get_full_url(
                self.get_path('single', realm=self._realm_name, id=self._id)
            ),
            data=json.dumps(payload)
        )

    def delete(self):

        return self._client.delete(
            url=self._client.get_full_url(
                self.get_path('single', realm=self._realm_name, id=self._id)
            )
        )




