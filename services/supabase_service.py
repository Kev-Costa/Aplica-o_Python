# -*- coding: utf-8 -*-

from typing import Any

import httpx
from postgrest.exceptions import APIError
from supabase import Client, ClientOptions, create_client

from config.settings import Settings


class SupabaseService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        options = ClientOptions(postgrest_client_timeout=settings.supabase_timeout_seconds)
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key, options)

    def fetch_contacts(self) -> list[dict[str, Any]]:
        query = (
            self.client.table(self.settings.supabase_table)
            .select("id,nome,telefone")
            .order("id")
            .limit(self.settings.max_contacts)
        )

        if self.settings.contact_ids:
            query = query.in_("id", self.settings.contact_ids)

        try:
            response = query.execute()
            return response.data or []
        except httpx.TimeoutException as error:
            raise RuntimeError(
                "Tempo esgotado ao conectar no Supabase. "
                "Verifique sua internet, a SUPABASE_URL e se o projeto Supabase esta ativo."
            ) from error
        except APIError as error:
            raise RuntimeError(
                "Erro retornado pelo Supabase. "
                "Verifique se a tabela existe, se as colunas estao corretas e se a SUPABASE_KEY tem permissao de leitura."
            ) from error
        except Exception as error:
            raise RuntimeError(
                "Nao foi possivel buscar contatos no Supabase. "
                "Confira SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE e CONTACT_IDS."
            ) from error
