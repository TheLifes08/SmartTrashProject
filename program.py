# Бибилотеки
import MFRC522
import RPi.GPIO as GPIO
import time
import vk_api
import pymysql
import requests


ERROR_COMMAND = "Команда не найдена."
HELP = "Список доступных команд для стандартного пользователя:\n- Реле (включить\выключить))\n- Помощь" \
       "\nДля получения справки по конкретной команде, введите первое слово команды. Например, 'Реле'."
ADMIN_HELP = "Список доступных команд для администратора:\n- Реле (включить\выключить)\n" \
             "- Блокировка (включить\выключить)\n- Помощь\nДля получения справки по конкретной команде, введите " \
             "первое слово команды. Например, 'Реле'."
UNKNOWN_COMMAND = "Неизвестная команда. Введите \'Помощь\' для получения списка команд."
UNKNOWN_OBJECT = "Неизвестный объект: "
COMMAND_EXECUTE = "Запрос на выполнение команды: "
DONT_HAVE_PERMISSIONS = "У вас нет прав на использование этой команды. Для получения прав вы можете обратиться к " \
                        "администратору."
RELAY_ALREADY_TURN_ON = "Реле уже включено."
RELAY_ALREADY_TURN_OFF = "Реле уже выключено."
RELAY_BLOCKED = "Реле заблокировано администратором."
RELAY_TURN_ON = "Реле успешно включено."
RELAY_TURN_OFF = "Реле успешно выключено."
RELAY_TURN_ON_SECONDS = ["Реле включено на ", " секунд(ы)."]
RELAY_BLOCK = "Реле успешно заблокировано."
RELAY_UNBLOCK = "Реле успешно разлокировано."
RELAY_HELP = ["Пример команды: ", " [Включить\Выключить\Заблокировать\Разблокировать]"]
LOG_MESSAGE = ["Пользователь ", " выполнил команду: "]
BIN_OCCUPANCY = "Заполненность мусорки: "
USS_DISTANCE = "Дистанция до препятствия: "

print("Инициализация устройства...")

