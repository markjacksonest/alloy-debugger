import snowflake.connector
import requests
import json
import os

class SnowflakeDb:

    def get_snowflake_connector_with_token(self):
        return self._get_snowflake_connector(authenticator="oauth", token=self._get_snowflake_token())

    def get_snowflake_connector_with_external_browser(self):
        return self._get_snowflake_connector(authenticator="externalbrowser")

    def _get_snowflake_connector(self, **kwargs):
        return snowflake.connector.connect(
            user=f"{os.getenv('OKTA_USERNAME')}@earnest.com",
            account=os.environ['SNOWFLAKE_ACCOUNT'],
            role=os.environ['SNOWFLAKE_ROLE'],
            warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
            **kwargs
        )

    @staticmethod
    def _get_snowflake_token() -> str:
        url = os.getenv("SNOWFLAKE_TOKEN_GENERATOR_URL") + "/token"
        data = {
            "okta_username": os.getenv("OKTA_USERNAME"),
            "okta_password": os.getenv("OKTA_PASSWORD"),
            "snowflake_role": os.getenv("SNOWFLAKE_ROLE"),
        }
        response = requests.post(url=url, data=json.dumps(data))
        if response.ok:
            return response.json()["token"]
        raise ValueError("Error getting the token. Check your credentials.")