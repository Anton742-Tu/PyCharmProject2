from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date


if __name__ == "__main__":
    print(get_mask_card_number(1234565409877654))
    print(get_mask_account(3456))
    print(mask_account_card("American Express 123456789087543"))
    print(get_date("2024-03-11T02:26:18.671407"))