# Классы
class RubbishBin:
    def __init__(self, bin_id, objects, admins, height=4, log_user=39140456):
        self.setup_gpio()
        self.objects = objects
        self.admins = admins
        self.log_user = log_user
        self.height = height
        self.bin_id = bin_id


    @staticmethod
    def setup_gpio():
        print("Настройка GPIO...")
        
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

    def send_bin_data(self, occup):
        print(occup)
        r = requests.post("http://trashbinptz.000webhostapp.com/php/update_data.php", data={'access_id': '...', 'bin_id': self.bin_id, 'mode': 'update', 'occupancy': occup })
        return r

    def create_bin_data(self, lat, lon, occup):
        r = requests.post("http://trashbinptz.000webhostapp.com/php/update_data.php", data={'access_id': '...', 'bin_id': self.bin_id, 'mode': 'create', 'occupancy': occup, 'lat': lat, 'lon': lon })
        return r

    def check_messages(self):
        print("Проверка сообщений ВК...")
        
        conversations = self.objects['bot'].api.messages.getConversations(filter='unread')
        
        print("Непрочитанных диалогов: " + str(conversations['count']))
        
        if conversations['count'] > 0:
            for conversation in conversations["items"]:
                self.execute_commands(conversation['last_message']['text'], conversation['conversation']['peer']['id'])


    def execute_commands(self, command, user_id):
        commands = command.lower().split(' ')

        if len(commands) == 1:
            if self.bin_id == 1:
                self.objects['bot'].api.messages.send(user_id=user_id, random_id=0, message='[BIN ID=' + str(BIN_ID) + '] В начале команды требуется написать id мусорного контейнера! Пример: id1 bin occupancy')
                return

        if commands[0] != ('id' + str(BIN_ID)):
            return
        
        self.objects['bot'].api.messages.send(user_id=user_id, random_id=0, message=('[BIN ID=' + str(BIN_ID) + '] ' + COMMAND_EXECUTE + command))
        
        print('[' + str(user_id) + ']: ' + command)

        if user_id != self.log_user:
            self.log(user_id, command)
            
        if commands[1] == 'bin':
            answer = self.execute_command({'commands': commands, 'user_id': user_id})
        elif commands[1] in self.objects:
            answer = self.objects[commands[1]].execute_command({'commands': commands, 'user_id': user_id})
        else:
            answer = UNKNOWN_OBJECT + command.split(' ')[1]
            
        print(answer + '\n')

        self.objects['bot'].api.messages.send(user_id=user_id, random_id=0, message=answer)


    def is_admin(self, user_id):
        return user_id in self.admins


    def get_occupancy(self):
        distance = self.objects['uss'].get_distance()

        if distance > self.height:
            distance = self.height    
        
        return 100 - round(distance / self.height * 100)


    def is_occupancy_change(self, delta=5):
        middle = 0
        for i in range(0, 3):
            middle += self.get_occupancy()
            time.sleep(0.1)
        value = round(middle / 3)
        
        return abs(value - OCCUPANCY) >= delta, value


    def log(self, user_id, command):
        profile = self.objects['bot'].api.users.get(user_id=user_id)[0]
        message = LOG_MESSAGE[0] + profile['first_name'] + ' ' + profile['last_name'] + LOG_MESSAGE[1] + command
        self.objects['bot'].api.messages.send(user_id=self.log_user, random_id=0, message=message)


    def execute_command(self, data):
        commands = data['commands']
        
        if len(commands) == 2:
            answer = self.get_help()
        elif commands[2] == 'occupancy':
            answer = BIN_OCCUPANCY + str(self.get_occupancy()) + '%'
        elif commands[2] == 'create':
            self.objects['bot'].api.messages.send(user_id=data['user_id'], random_id=0, message="Введите Lat мусорного контейнера.")

            lat = ""
            conversations = self.objects['bot'].api.messages.getConversations(filter='unread')
            while conversations['count'] == 0:
                conversations = self.objects['bot'].api.messages.getConversations(filter='unread')
            print(conversations)
            lat = conversations['items'][0]['last_message']['text']
            self.objects['bot'].api.messages.send(user_id=data['user_id'], random_id=0, message="Введите Lon мусорного контейнера.")
            lon = ""
            conversations = self.objects['bot'].api.messages.getConversations(filter='unread')
            while conversations['count'] == 0:
                conversations = self.objects['bot'].api.messages.getConversations(filter='unread')
            lon = conversations['items'][0]['last_message']['text']
            self.objects['bot'].api.messages.send(user_id=data['user_id'], random_id=0, message="Создание...")
            answer = self.create_bin_data(lat, lon, OCCUPANCY).text
            self.objects['bot'].api.messages.send(user_id=data['user_id'], random_id=0, message="Лог: " + logs)
        else:
            answer = ERROR_COMMAND

        return answer


    def get_help(self):
        return 'ПОМОЩЬ ПОКА НЕ ДОСТУПНА'


class UltrasonicSensor:
    
    def __init__(self, trigger_pin=16, echo_pin=18, temperature=26):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.sound_speed = 33100 + (0.6 * temperature)
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trigger_pin, False)
        time.sleep(0.5)


    def get_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start = time.time()
        stop = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop = time.time()

        elapsed = stop - start

        return elapsed * self.sound_speed / 2

    def get_help(self):
        return 'ПОМОЩЬ ПОКА НЕ ДОСТУПНА'


    def execute_command(self, data):
        commands = data['commands']
        
        if len(commands) == 2:
            answer = self.get_help()
        elif commands[2] == 'distance':
            answer = USS_DISTANCE + str(self.get_distance()) + ' см'
        else:
            answer = ERROR_COMMAND

        return answer


class VkBot:
    def __init__(self, token):
        self.token = token
        self.api = vk_api.VkApi(token=token).get_api()


    def get_help(self):
        return 'ПОМОЩЬ ПОКА НЕ ДОСТУПНА'


    def execute_command(self, data):
        commands = data['commands']
        
        if len(commands) == 2:
            answer = self.get_help()
        else:
            answer = ERROR_COMMAND

        return answer


