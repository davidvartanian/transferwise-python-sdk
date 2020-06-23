from transferwise.client.config import FUND_API_VERSION
from transferwise.models.base import TFModel


class Fund(TFModel):
    _api_version = FUND_API_VERSION
    _api_path_pattern = '{api_version}/profiles/{profile_id}/transfers/{transfer_id}/{entity}'
    _entity = 'payments'
    profile = None  # Profile model
    transfer = None  # Transfer model

    def _get_path(self):
        return self._api_path_pattern.format(api_version=self._api_version,
                                             profile_id=self.profile.id,
                                             transfer_id=self.transfer.id,
                                             entity=self._entity)
