import os
import requests
from typing import Dict, Any, Optional

class SerperService:
    def __init__(self):
        self.api_keys = [
            os.getenv('SERPER_API_KEY_1'),
            os.getenv('SERPER_API_KEY_2')
        ]
        self.current_key_index = 0
        self.base_url = 'https://google.serper.dev/search'

    def _get_current_api_key(self) -> str:
        return self.api_keys[self.current_key_index]

    def _rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    def search(self, keyword: str, country: str, device: str) -> Optional[Dict[str, Any]]:
        headers = {
            'X-API-KEY': self._get_current_api_key(),
            'Content-Type': 'application/json'
        }
        
        data = {
            'q': keyword,
            'gl': country,  # Country code
            'device': device
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # If first key fails, try with second key
            if self.current_key_index == 0:
                self._rotate_api_key()
                return self.search(keyword, country, device)
            return None

    def parse_results(self, response: Dict[str, Any]) -> list:
        if not response or 'organic' not in response:
            return []

        results = []
        for idx, item in enumerate(response['organic'], 1):
            results.append({
                'rank': idx,
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', '')
            })
        return results