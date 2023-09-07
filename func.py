from ipdata import ipdata
from blockcypher import get_address_overview
from requests import get
from traceback import format_exc

apikey = 'c335d87f4e99ce6a747f8628bea61368f7274ff83b39d019c4ed0731'
ipdata = ipdata.IPData(apikey)

def ip_check(ip):
	try:
		try:
			data = ipdata.lookup(ip)
		except ValueError:
			return 'Неправильный IP.'
		strfat = str(data)
		#c.print(strfat)
		domain, name = data['asn']['domain'], data['asn']['name']
		callcode, city = data['calling_code'], data['city']
		carrier = data['carrier']['name']
		contcode, contname = data['continent_code'], data['continent_name']
		ccode, cname = data["country_code"], data["country_name"]
		curcode, cursymbol = data['currency']["code"], data['currency']["symbol"]
		emoflag = data['emoji_flag']
		ipret = data['ip']
		lang = data['languages'][0]['name']
		lat, lon = data['latitude'], data['longitude']
		postal = data['postal']
		region = data['region']
		istor, isproxy = data['threat']['is_tor'], data['threat']['is_proxy']
		timezone, curtime = data['time_zone']['name'], data['time_zone']['current_time']
		txt = f"""<b>==IP: {ipret}==</b>\n\nКонтинент: {contname} ({contcode})\nСтрана:  {emoflag}{cname} ({ccode})\nВалюта: {curcode} ({cursymbol})\nЯзык: {lang}\nРегион: {region}\nМеждународный код: {callcode}\nПочтовый код: {postal}\nПровайдер: {carrier} | {name} ({domain})\nГород: {city}\nКоординаты: lat: {lat} | lon: {lon}\nТекущее время: {curtime}\nЧасовой пояс: {timezone}\nИспользует TOR: {istor}\nИспользует proxy: {isproxy}"""
		return txt
	except KeyError as e:
		callcode, city = data['calling_code'], data['city']
		contcode, contname = data['continent_code'], data['continent_name']
		ccode, cname = data["country_code"], data["country_name"]
		curcode, cursymbol = data['currency']["code"], data['currency']["symbol"]
		emoflag = data['emoji_flag']
		ipret = data['ip']
		lang = data['languages'][0]['name']
		lat, lon = data['latitude'], data['longitude']
		postal = data['postal']
		region = data['region']
		istor, isproxy = data['threat']['is_tor'], data['threat']['is_proxy']
		timezone, curtime = data['time_zone']['name'], data['time_zone']['current_time']
		txt = f"""<b>==IP: {ipret}==</b>\n\n├Континент: <i>{contname} ({contcode})</i>\n├Страна:  <i>{emoflag}{cname} ({ccode})</i>\n├Валюта: <i>{curcode} ({cursymbol})</i>\n├Язык: <i>{lang}</i>\n├Регион: <i>{region}</i>\n├Международный код: <i>{callcode}</i>\n├Почтовый код: {postal}\n├Город: <i>{city}</i>\n├Координаты: <i>lat: {lat} | lon: {lon}</i>\n├Текущее время: <i>{curtime}</i>\n├Часовой пояс: <i>{timezone}</i>\n├Использует TOR: <i>{istor}</i>\n├Использует proxy:<i>{isproxy}</i>"""
		return txt

def btc_check(addr: str):
    try:
        s = dict(get_address_overview(addr))
        txt = f'''<b>Информация по BTC адресу {addr}:</b>\n
├Общая сумма полученных средств: <i>{float(s['total_received'])/100000000}</i> BTC
├Общая сумма отправленных средств: <i>{float(s['total_sent'])/100000000}</i> BTC
├Итоговый баланс: <i>{float(s['total_received'])/100000000}</i> BTC
├Проведено транзакций: <i>{int(s['n_tx'])}</i>
├Изучить все транзакции: <a href="https://www.blockchain.com/btc/address/{addr}">клик</a>'''
        return txt
    except Exception as e:
        return "Неверный адрес."

def num_check(num: int):
    try:
        num = int(num)
        r = get(f'https://api.telnyx.com/anonymous/v2/number_lookup/{num}').json() 
        if r.get('errors'):
            return "Неверный формат номера.\nПример: 380678961593"
        else:
            return f"<b>Номер:</b> <i>{r['data']['phone_number']}</i>\n├Страна: <i>{r['data']['country_code']}</i>\n├Оператор: {r['data']['carrier']['name']}\n├Тип: <i>{r['data']['carrier']['type']}</i>"
    except Exception as e:
        print(e)
        return 'Неверный формат номера либо неверный номер.\n\nПример: 380678961593'


