#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            average /= 3;
            image[i][j].rgbtBlue = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtRed = round(average);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float T[] = {0, 0, 0, 0};
            int crse[2][2];
            crse[0][0] = -1;
            crse[1][0] = -1;
            crse[0][1] = 1;
            crse[1][1] = 1;
            if (i == 0)
                crse[0][0] = 0;
            if (j == 0)
                crse[1][0] = 0;
            if (i == height - 1)
                crse[0][1] = 0;
            if (j == width - 1)
                crse[1][1] = 0;
            for (int r = crse[0][0]; r <= crse[0][1]; r++)
            {
                for (int c = crse[1][0]; c <= crse[1][1]; c++)
                {
                    T[0] += image[i + r][j + c].rgbtRed;
                    T[1] += image[i + r][j + c].rgbtBlue;
                    T[2] += image[i + r][j + c].rgbtGreen;
                    T[3]++;
                }
            }
            temp[i][j].rgbtRed = round(T[0] / T[3]);
            temp[i][j].rgbtBlue = round(T[1] / T[3]);
            temp[i][j].rgbtGreen = round(T[2] / T[3]);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //{R,G,B}*{x,y}
            int G[3][2];
            G[0][0] = 0;
            G[1][0] = 0;
            G[2][0] = 0;
            G[0][1] = 0;
            G[1][1] = 0;
            G[2][1] = 0;
            int crse[2][2];
            crse[0][0] = -1;
            crse[1][0] = -1;
            crse[0][1] = 1;
            crse[1][1] = 1;
            if (i == 0)
                crse[0][0] = 0;
            if (j == 0)
                crse[1][0] = 0;
            if (i == height - 1)
                crse[0][1] = 0;
            if (j == width - 1)
                crse[1][1] = 0;
            for (int r = crse[0][0]; r <= crse[0][1]; r++)
            {
                for (int c = crse[1][0]; c <= crse[1][1]; c++)
                {
                    G[0][0] += image[i + r][j + c].rgbtRed * gx[r + 1][c + 1];
                    G[1][0] += image[i + r][j + c].rgbtGreen * gx[r + 1][c + 1];
                    G[2][0] += image[i + r][j + c].rgbtBlue * gx[r + 1][c + 1];
                    G[0][1] += image[i + r][j + c].rgbtRed * gy[r + 1][c + 1];
                    G[1][1] += image[i + r][j + c].rgbtGreen * gy[r + 1][c + 1];
                    G[2][1] += image[i + r][j + c].rgbtBlue * gy[r + 1][c + 1];
                }
            }
            int T[3];
            T[0] = round(sqrt(G[0][0] * G[0][0] + G[0][1] * G[0][1]));
            T[1] = round(sqrt(G[1][0] * G[1][0] + G[1][1] * G[1][1]));
            T[2] = round(sqrt(G[2][0] * G[2][0] + G[2][1] * G[2][1]));

            temp[i][j].rgbtRed = (T[0] > 255) ? 255 : T[0];
            temp[i][j].rgbtGreen = (T[1] > 255) ? 255 : T[1];
            temp[i][j].rgbtBlue = (T[2] > 255) ? 255 : T[2];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
        }
    }
    return;
}
