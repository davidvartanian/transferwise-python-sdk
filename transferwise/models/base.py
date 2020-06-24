import uuid
from decimal import Decimal
from transferwise.client.config import API_VERSION
from transferwise.utils import camelcase, snakecase


class TFModel(object):
    _api_version = API_VERSION
    _entity = None  # must be set in concrete class
    _api_path_pattern = '{api_version}/{entity}'
    _sync = {}
    id = None

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
    def _get_path(cls, object_id=None):
        path = cls._api_path_pattern.format(api_version=cls._api_version, entity=cls._entity)
        if object_id:
            path += f'/{object_id}'
        return path

    def post(self, client):
        data = client.post(self._get_path(), payload=self.to_json())
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
                serializable[k] = v._sync.get('id')  # if no id it wasn't synced
            elif isinstance(v, Decimal):
                serializable[k] = f'{v.normalize():f}'
            elif isinstance(v, uuid.UUID):
                serializable[k] = f'{v}'
            else:
                serializable[k] = v
        return serializable

