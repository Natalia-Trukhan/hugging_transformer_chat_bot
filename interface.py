from core import Bot


def show():
    # Try to initialize the bot and catch any startup errors
    try:
        bot = Bot()
    except Exception as e:
        print(f"\n[КРИТИЧНА ПОМИЛКА]: Не вдалося ініціалізувати бота.")
        print(f"Тип помилки: {type(e).__name__}")
        print(f"Повідомлення: {e}")
        return

    # Print welcome banner and instructions
    print("=" * 60)
    print("🤖 Вітаю! Ваш локальний Python-асистент на базі Qwen готовий до роботи.")
    print("Інструкції:")
    print(" - Просто пишіть своє запитання українською мовою.")
    print(" - Для виходу з програми введіть команду: 'вихід' або 'exit'.")
    print("=" * 60)

    # Main interactive console loop
    while True:
        try:
            # Read user input from the console
            text_user = input("\nВи: ").strip()

            # Handle user commands or input using match/case routing
            match text_user.lower():
                case "вихід" | "exit":
                    print("\n🤖 До побачення! Гарного дня та чистого коду!")
                    break
                case "":
                    print("Будь ласка, введіть запитання або команду для виходу.")
                    continue
                case _:
                    print("🤖 Бот думає...", end='', flush=True)
                    # Try generating a response and catch potential runtime errors
                    try:
                        response_bot = bot.generate_response(text_user)
                        print("\r" + " " * 30 + "\r", end="")
                        print(f"\nБот: {response_bot}")
                    except Exception as e:
                        print("\r" + " " * 30 + "\r", end="")
                        print(f"\n[ПОМИЛКА ГЕНЕРАЦІЇ]: Не вдалося створити відповідь.")
                        print(f"Тип помилки: {type(e).__name__}")
                        print(f"Повідомлення: {e}")
        except (KeyboardInterrupt, EOFError):
            # Handle graceful exit
            print("\n\n🤖 Роботу програми примусово завершено. Па-па!")
            break


if __name__ == "__main__":
    show()
