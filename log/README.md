# ロジアナのログ毎の信号線の繋ぎ方メモ

## _mden

|ch     | chip      |signal     |note       |
|:------|:----------|:----------|:----------|
|D0     |YM3016     |CLOCK      | |
|D1     |YM3016     |SD         | |
|D2     |YM3016     |SMP1       | |
|D3     |YM3016     |SMP2       | |
|D4     |YM2608     |/CS        | for OPNA access timing |
|D5     |YM2608     |D2         | for EOS status |
|D6     |YM2608     |D3         | for BRDY statis |
|D7     |YM2608     |MDEN       | for memory access |

## _pcmbusy

|ch     | chip      |signal     |note       |
|:------|:----------|:----------|:----------|
|D0     |YM3016     |CLOCK      | |
|D1     |YM3016     |SD         | |
|D2     |YM3016     |SMP1       | |
|D3     |YM3016     |SMP2       | |
|D4     |YM2608     |/CS        | for OPNA access timing |
|D5     |YM2608     |D2         | for EOS status |
|D6     |YM2608     |D3         | for BRDY statis |
|D7     |YM2608     |D5         | for PCMBUSY status |

## キャプチャのコマンドライン

```
sigrok-cli -d fx2lafw --config samplerate=16MHz -O binary --time=50s -o XXX.bin         
```