class Database:
    def __init__(self, host, user, password, db_name, charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.charset = charset
        self.database = pymysql.connect(host=host, user=user, password=password, db=db_name, charset=charset,
                                        cursorclass=pymysql.cursors.DictCursor, autocommit=True)


    def sql_request(self, request):
        return self.database.cursor().execute(request)


    def get_help(self):
        return 'ПОМОЩЬ ПОКА НЕ ДОСТУПНА'


    def execute_command(self, data):
        commands = data['commands']
        
        if len(commands) == 2:
            answer = self.get_help()
        else:
            answer = ERROR_COMMAND

        return answer


class Relay:
    def __init__(self, pin, status=0):
        self.pin = pin
        self.status = status

        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


    def execute_command(self, data):
        commands = data['commands']
        if len(commands) == 1:
            answer = self.get_help()
        elif commands[1] == 'turnon':
            if self.status == 1:
                answer = RELAY_ALREADY_TURN_ON
            elif self.status == 2:
                answer = RELAY_BLOCKED
            else:
                if len(commands) == 2:
                    answer = RELAY_TURN_ON
                    self.turn_on(0)
                else:
                    answer = RELAY_TURN_ON_SECONDS[0] + commands[2] + RELAY_TURN_ON_SECONDS[1]
                    self.turn_on(int(commands[2]))
        elif commands[1] == 'turnoff':
            if self.status == 0:
                answer = RELAY_ALREADY_TURN_OFF
            elif self.status == 2:
                answer = RELAY_BLOCKED
            else:
                answer = RELAY_TURN_OFF
                self.turn_off()
        elif commands[1] == 'block':
            answer = self.change_block(True, data['user_id'])
        elif commands[1] == 'unblock':
            answer = self.change_block(False, data['user_id'])
        else:
            answer = ERROR_COMMAND

        return answer


    def turn_on(self, seconds):
        self.change_status(1)

        if seconds == 0:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(seconds)
            self.turn_off()


    def turn_off(self):
        self.change_status(0)
        GPIO.output(self.pin, GPIO.LOW)


    def change_status(self, new_status):
        self.status = new_status


    def change_block(self, is_block, user_id):
        if BIN.is_admin(user_id):
            if is_block:
                if self.status == 1:
                    self.turn_off()
                self.change_status(2)
                answer = RELAY_BLOCK
            else:
                self.change_status(0)
                answer = RELAY_UNBLOCK
        else:
            answer = DONT_HAVE_PERMISSIONS

        return answer

    def get_help(self):
        return RELAY_HELP[0] + self.name + RELAY_HELP[1]


class RFID:
    def __init__(self):
        self.reader = MFRC522.Reader(0, 0, 22)

    def detect_card(self):
        self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        (status, uid) = self.reader.MFRC522_Anticoll()

        if status == self.reader.MI_OK:
            uid_str = str(uid[0]) + ',' + str(uid[1]) + ',' + str(uid[2]) + ',' + str(uid[3]) + ',' + str(uid[4])
            cursor = BIN.objects['db'].sql_request("SELECT * FROM users WHERE card='" + uid_str + "'")

            for item in cursor:
                list_commands = dict(item)['commands'].split(' ')
                BIN.objects[list_commands[0]].execute_command({'commands': list_commands, "user_id": -1})
                
    def get_help(self):
        return 'ПОМОЩЬ ПОКА НЕ ДОСТУПНА'

    def execute_command(self, data):
        commands = data['commands']
        
        if len(commands) == 2:
            answer = self.get_help()
        else:
            answer = ERROR_COMMAND

        return answer


class Help:
    @staticmethod
    def execute_command(data):
        commands = data['commands']
        if len(commands) == 2:
            if BIN.is_admin(data['user_id']):
                return ADMIN_HELP
            else:
                return HELP
        else:
            return BIN.objects[commands[1]].get_help()


IS_RUN = True
BIN_ID = int(open('id', 'r').read())
ofile =  open('occupancy', 'r+')
OCCUPANCY = int(ofile.read())
BIN = RubbishBin(BIN_ID, {}, admins=[39140456], height=57)
BIN.objects = {
    'help': Help(),
    'bot': VkBot('...'),
    'uss': UltrasonicSensor(16, 18)#,
    #'relay': Relay(12),
    #'rfid': RFID() #BIN.objects['rfid'].detect_card()
}

print("Настройка завершена!\n")

while IS_RUN:
    try:
        BIN.check_messages()
        (is_change, value) = BIN.is_occupancy_change()
        print("Значение ультразвукового дальномера: " + str(BIN.objects['uss'].get_distance()) + " (" + str(value) + "%)\n")
        if is_change:
            OCCUPANCY = value
            print("Обновление данных о мусорке. Ответ от сервера: " + BIN.send_bin_data(OCCUPANCY).text)
            ofile.write(value)
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print('Broken')
        GPIO.cleanup()
