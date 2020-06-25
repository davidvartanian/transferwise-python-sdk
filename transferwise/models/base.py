import re
import uuid
from decimal import Decimal
from transferwise.client.config import API_VERSION
from transferwise.utils import camelcase, snakecase


class TFModel(object):
    _api_version = API_VERSION
    _entity = None  # must be set in concrete class
    _api_path_pattern = '{api_version}/{entity}'
    id = None

    def __init__(self):
        self._sync = {}

    def __getattribute__(self, item):
        if not item.startswith('_'):
            keys = set([k for k in self.__dict__.keys() if not k.startswith('_')])
            keys.update([k for k in self._sync.keys()])
            if item in keys and self._sync.get(item, None):
                return self._sync.get(item)

        return super().__getattribute__(item)


    @classmethod
    def create_from_dict(cls, data: dict):
        model = cls()
        for k, v in data.items():
            setattr(model, k, v)
        return model

    @classmethod
    def get(cls, client, object_id=None):
        response = client.get(cls._get_path(object_id))
        if isinstance(response, list):
            return [cls.create_from_dict(item) for item in response]
        return cls.create_from_dict(response)

    @classmethod
    def _get_path(cls, object_id=None, **kwargs):
        path = cls._api_path_pattern.format(api_version=cls._api_version, entity=cls._entity, **kwargs)
        if object_id:
            path += f'/{object_id}'
        return path

    def _validate_group(self, group, errors):
        local_key = snakecase(group['key'])
        if hasattr(self, local_key):
            value = getattr(self, local_key, None)
        else:
            value = self.details.get(group['key'], None)

        if group['required'] and not value:
            errors.append(group)
        elif not group['required'] and not value:
            return
        if group['validationRegexp']:
            match = re.match(r'^[A-Z]{2}[a-zA-Z0-9 ]{12,40}$', value)
            if not match:
                errors.append(group)
        if group['minLength'] and len(value) < group['minLength']:
            errors.append(group)
        if group['maxLength'] and len(value) > group['maxLength']:
            errors.append(group)
        if group['valuesAllowed']:
            if value not in [v['key'] for v in group['valuesAllowed']]:
                errors.append(group)

    def attr(self, key):
        return super().__getattribute__(key)

    def post(self, client, *args, **kwargs):
        data = client.post(self._get_path(**kwargs), payload=self.to_json())
        if isinstance(data, dict):
            for k, v in data.items():
                self._sync[snakecase(k)] = v
        elif isinstance(data, list):
            self._sync = data

    def to_json(self):
        serializable = {}
        attrs = dict(self.__class__.__dict__)
        attrs.update(self.__dict__)
        for k, v in attrs.items():
            if k.startswith('_') or callable(getattr(self, k)):
                continue
            k = camelcase(k)
            if isinstance(v, TFModel):
                serializable[k] = v.id  # if no id, it wasn't synced
            elif isinstance(v, Decimal):
                serializable[k] = float(f'{v.normalize():f}')
            elif isinstance(v, uuid.UUID):
                serializable[k] = f'{v}'
            else:
                serializable[k] = v
        return serializable

