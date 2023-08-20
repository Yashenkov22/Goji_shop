from typing import Any

from utils.keyboards.shop_keyboards import create_photo_keyboard

def item_constructor(data: dict[str,Any]):
    photo_idx = data['photo_idx']
    photos = data['photos']
    kb_init: str
    
    if len(photos) == 1:
        kb_init = 'one'
    
    else:
        if photo_idx == 0:
            kb_init = 'start'
        elif photo_idx < len(data['photos'])-1:
            kb_init = 'mid'
        else:
            kb_init = 'end'

    photo_kb = create_photo_keyboard(kb_init)
    photo = data['photos'][photo_idx]
    name = data['name']
    price = data['price']

    return (
        name,
        price,
        photo,
        photo_kb
    )