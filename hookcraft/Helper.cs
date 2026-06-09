using System;
using System.Collections.Generic;

public class Hook
{
    public string Title { get; set; }
    public string Description { get; set; }
    public string Category { get; set; }
    public int VowelCount { get; set; }
    public DateTime CreatedAt { get; set; }

    public Hook(string title, string description, string category)
    {
        Title = title;
        Description = description;
        Category = category;
        VowelCount = TextHelper.CountVowels(title + " " + description);
        CreatedAt = DateTime.Now;
    }

    public override string ToString()
    {
        return $"📌 [{Category}] {Title}\n   {Description}\n   🔤 Голосних: {VowelCount} | 📅 {CreatedAt:dd.MM.yyyy HH:mm}";
    }
}

public static class TextHelper
{
    private static readonly HashSet<char> Vowels = new HashSet<char>
    {
        'а', 'е', 'є', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я',
        'А', 'Е', 'Є', 'И', 'І', 'Ї', 'О', 'У', 'Ю', 'Я',
        'a', 'e', 'i', 'o', 'u', 'y',
        'A', 'E', 'I', 'O', 'U', 'Y'
    };

    private static readonly string[] HookPatterns = new[]
    {
        "🚀 {0} - це змінить ваш {1}",
        "⚡ {0} який вас {1}",
        "🔥 {0} за {1}",
        "💡 {0} це не просто {1}",
        "😱 {0} - ви не повірите {1}",
        "✨ {0} - це магія {1}",
        "🎯 {0} - ваш ключ до {1}"
    };

    public static int CountVowels(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return 0;
        }

        int count = 0;
        foreach (char ch in input)
        {
            if (Vowels.Contains(ch))
            {
                count++;
            }
        }

        return count;
    }

    public static Hook GenerateHook(string topic, string benefit, string category)
    {
        if (string.IsNullOrWhiteSpace(topic) || string.IsNullOrWhiteSpace(benefit))
        {
            return null;
        }

        Random random = new Random();
        string pattern = HookPatterns[random.Next(HookPatterns.Length)];
        string title = string.Format(pattern, topic, benefit);

        return new Hook(title, $"Дізнайтеся більше про {topic}", category);
    }

    public static List<Hook> GenerateMultipleHooks(string topic, string benefit, string category, int count)
    {
        List<Hook> hooks = new List<Hook>();
        
        for (int i = 0; i < count; i++)
        {
            var hook = GenerateHook(topic, benefit, category);
            if (hook != null)
            {
                hooks.Add(hook);
            }
        }

        return hooks;
    }
}

