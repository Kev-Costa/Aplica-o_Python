# -*- coding: utf-8 -*-

import requests

from config.settings import Settings


class ZApiService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def send_text_message(self, phone: str, message: str) -> None:
        url = (
            "https://api.z-api.io/instances/"
            f"{self.settings.zapi_instance_id}/token/{self.settings.zapi_token}/send-text"
        )
        headers = {
            "Client-Token": self.settings.zapi_client_token,
            "Content-Type": "application/json",
        }
        payload = {
            "phone": phone,
            "message": message,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.ok:
            return

        try:
            details = response.json()
        except ValueError:
            details = response.text

        if isinstance(details, dict) and details.get("error") == "your client-token is not configured":
            raise RuntimeError(
                "A Z-API informou que o Client-Token nao esta configurado. "
                "Configure/copiei o Client Token no painel da Z-API e coloque apenas o token em ZAPI_CLIENT_TOKEN."
            )

        raise RuntimeError(
            "Erro ao enviar mensagem pela Z-API "
            f"(status={response.status_code}, resposta={details})"
        )
