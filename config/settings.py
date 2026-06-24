# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    supabase_table: str
    contact_ids: list[int]
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str
    max_contacts: int
    supabase_timeout_seconds: int
    dry_run: bool

    @classmethod
    def load(cls) -> "Settings":
        max_contacts = cls._parse_max_contacts()
        supabase_url = cls._required_env("SUPABASE_URL")
        cls._validate_supabase_url(supabase_url)

        return cls(
            supabase_url=supabase_url,
            supabase_key=cls._required_env("SUPABASE_KEY"),
            supabase_table=os.getenv("SUPABASE_TABLE", "contatos").strip() or "contatos",
            contact_ids=cls._parse_contact_ids(os.getenv("CONTACT_IDS", "")),
            zapi_instance_id=cls._required_env("ZAPI_INSTANCE_ID"),
            zapi_token=cls._required_env("ZAPI_TOKEN", fallback_name="ZAPI_INSTANCE_TOKEN"),
            zapi_client_token=cls._required_env("ZAPI_CLIENT_TOKEN"),
            max_contacts=max_contacts,
            supabase_timeout_seconds=cls._parse_positive_int("SUPABASE_TIMEOUT_SECONDS", 15),
            dry_run=cls._parse_bool(os.getenv("DRY_RUN", "true")),
        )

    @staticmethod
    def _required_env(name: str, fallback_name: str | None = None) -> str:
        value = os.getenv(name, "").strip()

        if not value and fallback_name:
            value = os.getenv(fallback_name, "").strip()

        if not value:
            names = f"{name} ou {fallback_name}" if fallback_name else name
            raise ValueError(f"Variavel de ambiente obrigatoria ausente: {names}")

        return value

    @staticmethod
    def _validate_supabase_url(value: str) -> None:
        if "supabase.com/dashboard" in value:
            raise ValueError(
                "SUPABASE_URL esta com a URL do painel do Supabase. "
                "Use a URL da API do projeto, no formato https://SEU_PROJECT_REF.supabase.co"
            )

        if not value.startswith("https://") or not value.endswith(".supabase.co"):
            raise ValueError(
                "SUPABASE_URL deve estar no formato https://SEU_PROJECT_REF.supabase.co"
            )

    @staticmethod
    def _parse_bool(value: str) -> bool:
        return value.strip().lower() in {"1", "true", "yes", "sim", "s"}

    @staticmethod
    def _parse_contact_ids(value: str) -> list[int]:
        contact_ids: list[int] = []

        for item in value.split(","):
            item = item.strip()
            if not item:
                continue

            try:
                contact_ids.append(int(item))
            except ValueError as error:
                raise ValueError("CONTACT_IDS deve conter apenas IDs numericos separados por virgula.") from error

        return contact_ids

    @staticmethod
    def _parse_max_contacts() -> int:
        try:
            max_contacts = int(os.getenv("MAX_CONTACTS", "3"))
        except ValueError as error:
            raise ValueError("MAX_CONTACTS deve ser um numero entre 1 e 3.") from error

        if max_contacts < 1 or max_contacts > 3:
            raise ValueError("MAX_CONTACTS deve estar entre 1 e 3.")

        return max_contacts

    @staticmethod
    def _parse_positive_int(name: str, default: int) -> int:
        try:
            value = int(os.getenv(name, str(default)))
        except ValueError as error:
            raise ValueError(f"{name} deve ser um numero inteiro positivo.") from error

        if value <= 0:
            raise ValueError(f"{name} deve ser maior que zero.")

        return value
