import json
import random
import string

from django.test.client import Client
from mixer.backend.django import mixer


class DRFClient(Client):
    def __init__(self,
                 user=None,
                 god_mode=True,
                 anon=False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if not anon:
            self.auth(user, god_mode)

    def get(self, *args, **kwargs):
        return self._api_call('get',
                              kwargs.get('expected_status_code', 200),
                              *args,
                              **kwargs)

    def post(self, *args, **kwargs):
        return self._api_call('post',
                              kwargs.get('expected_status_code', 201),
                              *args,
                              **kwargs)

    def put(self, *args, **kwargs):
        return self._api_call('put',
                              kwargs.get('expected_status_code', 200),
                              *args,
                              **kwargs)

    def delete(self, *args, **kwargs):
        return self._api_call('delete',
                              kwargs.get('expected_status_code', 204),
                              *args,
                              **kwargs)

    def auth(self, user=None, god_mode=True):
        self.user = user or self._create_user(god_mode)
        self.god_mode = god_mode

        self.force_login(self.user)

    def logout(self):
        super().logout()

    def _create_user(self, god_mode=True):
        client = self._create_client()

        user_opts = dict()
        if god_mode:
            user_opts = {
                'is_staff': True,
                'is_superuser': True,
                'client': client,
            }
        user = mixer.blend('auth.User', **user_opts)
        self.password = ''.join([random.choice(string.hexdigits)
                                for _ in range(0, 6)])
        user.set_password(self.password)
        user.save()
        return user

    def _api_call(self, method, expected, *args, **kwargs):
        # by default submit all data in JSON
        kwargs['format'] = kwargs.get('format', 'json')
        as_response = kwargs.pop('as_response', False)

        method = getattr(super(), method)
        response = method(*args, **kwargs)

        if as_response:
            return response

        content = self._decode(response)
        content = self._convert_response(content)

        assert response.status_code == expected, content

        return content

    def _convert_response(self, content):
        if not content:
            return content

        if isinstance(content, str):
            return content

        if isinstance(content, dict):
            self._convert_dict_value_to_str(content)
            return content

        new_content = []
        for item in content:
            self._convert_dict_value_to_str(item)
            new_content.append(item)

        return new_content

    def _convert_dict_value_to_str(self, item):
        if isinstance(item, list):
            self._convert_list_to_str(item)
            return None

        if isinstance(item, str):
            return item

        for key in item.keys():
            if isinstance(item[key], str):
                continue

            if isinstance(item[key], dict):
                dict_item = item[key]
                self._convert_dict_value_to_str(dict_item)
                item[key] = dict_item
                continue

            if isinstance(item[key], list):
                new_contents = []
                for list_item in item[key]:
                    self._convert_dict_value_to_str(list_item)
                    new_contents.append(list_item)
                item[key] = new_contents
                continue

            item[key] = str(item[key])

    def _convert_list_to_str(self, items):
        new_list = []
        for item in items:
            if isinstance(item, dict):
                self._convert_dict_value_to_str(item)
                new_list.append(item)
                continue

            if isinstance(item, list):
                self._convert_list_to_str(item)
                new_list.append(item)
                continue

            new_list.append(str(item))

    def _decode(self, response):
        if not len(response.content):
            return

        content = response.content.decode('utf-8', errors='ignore')
        if 'application/json' in response.headers['Content-Type']:
            return json.loads(content)
        else:
            return content
