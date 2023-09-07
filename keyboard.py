from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton as ib
kbadmin = ReplyKeyboardMarkup(resize_keyboard=True)
kbadmin.row("📟Статистика","✉️Рассылка")

kbsend = ReplyKeyboardMarkup(resize_keyboard=True)
kbsend.row("С фото","Без фото"," 🐍Назад")

kbsub = InlineKeyboardMarkup()
kbsub.row(ib('〽️ Подписаться 1', url='https://t.me/+9LVPcbM4YOEzOGVi'))
kbsub.row(ib('〽️ Подписаться 2', url='https://t.me/+o9usEqFR1eNmMWZi'))
kbsub.row(ib('✅ Подписался', callback_data='subbed'))

kbmenu = InlineKeyboardMarkup()
kbmenu.add(ib('IP-адрес', callback_data='checkip'))
kbmenu.add(ib('BTC-адрес', callback_data='checkbtc'))
kbmenu.add(ib('MAC-адрес', callback_data='checkmac'))
kbmenu.add(ib('Никнейм', callback_data='checknick'))
kbmenu.add(ib('Номер телефона', callback_data='checknum'))
kbmenu.add(ib('BIN карты', callback_data='checkbin'))
kbmenu.add(ib('VK профиль', callback_data='checkvk'))

kbback = InlineKeyboardMarkup().row(ib('Назад', callback_data='back'))