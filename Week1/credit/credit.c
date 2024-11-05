#include <cs50.h>
#include <stdio.h>
int visa13(long num);
int visa16(long num);
int amex(long num);
int masterCard(long num);
int valid(long num);
int main(void)
{
    long num = get_long("Number: ");

    if (num < 5000000000000 && num >= 4000000000000)
    {
        visa13(num);
    }
    else if (num < 5000000000000000 && num >= 4000000000000000)
    {
        visa16(num);
    }
    else if (num < 350000000000000 && num >= 340000000000000)
    {
        amex(num);
    }
    else if (num < 380000000000000 && num >= 370000000000000)
    {
        amex(num);
    }
    else if (num < 5600000000000000 && num >= 5100000000000000)
    {
        masterCard(num);
    }
    else
    {
        printf("INVALID\n");
    }
}
int valid(long num)
{
    int count = 0;
    int ot[] = {0, 0, 0, 0, 0, 0, 0, 0};
    int et[] = {0, 0, 0, 0, 0, 0, 0, 0};
    while (num > 0)
    {
        if (count % 2 == 0)
        {
            et[count / 2] = num % 10;
        }
        else
        {
            ot[count / 2] = num % 10;
        }
        count++;
        num /= 10;
    }
    int total = 0;
    for (int i = 0; i < 8; i++)
    {
        printf("%i,", et[i]);
        printf("%i,", ot[i]);
    }
    for (int i = 0; i < 8; i++)
    {
        if (ot[i] >= 5)
        {
            total += 2 * ot[i];
            total -= 9;
        }
        else
        {
            total += 2 * ot[i];
        }
        total += et[i];
        printf("t: %i\n", total);
    }
    return (total % 10);
}
int amex(long num)
{
    if (valid(num) == 0)
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
int visa13(long num)
{
    if (valid(num) == 0)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
int visa16(long num)
{
    if (valid(num) == 0)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
int masterCard(long num)
{
    if (valid(num) == 0)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
