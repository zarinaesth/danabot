pip install python-telegram-bot==20.0

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Stages for the quiz
QUIZ, ANSWER = range(2)

# Sample quiz questions
quiz_questions = [
    {
        "question": "Что делают казахи, когда кто-то впервые заходит в новый дом? / Қазақтар жаңа үйге алғаш рет кірген кезде не істейді?",
        "answer": "Жиын"
    },
    {
        "question": "Как называется древний казахский музыкальный инструмент? / Ежелгі қазақ музыкалық аспабы қалай аталады?",
        "answer": "Домбра"
    },
    {
        "question": "У меня нет тела, но я могу убить. У меня нет голоса, но я могу напугать. Что я? / Менің денем жоқ, бірақ мен өлтіре аламын. Менің дауысым жоқ, бірақ мен қорқыта аламын. Мен не?",
        "answer": "Тишина / Тыныштық"
    }
]

# Bot start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Меня зовут Дана. Я могу рассказать тебе о древних традициях аула или провести для тебя тест. Напиши 'хочу пройти тест', чтобы начать!"
    )

# Respond to a quiz request
def start_quiz(update: Update, context: CallbackContext):
    context.user_data['quiz_index'] = 0  # Start with the first question
    context.user_data['score'] = 0
    question = quiz_questions[context.user_data['quiz_index']]['question']
    update.message.reply_text(
        f"Давай начнем! Вот первый вопрос:\n\n{question}"
    )
    return QUIZ

# Handle quiz answers
def handle_answer(update: Update, context: CallbackContext):
    user_answer = update.message.text
    quiz_index = context.user_data.get('quiz_index', 0)
    correct_answer = quiz_questions[quiz_index]['answer']

    if user_answer.strip().lower() == correct_answer.strip().lower():
        context.user_data['score'] += 1
        update.message.reply_text("Правильно! Молодец!")
    else:
        update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")

    context.user_data['quiz_index'] += 1

    # Check if there are more questions
    if context.user_data['quiz_index'] < len(quiz_questions):
        next_question = quiz_questions[context.user_data['quiz_index']]['question']
        update.message.reply_text(f"Следующий вопрос:\n\n{next_question}")
        return QUIZ
    else:
        # Quiz is over
        score = context.user_data['score']
        update.message.reply_text(f"Тест окончен! Ты набрал {score} из {len(quiz_questions)}.")
        if score == len(quiz_questions):
            update.message.reply_text("Поздравляю! Вот твой промокод на скидку: DANA-10!")
        else:
            update.message.reply_text("Попробуй ещё раз, чтобы получить лучший результат.")
        return ConversationHandler.END

# Handle fallback for quitting or errors
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("До встречи! Если захочешь попробовать снова, просто напиши 'хочу пройти тест'.")
    return ConversationHandler.END

# Main function to set up the bot
def main():
    # Initialize the bot
    updater = Updater("7508544660:AAEC51be8U7YTG1HBfwn0MrryfT4L_iZrU8")
    dispatcher = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("хочу пройти тест"), start_quiz)],
        states={
            QUIZ: [MessageHandler(Filters.text & ~Filters.command, handle_answer)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
