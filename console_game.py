from db_scripts import *
import random

def play_quiz(quiz_id):
    """
    Функция для игры в квиз.
    Принимает quiz_id — ID выбранной викторины.
    """
    question_id = 0
    score = 0
    total_questions = 0

    while True:
        # Получаем следующий вопрос
        question_data = get_question_after(quiz_id, question_id)
        if not question_data:
            break  # Если больше нет вопросов, выходим из цикла

        # Распаковываем данные вопроса
        question_id, question, answer, wrong1, wrong2, wrong3 = question_data

        # Создаем список вариантов ответов и перемешиваем их
        options = [answer, wrong1, wrong2, wrong3]
        random.shuffle(options)

        # Выводим вопрос и варианты ответов
        print(f"\nВопрос: {question}")
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")

        # Получаем ответ пользователя
        while True:
            user_answer = input("Выберите правильный вариант (1-4): ")
            try:
                user_choice = int(user_answer) - 1
                if 0 <= user_choice < len(options):
                    selected_option = options[user_choice]
                    if selected_option == answer:
                        print("Правильно!")
                        score += 1
                    else:
                        print(f"Неправильно! Правильный ответ: {answer}")
                    total_questions += 1
                    break
                else:
                    print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")
            except ValueError:
                print("Неверный формат ввода. Пожалуйста, введите число от 1 до 4.")

    # Итоговый результат
    print(f"\nИгра завершена! Ваш результат: {score}/{total_questions}")

def list_quizzes():
    """
    Выводит список доступных викторин.
    """
    db_name = 'quiz.sqlite'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM quiz")
    quizzes = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\nДоступные викторины:")
    for quiz in quizzes:
        print(f"{quiz[0]}. {quiz[1]}")

def main():
    """
    Основная функция для запуска игры.
    """
    print("Добро пожаловать в игру 'Квиз'!")

    # Вывод списка викторин
    list_quizzes()

    # Выбор викторины пользователем
    try:
        quiz_id = int(input("Введите номер викторины, чтобы начать игру: "))
        play_quiz(quiz_id)
    except ValueError:
        print("Неверный формат ввода. Пожалуйста, введите число.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()