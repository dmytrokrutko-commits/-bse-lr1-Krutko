using System.Collections.Generic;

public static class TextHelper
{
    private static readonly HashSet<char> Vowels = new HashSet<char>
    {
        'а', 'е', 'є', 'и', 'і', 'ї', 'о', 'у', 'ю', 'я',
        'А', 'Е', 'Є', 'И', 'І', 'Ї', 'О', 'У', 'Ю', 'Я',
        'a', 'e', 'i', 'o', 'u', 'y',
        'A', 'E', 'I', 'O', 'U', 'Y'
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
}

