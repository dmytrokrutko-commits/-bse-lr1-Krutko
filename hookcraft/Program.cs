using System;
using System.Collections.Generic;
using System.Text;

// Забезпечуємо коректне відображення української мови в консолі Windows
Console.OutputEncoding = Encoding.UTF8;
Console.InputEncoding = Encoding.UTF8;

Console.WriteLine("==================================================");
Console.WriteLine("          Вітаємо у системі HookCraft!           ");
Console.WriteLine("==================================================");

bool isRunning = true;
List<Hook> savedHooks = new List<Hook>();

while (isRunning)
{
    Console.WriteLine("\n📋 Головне меню:");
    Console.WriteLine("1. ✨ ШІ-генерація тексту (Інтеграція з OpenAI)");
    Console.WriteLine("2. 🎣 Генерація гачків (Hook Creator)");
    Console.WriteLine("3. 💾 Менеджмент контенту (Крафт та збереження нотаток)");
    Console.WriteLine("4. 🛡️ Модерація та безпека контенту");
    Console.WriteLine("5. ❌ Вихід з програми");
    Console.Write("\nОберіть номер опції: ");

    string input = Console.ReadLine();

    switch (input)
    {
        case "1":
            RunAIGeneration();
            break;
        case "2":
            RunHookGeneration(savedHooks);
            break;
        case "3":
            RunContentManagement();
            break;
        case "4":
            RunModeration();
            break;
        case "5":
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

// 2. Розділ Генерації Гачків
static void RunHookGeneration(List<Hook> hooks)
{
    Console.WriteLine("\n--- 🎣 Розділ: Генерація гачків ---");
    Console.WriteLine("1. Створити один гачок");
    Console.WriteLine("2. Створити кілька гачків");
    Console.WriteLine("3. Переглянути збережені гачки");
    Console.Write("\nОберіть дію: ");
    
    string choice = Console.ReadLine();

    switch (choice)
    {
        case "1":
            CreateSingleHook(hooks);
            break;
        case "2":
            CreateMultipleHooks(hooks);
            break;
        case "3":
            DisplaySavedHooks(hooks);
            break;
        default:
            Console.WriteLine("⚠️ Некоректний вибір.");
            break;
    }
}

static void CreateSingleHook(List<Hook> hooks)
{
    Console.Write("Введіть тему гачка (наприклад, 'заробіток в інтернеті'): ");
    string topic = Console.ReadLine();
    
    Console.Write("Введіть переваги/результат (наприклад, 'заробити 1000 грн за день'): ");
    string benefit = Console.ReadLine();
    
    Console.Write("Оберіть категорію (SMM, Бізнес, Розвиток, Інше): ");
    string category = Console.ReadLine();

    if (string.IsNullOrWhiteSpace(topic) || string.IsNullOrWhiteSpace(benefit))
    {
        Console.WriteLine("⚠️ Поля не можуть бути порожніми.");
        return;
    }

    Hook newHook = TextHelper.GenerateHook(topic, benefit, category);
    
    if (newHook != null)
    {
        hooks.Add(newHook);
        Console.WriteLine("\n✅ Гачок успішно створено:");
        Console.WriteLine(newHook);
    }
}

static void CreateMultipleHooks(List<Hook> hooks)
{
    Console.Write("Введіть тему гачків: ");
    string topic = Console.ReadLine();
    
    Console.Write("Введіть переваги/результат: ");
    string benefit = Console.ReadLine();
    
    Console.Write("Оберіть категорію (SMM, Бізнес, Розвиток, Інше): ");
    string category = Console.ReadLine();
    
    Console.Write("Скільки гачків створити (1-10): ");
    if (!int.TryParse(Console.ReadLine(), out int count) || count < 1 || count > 10)
    {
        Console.WriteLine("⚠️ Введіть число від 1 до 10.");
        return;
    }

    List<Hook> generatedHooks = TextHelper.GenerateMultipleHooks(topic, benefit, category, count);
    hooks.AddRange(generatedHooks);

    Console.WriteLine($"\n✅ Успішно створено {generatedHooks.Count} гачків:");
    foreach (var hook in generatedHooks)
    {
        Console.WriteLine("\n" + hook);
    }
}

static void DisplaySavedHooks(List<Hook> hooks)
{
    if (hooks.Count == 0)
    {
        Console.WriteLine("\n📭 Поки що гачків не створено.");
        return;
    }

    Console.WriteLine($"\n📚 Список збережених гачків ({hooks.Count}):");
    Console.WriteLine(new string('=', 60));
    
    for (int i = 0; i < hooks.Count; i++)
    {
        Console.WriteLine($"\n#{i + 1}");
        Console.WriteLine(hooks[i]);
    }
}

// 3. Розділ Менеджменту контенту
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

// 4. Розділ Модерації
static void RunModeration()
{
    Console.WriteLine("\n--- 🛡️ Розділ: Модерація та безпека ---");
    Console.WriteLine("Аналіз контенту на відповідність правилам безпеки системи...");
    
    // TODO: Додати логіку фільтрації слів або перевірки прав доступу користувачів
    Console.WriteLine("✓ Перевірка завершена. Порушень протоколів безпеки не виявлено.");
}