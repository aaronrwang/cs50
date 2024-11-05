#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // While there's still data left to read from the memory card
    FILE *img = NULL;
    int count = -1;
    while (fread(buffer, 1, 512, card) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            count++;
            char filename[8];
            sprintf(filename, "%03i.jpg", count);
            if (img != NULL)
            {
                fclose(img);
            }
            img = fopen(filename, "w");
            fwrite(buffer, 1, 512, img);
        }
        else if (count >= 0)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(card);
    fclose(img);
}
