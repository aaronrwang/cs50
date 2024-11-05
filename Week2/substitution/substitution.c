#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    bool mapped[26];
    string key;
    key = argv[1];
    for (int i = 0; i < 26; i++)
    {
        mapped[i] = false;
        key[i] = (key[i] > 96) ? key[i] - 32 : key[i];
    }
    for (int i = 0; i < 26; i++)
    {
        mapped[key[i] - 65] = true;
    }
    bool cont = true;
    for (int i = 0; i < 26; i++)
    {
        cont = (mapped[i]) ? cont : false;
    }
    if (!cont)
    {
        printf("Invalid key\n");
        return 1;
    }
    string text = get_string("plaintext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        int c = text[i];
        if (c < 91 && c > 64)
        {
            int s = c - 65;
            text[i] = key[s];
        }
        else if (c < 123 && c > 96)
        {
            int s = c - 97;
            text[i] = key[s] + 32;
        }
    }
    printf("ciphertext: %s\n", text);
}
