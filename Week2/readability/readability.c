#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
int count_letters(string phrase);
int count_words(string phrase);
int count_sentences(string phrase);
int main(void)
{
    string phrase = get_string("Text: ");
    int l = count_letters(phrase);
    int w = count_words(phrase);
    int s = count_sentences(phrase);
    double L = l * 100 / (double) w;
    double S = s * 100 / (double) w;
    double i = 0.0588 * L - 0.296 * S - 15.8;
    if (i < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (i > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(i));
    }
}

int count_words(string phrase)
{
    int l = strlen(phrase);
    int words = 1;
    for (int i = 0; i < l; i++)
    {
        if (phrase[i] == 32)
        {
            words++;
        }
    }
    printf("words: %d\n", words);
    return words;
}

int count_letters(string phrase)
{
    int l = strlen(phrase);
    int letters = 0;
    for (int i = 0; i < l; i++)
    {
        if ((phrase[i] < 91 && phrase[i] > 64) || (phrase[i] < 123 && phrase[i] > 96))
        {
            letters++;
        }
    }
    printf("letters: %d\n", letters);
    return letters;
}

int count_sentences(string phrase)
{
    int l = strlen(phrase);
    int punctuation = 0;
    for (int i = 0; i < l; i++)
    {
        if (phrase[i] == 33 || phrase[i] == 46 || phrase[i] == 63)
        {
            punctuation++;
        }
    }
    printf("sentences: %d\n", punctuation);
    return punctuation;
}
