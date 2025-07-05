import json
from dataclasses import dataclass
from typing import Any, List

import httpx
from fastapi import UploadFile


@dataclass
class ExternalServiceFacade:
    async_client: httpx.AsyncClient
    access_token: str

    async def proxy_get(
            self,
            endpoint: str,
            base_url: str,
            params: dict | None = None
    ) -> (json, int):
        async with self.async_client as client:
            response = await client.get(
                url=f"{base_url}/{endpoint}",
                params=params,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
        return response.json(), response.status_code

    async def proxy_post(
            self,
            endpoint: str,
            data: Any,
            base_url: str,
            files: List[UploadFile] | None = None,
    ) -> (json, int):
        async with self.async_client as client:
            files_data = None
            if files:
                files_data = [
                    ("files", (file.filename, file.file, file.content_type))
                    for file in files
                ]

            response = await client.post(
                url=f"{base_url}/{endpoint}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                json=data,
                files=files_data,
            )
            return response.json(), response.status_code

    async def proxy_patch(
            self,
            endpoint: str,
            data: Any,
            base_url: str
    ) -> (json, int):
        async with self.async_client as client:
            response = await client.patch(
                url=f"{base_url}/{endpoint}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                json=data,
            )
            return response.json(), response.status_code

    async def proxy_delete(self, endpoint: str, base_url: str) -> (json, int):
        async with self.async_client as client:
            response = await client.delete(
                url=f"{base_url}/{endpoint}",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            return response.json(), response.status_code
