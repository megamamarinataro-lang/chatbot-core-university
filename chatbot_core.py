# chatbot_core.py
# Консольная имитация ядра серверной логики чат-бота

# === 1. Константы (Business Logic + Response Builder) ===
GREETING_RESPONSE = "Здравствуйте! Я — учебный помощник. Спросите меня о расписании."
SCHEDULE_PROMPT = "Для получения расписания укажите номер группы (101, 102 или 103)."
UNKNOWN_RESPONSE = "Извините, я вас не понял. Напишите 'расписание' или 'привет'."

SCHEDULES = {
    "101": "Расписание для группы 101: понедельник/среда 10:00–13:00.",
    "102": "Расписание для группы 102: вторник/четверг 11:00–14:00.",
    "103": "Расписание для группы 103: пятница 10:00–15:00.",
}

GREETING_WORDS = ["привет", "здравствуй", "hello"]


# === 2. Business Logic + Handler (чистая функция) ===
def get_bot_response(user_message: str, current_state):
    """
    Обрабатывает сообщение пользователя и возвращает ответ бота и новое состояние.
    Это объединение Handler, Business Logic и Response Builder для упрощения.
    """
    # Приводим к нижнему регистру и убираем лишние пробелы для надежности сравнения
    message = user_message.lower().strip()
    
    # Пункт 1: Проверка на команду выхода
    if message == "выход":
        return "До свидания!", None
        
    # Пункт 4: Ожидание группы (Проверяем в первую очередь, если бот ждет номер)
    if current_state == "awaiting_group":
        if message in SCHEDULES:
            return SCHEDULES[message], None  # Группа найдена, сбрасываем состояние
        else:
            return "Группа не найдена. Укажите 101, 102 или 103.", "awaiting_group"  # Ждем правильный ввод
            
    # Пункт 2: Приветствие
    if message in GREETING_WORDS:
        return GREETING_RESPONSE, None
        
    # Пункт 3: Запрос расписания
    if "расписание" in message:
        return SCHEDULE_PROMPT, "awaiting_group"
        
    # Пункт 5: Неизвестная команда
    return UNKNOWN_RESPONSE, current_state


# === 3. Основная программа (API Gateway + Dialog Manager) ===
def main():
    user_states = {}  # Dialog Manager: хранение состояний каждого пользователя
    
    print("=== Чат-бот учебной организации (консольная имитация) ===")
    print("Для выхода введите 'выход' в поле имени пользователя или в сообщении\n")
    
    while True:
        user_name = input("Введите имя пользователя: ").strip()
        if user_name.lower() == "выход" or not user_name:
            print("Программа завершена.")
            break
        
        user_message = input("Введите сообщение: ").strip()
        
        # Получаем текущее состояние пользователя (None по умолчанию)
        current_state = user_states.get(user_name)
        
        # Вызываем бизнес-логику (Business Logic)
        bot_answer, new_state = get_bot_response(user_message, current_state)
        
        # Сохраняем или сбрасываем новое состояние (Dialog Manager)
        if new_state is None:
            if user_name in user_states:
                del user_states[user_name]
        else:
            user_states[user_name] = new_state
        
        # Выводим ответ на экран (Response Builder)
        print(f"Бот: {bot_answer}\n")
        
        # Если пользователь написал выход внутри сообщения, тоже закрываем программу
        if bot_answer == "До свидания!":
            print("Программа завершена.")
            break


if __name__ == "__main__":
    main()
