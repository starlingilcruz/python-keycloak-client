import json
from collections import OrderedDict
from keycloak.utils import to_camel_case
from keycloak.admin import KeycloakAdminBase

__all__ = ('Groups',)

# https://www.keycloak.org/docs-api/7.0/rest-api/index.html#_grouprepresentation
GROUPS_KWARGS = [
    'access'
    'attributes'
    'client_roles'
    'name'
    'path'
    'realm_roles'
    'sub_groups'
]


class Groups(KeycloakAdminBase):
    _BASE = '/auth/admin/realms/{realm}'
    _paths = {
        'collection': _BASE + '/groups',
        'children': _BASE + '/groups/{group_id}/children',
        'by_path': _BASE + '/group-by-path/{group_path}'
    }
    _kwargs = GROUPS_KWARGS

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(Groups, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name,
                )
            ),
        )

    def create(self, name, **kwargs):
        """
        Create a group in Keycloak

        https://www.keycloak.org/docs-api/7.0/rest-api/index.html#_grouprepresentation

        :param name
        :param path
        :param access
        :param attributes
        :param client_roles
        :param realm_roles
        :param sub_groups
        """
        payload = OrderedDict(name=name)
        for key in GROUPS_KWARGS:
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name
                )
            ),
            data=json.dumps(payload)
        )

    def by_path(self, path):
        """
        Get group by given path
        https://www.keycloak.org/docs-api/4.8/rest-api/#_getgroupbypath
        :param path:
        :return:
        """
        return self._client.get(
            url=self._client.get_full_url(
                self.get_path('by_path',
                              realm=self._realm_name,
                              group_path=path)
            )
        )

    def by_id(self, group_id):
        return Group(realm_name=self._realm_name,
                     group_id=group_id,
                     client=self._client)

    def move(self, from_id, to_id):
        """
        Move a group as a subgroup to other group
        :param from_id:
        :param to_id:
        :return:
        """
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'children',
                    realm=self._realm_name,
                    group_id=to_id
                )
            ),
            data=json.dumps({'id': from_id})
        )

    def move_to_root(self, group_id, name):
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'collection',
                    realm=self._realm_name
                )
            ),
            data=json.dumps({'id': group_id, 'name': name})
        )


class Group(KeycloakAdminBase):
    _BASE = "/auth/admin/realms/{realm}"
    _paths = {
        'single': _BASE + '/groups/{group_id}',
        'children': _BASE + '/groups/{group_id}/children'
    }
    _kwargs = GROUPS_KWARGS

    def __init__(self, realm_name, group_id=None, *args, **kwargs):
        self._group_id = group_id
        self._realm_name = realm_name
        self._group = None
        super(Group, self).__init__(*args, **kwargs)

    @property
    def group(self):
        if self._group is None:
            return self.get()
        return self._group

    def get(self):
        """
        Return registered group with the given group id
        https://www.keycloak.org/docs-api/4.8/rest-api/#_grouprepresentation
        https://www.keycloak.org/docs-api/4.8/rest-api/#_getgroup
        """
        self._group = self._client.get(
            url=self._client.get_full_url(
                self.get_path(
                    'single',
                    realm=self._realm_name,
                    group_id=self._group_id
                )
            )
        )
        self._group_id = self._group["id"]
        return self._group

    def add_subgroup(self, name):
        return self._client.post(
            url=self._client.get_full_url(
                self.get_path(
                    'children',
                    realm=self._realm_name,
                    group_id=self._group_id
                )
            ),
            data=json.dumps({'name': name})
        )

