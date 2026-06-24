# -*- coding: utf-8 -*-

from config.settings import Settings
from services.supabase_service import SupabaseService
from services.zapi_service import ZApiService
from utils.logger import setup_logger
from utils.validators import mask_phone, validate_contact


logger = setup_logger()


def main() -> None:
    try:
        settings = Settings.load()
        logger.info("Variaveis de ambiente carregadas.")
        logger.info(
            "Filtro carregado: CONTACT_IDS=%s | MAX_CONTACTS=%s | DRY_RUN=%s",
            settings.contact_ids or "todos",
            settings.max_contacts,
            settings.dry_run,
        )

        supabase = SupabaseService(settings)
        zapi = ZApiService(settings)

        contacts = supabase.fetch_contacts()

        if not contacts:
            logger.warning("Nenhum contato encontrado.")
            return

        logger.info("%s contato(s) encontrado(s).", len(contacts))

        for contact in contacts:
            try:
                name, phone = validate_contact(contact)
                message = f"Olá, {name} tudo bem com você?"

                if settings.dry_run:
                    logger.info("[DRY_RUN] Enviaria para %s: %s", mask_phone(phone), message)
                    continue

                zapi.send_text_message(phone, message)
                logger.info("Mensagem enviada para %s.", name)
            except Exception as error:
                logger.exception(
                    "Erro ao processar contato id=%s: %s",
                    contact.get("id"),
                    error,
                )
    except KeyboardInterrupt:
        logger.warning("Execucao interrompida pelo usuario.")
    except Exception as error:
        logger.error("Erro geral da aplicacao: %s", error)


if __name__ == "__main__":
    main()
