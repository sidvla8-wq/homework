def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    card = card_number.replace(" ", "")
    if not card.isdigit():
        return "Номер карты должен состоять из цифр!"
    if len(card) != 16:
        return "Номер карты не содержит 16 цифр"
    mask_card = card[:4] + " " + card[4:6] + "**" + " " + "****" + card[-4:]
    return mask_card


def get_mask_account(account: str) -> str:
    """Функция маскировки номера банковского счёта"""
    acnt = account.replace(" ", "")
    if not acnt.isdigit():
        return "Счёт должен состоять из цифр"
    if len(acnt) != 20:
        return "Счёт не равен 20 цифрам"
    mask_account = "**" + acnt[-4:]
    return mask_account
