import json
import logging
from typing import List
from datetime import datetime

import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway

logger = logging.getLogger(__name__)


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    @classmethod
    def _datetime_encoder(cls, o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"{type(o)} object is not serializable")

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        if not processed_agent_data_batch:
            return True

        payload = json.dumps([batch.dict() for batch in processed_agent_data_batch], default=self._datetime_encoder)
        logger.info(payload)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(f"{self.api_base_url}/processed_agent_data", headers=headers, data=payload)

        if response.status_code == 200:
            logger.info("Successfully saved")
            return True

        logger.warning(f"Error occurred while saving AgentData. Status code: {response.status_code}. "
                       f"Message: {response.json()}")
        return False
