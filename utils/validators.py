# -*- coding: utf-8 -*-

import re
from typing import Any


def normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone)


def mask_phone(phone: str) -> str:
    if len(phone) <= 4:
        return "****"
    return f"{phone[:4]}***{phone[-4:]}"


def validate_contact(contact: dict[str, Any]) -> tuple[str, str]:
    name = str(contact.get("nome") or "").strip()
    phone = normalize_phone(str(contact.get("telefone") or ""))

    if not name:
        raise ValueError("Contato sem nome.")

    if not phone:
        raise ValueError(f"Contato {name} sem telefone.")

    if len(phone) < 10 or len(phone) > 15:
        raise ValueError(f"Telefone invalido para {name}: use codigo do pais + DDD + numero.")

    return name, phone
