from core import Bot


def show():
    # Try to initialize the bot and catch any startup errors
    try:
        print()
        print("=" * 60)
        print("СТВОРЕННЯ БОТА ДЛЯ ДОПОМОГИ В ПРОГРАМУВАННІ")
        print("=" * 60)
        print()
        while True:
            print("=" * 60)
            print("Виберіть одну з представлених моделей для ініціалізації бота:")
            print("""
- 1 ministral/Ministral-3b-instruct
- 2 Qwen/Qwen2.5-3B-Instruct
- 3 Qwen/Qwen2.5-Coder-1.5B-Instruct
- 4 HuggingFaceTB/SmolLM2-1.7B-Instruct
- 5 MaziyarPanahi/calme-3.3-baguette-3b
- 6 HuggingFaceTB/SmolLM3-3B
- 7 Qwen/Qwen3-1.7B
- 'вихід' або 'exit' для завершення 
            """)
            print("=" * 60)
            name_model = input("> ").strip()
            match name_model.lower():
                case '1':
                    name_model = "ministral/Ministral-3b-instruct"
                case '2':
                    name_model = "Qwen/Qwen2.5-3B-Instruct"
                case '3':
                    name_model = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
                case '4':
                    name_model = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
                case '5':
                    name_model = "MaziyarPanahi/calme-3.3-baguette-3b"
                case '6':
                    name_model = "HuggingFaceTB/SmolLM3-3B"
                case '7':
                    name_model = "Qwen/Qwen3-1.7B"
                case 'вихід' | 'exit':
                    print("\n🤖 До побачення! Гарного дня та чистого коду!")
                    break
                case _:
                    print("Виберіть лише цифри від 1 до 7 або 'вихід' або 'exit' для завершення!")
                    continue

            try:
                bot = Bot(name_model)
            except Exception as e:
                print(f"ПОМИЛКА ВАЛІДАЦІЇ: {e}")
                continue

            print()
            print("=" * 60)
            print(f"🤖 Вітаю! Ваш локальний Python-асистент на базі {name_model} моделі готовий до роботи.")
            print("Інструкції:")
            print(" - Просто пишіть своє запитання українською мовою.")
            print(" - Для повернення до меню де можна вибрати іншу модель введіть команду: 'назад' або 'back'.")
            print("=" * 60)

            # Main interactive console loop
            while True:
                try:
                    # Read user input from the console
                    text_user = input("\nВи: ").strip()

                    # Handle user commands or input using match/case routing
                    match text_user.lower():
                        case "назад" | "back":
                            print("\n🤖 Переходимо до вибора іншої моделі..")
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

    except Exception as e:
        print(f"\n[КРИТИЧНА ПОМИЛКА]: Не вдалося ініціалізувати бота.")
        print(f"Тип помилки: {type(e).__name__}")
        print(f"Повідомлення: {e}")
        return

    # Print welcome banner and instructions


if __name__ == "__main__":
    show()
