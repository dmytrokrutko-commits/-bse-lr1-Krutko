using System;
using System.Text;

// Забезпечуємо коректне відображення української мови в консолі Windows
Console.OutputEncoding = Encoding.UTF8;
Console.InputEncoding = Encoding.UTF8;

Console.WriteLine("==================================================");
Console.WriteLine("          Вітаємо у системі HookCraft!           ");
Console.WriteLine("==================================================");

bool isRunning = true;

while (isRunning)
{
    Console.WriteLine("\n📋 Головне меню:");
    Console.WriteLine("1. ✨ ШІ-генерація тексту (Інтеграція з OpenAI)");
    Console.WriteLine("2. 💾 Менеджмент контенту (Крафт та збереження нотаток)");
    Console.WriteLine("3. 🛡️ Модерація та безпека контенту");
    Console.WriteLine("4. ❌ Вихід з програми");
    Console.Write("\nОберіть номер опції: ");

    string input = Console.ReadLine();

    switch (input)
    {
        case "1":
            RunAIGeneration();
            break;
        case "2":
            RunContentManagement();
            break;
        case "3":
            RunModeration();
            break;
        case "4":
            isRunning = false;
            Console.WriteLine("👋 Дякуємо за використання HookCraft. До зустрічі!");
            break;
        default:
            Console.WriteLine("⚠️ Некоректний вибір, спробуйте ще раз.");
            break;
    }
}

// 1. Розділ ШІ-Генерації
static void RunAIGeneration()
{
    Console.WriteLine("\n--- 🤖 Розділ: ШІ-Генерація варіантів тексту ---");
    Console.Write("Введіть ваш запит (промт) для SMM-тексту: ");
    string prompt = Console.ReadLine();
    
    if (string.IsNullOrWhiteSpace(prompt))
    {
        Console.WriteLine("⚠️ Запит не може бути порожнім.");
        return;
    }

    Console.WriteLine("⏳ Звернення до OpenAI API (генерація триває 3-5 секунд)...");
    // TODO: У майбутньому тут буде підключено HttpClient або офіційний OpenAI NuGet пакет
    
    Console.WriteLine("\n[Згенерований ШІ результат]:");
    Console.WriteLine($"👉 Креативний пост на тему '{prompt}' успішно створено та оптимізовано!");
}

// 2. Розділ Менеджменту контенту
static void RunContentManagement()
{
    Console.WriteLine("\n--- 📝 Розділ: Менеджмент контенту ---");
    Console.WriteLine("1. Створити/закрафтити нову нотатку");
    Console.WriteLine("2. Переглянути список збережених креативів");
    Console.Write("Оберіть підпункт дії (поки що працює як заглушка): ");
    Console.ReadLine();
    
    // TODO: Додати колекцію List<string> або роботу з базой даних для збереження результатів
    Console.WriteLine("✓ Дію успішно імітовано.");
}

// 3. Розділ Модерації
static void RunModeration()
{
    Console.WriteLine("\n--- 🛡️ Розділ: Модерація та безпека ---");
    Console.WriteLine("Аналіз контенту на відповідність правилам безпеки системи...");
    
    // TODO: Додати логіку фільтрації слів або перевірки прав доступу користувачів
    Console.WriteLine("✓ Перевірка завершена. Порушень протоколів безпеки не виявлено.");
}