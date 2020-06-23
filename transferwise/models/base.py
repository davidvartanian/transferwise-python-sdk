from transferwise.client.config import API_VERSION


class TFModel:
    _api_version = API_VERSION
    _entity = None  # must be set in concrete class
    _api_path_pattern = '{api_version}/{entity}'
    _sync_data = None
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

    def post(self, client):
        self._sync_data = client.post(self._get_path(), {k: v for k, v in self.__dict__ if not k.startswith('_')})

    @classmethod
    def _get_path(cls, object_id=None):
        path = cls._api_path_pattern.format(api_version=cls._api_version, entity=cls._entity)
        if object_id:
            path += f'/{object_id}'
        return path
