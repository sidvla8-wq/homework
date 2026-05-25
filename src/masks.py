from log_config import setup_logger

# Создаём логгер для модуля masks
logger = setup_logger(__name__, 'masks.log')

# Пример использования логгера
def apply_mask(data):
    logger.info("Применяем маску к данным")
    try:
        # Логика применения маски
        result = data
        logger.debug("Маска успешно применена")
        return result
    except Exception as e:
        logger.error(f"Ошибка при применении маски: {e}")
        raise


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    card = card_number.replace(" ", "")
    if not card.isdigit():
        return "Номер карты должен состоять из цифр!"
    if len(card) != 16:
        return "Номер карты не содержит 16 цифр"
    mask_card = card[:4] + " " + card[4:6] + "**" + " " + "****" + " " + card[-4:]
    return mask_card


def get_mask_account(account: str) -> str:
    """Функция маскировки номера банковского счёта"""
    acnt = account.replace(" ", "")
    if not acnt.isdigit():
        return "Счёт должен состоять из цифр!"
    if len(acnt) != 20:
        return "Счёт не равен 20 цифрам"
    mask_account = "**" + acnt[-4:]
    return mask_account
