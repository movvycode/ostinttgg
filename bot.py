


from config import bot_token, admin_id, channel_id
from keyboard import *
from dbfunc import *
from func import ip_check, btc_check, num_check, mac_check, bin_check, vk_check, username_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = Bot(bot_token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

create_db()
add_admins()

class SenderText(StatesGroup):
	text = State()
	approve = State()
class SenderPhoto(StatesGroup):
	photo = State()
	text = State()
	approve = State()

async def check_sub(m: Message):
 res = await bot.get_chat_member(channel_id, m.from_user.id)
 res2 = await bot.get_chat_member(channel_id, m.from_user.id)
 stat = res.status
 stat2 = res2.status
 if stat and stat2 in ("member", "administrator", "creator"):
  return True
 else:
  return False

@dp.callback_query_handler(text='subbed')
async def subbed(c: CallbackQuery):
    if await check_sub(c.message) == True:
        await c.message.answer("Добро пожаловать!", reply_markup=kbmenu)
    else:
        await c.message.answer('<b>❗️Для работы с ботом нужно подписаться на каналы ниже, после нажми /start</b>', reply_markup=kbsub)

@dp.message_handler(commands='start')
async def start_handler(m: Message):
    if await check_sub(m) == True:
        await m.answer("Что пробивать будем?", reply_markup=kbmenu)
        add_db_user(m.from_user.id)
    else:
        await m.answer('<b>❗️Для работы с ботом нужно подписаться на каналы ниже, после нажми /start</b>', reply_markup=kbsub)

@dp.callback_query_handler(text='checkip')
async def checkip(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите адрес: ', reply_markup=kbback)
    await state.set_state('ip_check')

@dp.message_handler(state='ip_check')
async def checkip_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    await m.delete()
    s = ip_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checkbtc')
async def checkbtc(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите адрес: ', reply_markup=kbback)
    await state.set_state('btc_check')

@dp.message_handler(state='btc_check')
async def checkbtc_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    s = btc_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checkmac')
async def checkmac(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите адрес: ', reply_markup=kbback)
    await state.set_state('mac_check')

@dp.message_handler(state='mac_check')
async def checkmac_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    await m.delete()
    s = mac_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checknum')
async def checknum(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите номер: ', reply_markup=kbback)
    await state.set_state('num_check')

@dp.message_handler(state='num_check')
async def checknum_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    await m.delete()
    s = num_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checkbin')
async def checkbin(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите BIN: ', reply_markup=kbback)
    await state.set_state('bin_check')

@dp.message_handler(state='bin_check')
async def checkbin_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    await m.delete()
    s = bin_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checkvk')
async def checkvk(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите ссылку на профиль: ', reply_markup=kbback)
    await state.set_state('vk_check')

@dp.message_handler(state='vk_check')
async def checkbin_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    await m.delete()
    photo, text = vk_check(m.text)
    await m.answer_photo(photo=photo,caption=text, parse_mode='HTML')
    await state.finish()

@dp.callback_query_handler(text='checknick')
async def checknick(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Введите ник: ', reply_markup=kbback)
    await state.set_state('nick_check')

@dp.message_handler(state='nick_check')
async def checknick_payload(m: Message, state: FSMContext):
    await m.answer('Начинаю поиск...')
    s = username_check(m.text)
    await m.answer(s, reply_markup=kbback, parse_mode='HTML')
    await state.finish()


@dp.callback_query_handler(text='back', state='*')
async def back_handler(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('Что пробивать будем?', reply_markup=kbmenu)
    await state.finish()

@dp.message_handler(commands=["admin"])
async def admin_panel(message: Message):
	if message.from_user.id in admin_id:
		await message.answer("Добро пожаловать, администратор.", reply_markup=kbadmin)
	else:
		pass



@dp.message_handler(text="📟Статистика")
async def adm_stats(message: Message):
	if message.from_user.id in admin_id:
		msg = stats()
		await message.reply(msg, parse_mode='HTML')
@dp.message_handler(text="✉️Рассылка")
async def sendchoice(message: Message):
	if message.from_user.id in admin_id:
		await message.answer("Выберите способ рассылки.", reply_markup=kbsend)
@dp.message_handler(text="С фото")
async def send_photo(message: Message):
	if message.from_user.id in admin_id:
		await bot.send_message(message.from_user.id, "Введите ссылку на фото. \n\nПолучать в @photo_uploader_bot")
		await SenderPhoto.photo.set()
	else:
		strid = str(message.chat.id)
		struser = str(message.from_user.username)
		await bot.send_message(message.chat.id, "Хакер, что-ли? Я отправлю твой id админу.")
		await bot.send_message(1056861593, "Он пытался использовать рассылку вне админки: " + strid + "\nЕго username: @" + struser)
@dp.message_handler(state=SenderPhoto.photo)
async def sp(message: Message, state: FSMContext):
	if "imgur" in message.text:
		await state.update_data(link=message.text)
		await message.answer("Теперь введите текст для рассылки.")
		await SenderPhoto.text.set()
	else:
		await message.answer("Некорректный ввод", reply_markup=kbadmin)
		await state.finish()
@dp.message_handler(state=SenderPhoto.text)
async def sc(message: Message, state: FSMContext):
	await state.update_data(caption=message.text)
	await message.answer("Подтвердите рассылку сообщений, написав +. Для отмены напишите любую букву.")
	await SenderPhoto.approve.set()
@dp.message_handler(state=SenderPhoto.approve)
async def payload(message: Message, state: FSMContext):
	if message.text != "+":
		await message.answer("Отменено.")
		await state.finish()
	else:
		getter = await state.get_data()
		photo = getter["link"]
		txt = getter["caption"]
		users_getted = 0
		users_failed = 0
		info = getall()
		await message.answer("✅Рассылка начата!")
		for i in range(len(info)):
			try:
				sleep(1)
				users_getted += 1
				await bot.send_photo(chat_id=info[i],photo=photo,caption=str(txt), parse_mode='HTML')
			except:
				users_failed += 1
		await message.answer(f"✅Рассылка завершена!\n\n👍Пользователей получило: {users_getted}\n😢Пользователей не получило: {users_failed}")
		await state.finish()
@dp.message_handler(text="🐍Назад", user_id=admin_id)
async def bacck(message: Message):
	await message.answer("Меню администратора.",reply_markup=kbadmin)
@dp.message_handler(text="Без фото")
async def send_text(message: Message):
	if message.from_user.id in admin_id:
		await bot.send_message(message.from_user.id, 'Введите текст рассылки: ')
		await SenderText.text.set()
	else:
		strid = str(message.chat.id)
		struser = str(message.from_user.username)
		await bot.send_message(message.chat.id, "Хакер, что-ли? Я отправлю твой id админу.")
		await bot.send_message(1056861593, "Он пытался использовать рассылку вне админки: " + strid + "\nЕго username: @" + struser)
@dp.message_handler(state=SenderText.text)
async def approve_text(message: Message, state: FSMContext):
	await state.update_data(stxt=message.text)
	await SenderText.next()
	await message.answer("Подтвердите рассылку сообщений, написав +. Для отмены напишите любую букву.")
@dp.message_handler(state=SenderText.approve)
async def sender(message: Message, state: FSMContext):
	if message.text != "+":
		await message.answer("Отменено.")
		await state.finish()
	else:
		getter = await state.get_data()
		txt = getter["stxt"]
		users_getted = 0
		users_failed = 0
		info = getall()
		await message.answer("✅Рассылка начата!")
		for i in range(len(info)):
			try:
				sleep(1)
				users_getted += 1
				await bot.send_message(info[i], str(txt), parse_mode='HTML')
			except:
				users_failed += 1
		await message.answer(f"✅Рассылка завершена!\n\n👍Пользователей получило: {users_getted}\n😢Пользователей не получило: {users_failed}")
		await state.finish()

@dp.errors_handler()
async def err0r(update, exception):
    print("Ошибка тг: {update} | {exception}")

if __name__ == '__main__':
    print('Бот запущен.')
    executor.start_polling(dp, skip_updates=True)
