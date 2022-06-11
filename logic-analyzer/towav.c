#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>

#include <sndfile.h>

#define SAMPLE_RATE (7987200 / 144)
#define CHANNELS (2)
#define BUFFER_COUNT (1024 * 1024)
#define INTRO_SAMPLES (100)

SNDFILE *file = NULL;
static int16_t buffer[BUFFER_COUNT * CHANNELS];
static int32_t buffer_wp = 0;

SNDFILE *file_stat = NULL;
static int16_t buffer_stat[BUFFER_COUNT * 2];
SNDFILE *file_opt = NULL;
static int16_t buffer_opt[BUFFER_COUNT * 1];


static void flush_data(void)
{
    sf_write_short(file, buffer, buffer_wp * CHANNELS);
    if (file_stat)
        sf_write_short(file_stat, buffer_stat, buffer_wp * 2);
    if (file_opt)
        sf_write_short(file_opt, buffer_opt, buffer_wp * 1);
    buffer_wp = 0;
}

static void write_data(int16_t sample_ch1, int16_t sample_ch2)
{
    buffer[buffer_wp * 2 + 0] = sample_ch1;
    buffer[buffer_wp * 2 + 1] = sample_ch2;
    buffer_wp++;
    if (buffer_wp >= BUFFER_COUNT)
    {
        flush_data();
    }
}

static void write_stat(int16_t s0, int16_t s1, int16_t s2)
{
    buffer_stat[buffer_wp * 2 + 0] = s0;
    buffer_stat[buffer_wp * 2 + 1] = s1;
    buffer_opt[buffer_wp * 1] = s2;
}


int main(int argc, char *argv[])
{
    int c;
    uint32_t data;
    uint32_t prev = 0xffffffff;
    uint32_t diff;
    uint16_t sample;
    int16_t sample_ch1 = 0;
    int16_t sample_ch2 = 0;
    uint32_t start = 0;
    int32_t num_sample = 0;
    int32_t max_sample = -1;
    uint32_t stat[3][2];
    int num_stat = 3;

    int opt;
    bool opt_s = false;
    bool opt_m = false;

    char fname[128] = "test_pcm.wav";
    char fname_stat[128] = "test_stat.wav";
    char fname_opt[128] = "test_opt.wav";

    while ((opt = getopt(argc, argv, "o:l:sm")) != -1)
    {
        switch (opt)
        {
        case 'o':
            sprintf(fname, "%s_pcm.wav", optarg);
            sprintf(fname_stat, "%s_stat.wav", optarg);
            sprintf(fname_opt, "%s_opt.wav", optarg);
            break;
        case 'l':
            max_sample = atoi(optarg) * SAMPLE_RATE;
            break;
        case 's':
            opt_s = true;
            break;
        case 'm':
            opt_m = true;
            break;
        default:
            printf("Options:\n");
            printf("  -o fname\n");
            printf("  -l length (seconds)\n");
            exit(1);
            break;
        }
    }

    SF_INFO sfinfo;
    memset(&sfinfo, 0, sizeof(sfinfo));
    sfinfo.samplerate = SAMPLE_RATE;
    sfinfo.channels = CHANNELS;
    sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;

    file = sf_open(fname, SFM_WRITE, &sfinfo);
    if (file == NULL)
    {
        printf("file open error\n");
        return 1;
    }

    if (opt_s || opt_m)
    {
        memset(&sfinfo, 0, sizeof(sfinfo));
        sfinfo.samplerate = SAMPLE_RATE;
        sfinfo.channels = 2;
        sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;

        file_stat = sf_open(fname_stat, SFM_WRITE, &sfinfo);
        if (file_stat == NULL)
        {
            printf("stat file open error\n");
            return 1;
        }

        memset(&sfinfo, 0, sizeof(sfinfo));
        sfinfo.samplerate = SAMPLE_RATE;
        sfinfo.channels = 1;
        sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;

        file_opt = sf_open(fname_opt, SFM_WRITE, &sfinfo);
        if (file_opt == NULL)
        {
            printf("opt file open error\n");
            return 1;
        }
    }

    if (opt_m) num_stat = 2;

    for (int i = 0; i < 3; i++)
    {
        stat[i][0] = 0;
        stat[i][1] = 0;
    }

    while ((c = getchar()) != -1)
    {
        data = (uint32_t)c;
        if (data == prev)
            continue;
        diff = data ^ prev;
        prev = data;

        //printf("%02x\n", data);

        uint32_t clk = (data >> 0) & 1;
        uint32_t sd = (data >> 1) & 1;
        uint32_t smp1 = (data >> 2) & 1;
        uint32_t smp2 = (data >> 3) & 1;
        uint32_t cs = (data >> 4) & 1;
        uint32_t s[3];
        s[0] = (data >> 5) & 1;
        s[1] = (data >> 6) & 1;
        s[2] = (data >> 7) & 1;

        if ((diff & 16) && (cs == 1))
        {
            for (int i = 0; i < num_stat; i++)
            {
                stat[i][s[i]]++;
            }
        }
        if (opt_m && (s[2] != 0))
        {
            stat[2][1]++;
        }

        if ((diff & 1) && (clk == 0))
        {
            sample = (sample >> 1) | (sd << 15);
        }

        if ((diff & 8) && smp2 == 0)
        {
            sample_ch1 = (int16_t)(sample ^ 0x8000);
        }
        if ((diff & 4) && smp1 == 0)
        {
            sample_ch2 = (int16_t)(sample ^ 0x8000);

            int16_t sv[3] = {0, 0, 0};

            for (int i = 0; i < 3; i++)
            {
                if (stat[i][0] == 0 && stat[i][1] == 0)
                {
                    sv[i] = 0;
                }
                else if (stat[i][0] != 0 && stat[i][1] == 0)
                {
                    sv[i] = 0x1000;
                }
                else if (stat[i][0] != 0 && stat[i][1] != 0)
                {
                    sv[i] = 0x4000;
                }
                else if (stat[i][0] == 0 && stat[i][1] != 0)
                {
                    sv[i] = 0x6000;
                }
                stat[i][0] = stat[i][1] = 0;
            }

            if (start == 0)
            {
                start++;
            }
            else if (start  == 1)
            {
                if (sample_ch1 || sample_ch2)
                {
                    printf("start (%04x:%04x)\n", sample_ch1, sample_ch2);
                    for (int i = 0; i < INTRO_SAMPLES; i++)
                    {
                        write_stat(0, 0, 0);
                        write_data(0, 0);
                    }
                    write_stat(sv[0], sv[1], sv[2]);
                    write_data(sample_ch1, sample_ch2);
                    num_sample++;
                    start++;
                }
            }
            else
            {
                write_stat(sv[0], sv[1], sv[2]);
                write_data(sample_ch1, sample_ch2);
                num_sample++;
            }
        }

        if (max_sample > 0 && num_sample > max_sample)
        {
            break;
        }
    }

    flush_data();

    printf("end\n");

    sf_close(file);

    return 0;
}
