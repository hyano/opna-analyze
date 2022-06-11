#include <stdio.h>

int main()
{
    int c;
    int prev = -1;
    while ((c = getchar()) != -1)
    {
        if (c != prev)
        {
            //printf("%02x\n", c);
            putchar(c);
            prev = c;
        }
    }
}