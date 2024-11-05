#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int size;
    do
    {
        size = get_int("Height: ");
    }
    while (size < 1 || size > 8);
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size + 3 + i; j++)
        {
            if (j < size - i - 1 || j == size || j == size + 1 || j > size + i + 2)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