def bin_check(ccbin: int):
	if len(ccbin) < 6:
		return("BIN должен быть больше 6 цифр.")
	else:
		reply=get("https://lookup.binlist.net/{}".format(ccbin))
		if reply.status_code == 200:
			data=reply.json()
			text="""<i>Результат</i>:
	├Чисел: <b>{0}</b>
	├Тип: <b>{1}</b>
	├Брэнд: <b>{2}</b>
	├Уровень: <b>{3}</b>
	├Prepaid?: <b>{4}</b>
	├Страна: <b>{5}</b>
	├Банк: <b>{6}</b>
	├Валюта: <b>{7}</b>
	"""
#json variables#
			try:
				numbers=data["number"]["length"]
				scheme=data["scheme"]
				cctype=data["type"]
				brand=data["brand"]
				prepaid=data["prepaid"]
				country=data["country"]["name"]
				bank=data["bank"]["name"]
				currency=data["country"]["currency"]
			except Exception as e:
				scheme=data["scheme"]
				cctype=data["type"]
				brand=data["brand"]
				country=data["country"]["name"]
				currency=data["country"]["currency"]
				return f"""<i>Результат</i>:
	├Тип: <b>{scheme}</b>
	├Брэнд: <b>{brand}</b>
	├Уровень: <b>{cctype}</b>
	├Страна: <b>{country}</b>
	├Валюта: <b>{currency}</b>
	"""
#code
		try:
			return (text.format(numbers, scheme, cctype, brand, prepaid, country, bank, currency))
		except KeyError as e:
			return ("Неправильный BIN.")
		except UnboundLocalError as ee:
			return ("Введите правильный BIN.")


def mac_check(addr: str):
    try:
        s = get(f'https://www.macvendorlookup.com/api/v2/{addr}').json()
        s = s[0]
        return f'<b>MAC-адрес</b>: {addr}\n├Производитель: <i>{s["company"]}</i>\n├Адрес производителя: <i>{", ".join([s["addressL1"], s["addressL2"], s["addressL3"]])}</i>\n├Страна: <i>{s["country"]}</i>\n├Тип: <i>{s["type"]}</i>'
    except Exception as e:
        print(e)
        return 'Неверный MAC.'

def resolve_vk_id(nick: str):
    try:
        r = get(f'https://api.vk.com/method/utils.resolveScreenName?access_token=0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c&v=5.131&screen_name={nick}').json()
        return int(r['response']['object_id'])
    except Exception as e:
        return None

def raw_id_getter(raw_str: str):
    if 'id' in raw_str:
        return int(raw_str.split('/')[3].split('id')[1])
    else:
        return resolve_vk_id(str(raw_str.split('/')[3]))

def vk_check(link: str):
    try:
        idx = raw_id_getter(link)
        if idx == None:
            return 'https://okeygeek.ru/wp-content/uploads/2017/09/1885f2cadafc0e310a9c97a54e52070d.jpg', 'Неверно указана ссылка.'
        else:
            r = get(f'https://api.vk.com/method/users.get?access_token=0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c&v=5.131&user_ids={idx}&fields=first_name,last_name,status,sex,country,photo_max_orig').json()
            return r['response'][0]['photo_max_orig'], f"""<b>VK</b>: <i>{idx}</i>
├Имя: <i>{r['response'][0]['first_name']}</i>
├Фамилия: <i>{r['response'][0]['last_name']}</i>
├Статус: <i>{r['response'][0]['status']}</i>
├Страна: <i>{r['response'][0]['country']['title']}</i>
├Пол: <i>{"Мужской" if r['response'][0]['sex'] == 2 else 'Женский'}</i>"""
    except Exception as e:
        print(format_exc())
        return 'https://okeygeek.ru/wp-content/uploads/2017/09/1885f2cadafc0e310a9c97a54e52070d.jpg', f"Неверно указана ссылка либо на странице нету параметра {e}."

def username_check(username: str):
    try:
        s = []
        txt = '\n'
        WEBSITES = [
        "https://www.instagram.com/{}/media/",
        "http://pastebin.com/u/{}",
        "https://www.reddit.com/user/{}.json",
        "https://github.com/{}",
        'https://t.me/{}',
        'https://vk.com/{}']
        for website in WEBSITES:
            url = website.format(username)
            r = get(url, allow_redirects=False).status_code
            if r == 200:
                s.append(f"├Пользователь существует: {url}")
            else:
                s.append(f"├Пользователь не существует: {url}")
        return f'<b>Результаты: </b>\n<i>├Ник:</i> {username}\n{txt.join(s)}'
    except Exception:
        return 'Неверный ник.'
        print(format_exc())