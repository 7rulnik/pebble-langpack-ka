# Georgian + Russian glyphs for Pebble

A language pack for Pebble watches running PebbleOS (Core Devices and Rebble firmware). It adds
glyphs the stock fonts lack while keeping the English interface:

- Georgian: Mkhedruli, Mtavruli capitals, Asomtavruli, Nuskhuri (U+10A0–10FF, U+1C90–1CBF, U+2D00–2D2F)
- Cyrillic and Cyrillic Supplement (U+0400–052F)
- ₾ ₽ №

Only one language pack can be installed at a time, and the stock fonts contain Latin only. A
Georgian-only pack therefore removes Cyrillic; this pack carries both and is a superset of the
"English + Кириллица" pack from the app's list.

## Install

Download `pebble-langpack-georgian-russian.pbl` from the
[latest release](https://github.com/7rulnik/pebble-langpack-ka-ru/releases/latest), copy it to
the phone and open it with the Pebble app. On Android, save it with a file manager first: opening
straight from the browser can fail. The app shows the pack under its file name until the watch
reconnects, then as `en_GE (v1)`.

From a Mac with adb:

```sh
adb push pebble-langpack-georgian-russian.pbl /sdcard/Download/
adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE \
    -d file:///sdcard/Download/pebble-langpack-georgian-russian.pbl
ID=$(adb shell content query --uri content://media/external/downloads --projection _id \
    --where "\"_display_name='pebble-langpack-georgian-russian.pbl'\"" | sed -n 's/.*_id=\([0-9]*\).*/\1/p' | tail -1)
adb shell am start -a android.intent.action.VIEW -d "content://media/external/downloads/$ID" \
    -t application/octet-stream --grant-read-uri-permission -n coredevices.coreapp/.MainActivity
```

## How it looks

Cyrillic in the 14–28 px Gothic fonts is pixel-identical to the stock Latin. Georgian is drawn
by Noto Sans Georgian, sized so that its capitals and lowercase are as tall as Gothic's, with
stem widths matching Gothic Regular and Bold. Notification body font, 24 px bold: stock Latin,
Rebble Cyrillic, Noto Sans Georgian Medium at 20 px, then `Oo` next to Cyrillic `Оо`:

```
                                                                                                                                                           #
                                                                                                                            ######                    #####                                    ##
 ##    ##           ##  ##               ########                                                                          ########                 ######                                     ###                       ####                   ####
 ##    ##           ##  ##               ########                                                                          ##    ##                ##                                           ###                     ######                 ######
 ##    ##           ##  ##               ##    ##                                                                                 ##              ##                                             ##                    ###  ###               ###  ###
 ##    ##    ###    ##  ##    ###        ##    ##  ## ###   ##   ##  #####      ###    ######         ####        ###       ####  ##     ###      # ###  ####        ##       ####  ####       ####        ###         ##    ##    ###        ##    ##    ###
 ##    ##   #####   ##  ##   #####       ##    ##  #######  ##  ###  ######    #####   ######        ######        ##      #########      ##     #############       ##      ############    ########       ##         ##    ##   #####       ##    ##   #####
 ##    ##  ##   ##  ##  ##  ##   ##      ##    ##  ##   ##  ##  ###  ##   ##  ##   ##    ##         ##    ##       ###     ##    ###      ###    ###   ###  ###  ######      ##   ###   ##   ##    ##       ###        ##    ##  ##   ##      ##    ##  ##   ##
 ########  ##   ##  ##  ##  ##   ##      ##    ##  ##   ##  ## ####  ##   ##  ##   ##    ##         ##    ##        ###   ###    ###       ###   ##    ##    ##   ########  ##    ##    ##  ###     ##       ###       ##    ##  ##   ##      ##    ##  ##   ##
 ########  #######  ##  ##  ##   ##      ##    ##  ##   ##  ## ####  ######   #######    ##              ##          ###  ##      ##        ###  ##    ##    ##      #####  ##    ##    ##  ##      ##        ###      ##    ##  ##   ##      ##    ##  ##   ##
 ##    ##  #######  ##  ##  ##   ##      ##    ##  ##   ##  #######  ######   #######    ##           #####    ##     ##  ##      ##  ##     ##  ##    ##    ##      ##     ##    ##    ##  ##      ##  ##     ##      ##    ##  ##   ##      ##    ##  ##   ##
 ##    ##  ##       ##  ##  ##   ##      ##    ##  ##   ##  #### ##  ##   ##  ##         ##          ######    ##     ##  ##      ##  ##     ##  ##    ##    ##      ##     ##    ##    ##  ##      ##  ##     ##      ##    ##  ##   ##      ##    ##  ##   ##
 ##    ##  ##   ##  ##  ##  ##   ##      ##    ##  ##   ##  ###  ##  ##   ##  ##   ##    ##         ##    ##   ##     ##  ###    ###  ##     ##  ##          ##       ##    ##          ##  ###     ##  ##     ##      ##    ##  ##   ##      ##    ##  ##   ##
 ##    ##  ##   ##  ##  ##  ##   ##      ##    ##  ##   ##  ###  ##  ##   ##  ##   ##    ##        ###    ###  ###   ###   ##    ##   ###   ###  ###         ##        ##   ###         ##   ##    ###  ###   ###      ###  ###  ##   ##      ###  ###  ##   ##
 ##    ##   #####   ##  ##   #####       ##    ##  #######  ##   ##  ######    #####     ##        ##      ##   #######    ########    #######    ##         ##        ###   ##         ##   ########    #######        ######    #####        ######    #####
 ##    ##    ###    ##  ##    ###        ##    ##  ## ###   ##   ##  #####      ###      ##        ##      ##    #####       ####       #####     ##        ##   ##     ##   ##        ##      #####      #####          ####      ###          ####      ###
                                                   ##                                              ##      ##                                                    ##     ###
                                                   ##                                              ##      ##                                                    ##     ##
                                                   ##                                               ##    ##                                                     ###    ##
                                                   ##                                               ########                                                      ########
                                                                                                      ####                                                         #####
```

## Where the glyphs come from

| Script | Source | Why |
|---|---|---|
| Cyrillic, 104 letters for Russian, Ukrainian, Belarusian, Serbian, Kazakh, 14–28 px | Official Rebble `ru_RU` pack, converted to PBFF text in `pbff/rebble_ru/` | Pixel-identical to the stock Gothic: same cap height, x-height, stem width, advance |
| Georgian, all sizes | [Noto Sans Georgian](https://github.com/notofonts/georgian) statics in `ttf/`, SIL OFL | Rendered at a smaller pixel size than the slot so its metrics match Gothic |
| Remaining Cyrillic, ₾ ₽ №, all Cyrillic at 36 px | Go Noto Kurrent Regular and Bold from [go-noto-universal](https://github.com/satbyy/go-noto-universal), SIL OFL | Fallback for letters the Rebble pack lacks |

The Rebble Cyrillic glyphs are Pebble's original language-pack artwork as distributed by Rebble
(`lp.rebble.io`); they are not under a free license and are included as-is.

### Sizing

Noto is rendered smaller than the slot's nominal size so that cap height and x-height equal
Gothic's; the baseline stays at the slot height (`height` + `offset` in `lang/fonts.json`):

| Slot | Gothic cap / x-height | Noto px | Georgian weight, regular / bold slot |
|---|---|---|---|
| 14 | 9 / 7 | 13, bold 12 | Regular / SemiBold |
| 18 | 11 / 8 | 15 | Regular / Medium |
| 24 | 14 / 11 | 20 | Regular / Medium |
| 28 | 18 / 14 | 25 | Regular / Medium |
| 36 | 22 / 16 | 30 | Regular / SemiBold |

Bold weights were chosen so the vertical stem equals Gothic Bold's: 2 px up to 24, 3 px at 28,
4 px at 36. Noto Bold is one pixel heavier at 24 and 28 px.

Only the ten Gothic slots are filled. PebbleOS asserts that a glyph bitmap fits in 256 bytes
(`MAX_FONT_GLYPH_SIZE`); wide letters in the 42–49 px Bitham and Roboto slots exceed it and would
reboot the watch. Official Core Devices packs fill the Gothic slots only for the same reason.

The pack reports locale `en_GE` and the name "English + Georgian/Cyrillic", following Core Devices'
`en_IL` / `en_SA` convention for English-UI packs with extra glyphs.

## Rebuild

Built with [pebble-lang-gen](https://github.com/Pyxzure/pebble-lang-gen):

```sh
git clone https://github.com/Pyxzure/pebble-lang-gen && cd pebble-lang-gen
rm lang/kanji.txt
cp <this repo>/lang/* lang/
cp -r <this repo>/pbff/rebble_ru pbff/
cp <this repo>/ttf/*.ttf ttf/
cp <this repo>/translation/000.po translation/
curl -L -o ttf/GoNotoKurrent-Bold.ttf \
  https://github.com/satbyy/go-noto-universal/releases/download/v7.0/GoNotoKurrent-Bold.ttf
msgfmt -o translation/000 translation/000.po        # brew install gettext
python3 -m venv .venv && .venv/bin/pip install freetype-py
.venv/bin/python build.py                           # -> build/langpack.pbl
```

`tools/pbf_inspect.py` lists a pack's slots and glyph ranges and renders text as ASCII; it also
decodes the stock PebbleOS PBF fonts (v3, RLE4), which is how the sizes above were measured:

```sh
python3 tools/pbf_inspect.py build/langpack.pbl "Hello Привет გამარჯობა" 6
```

## Testing from a Mac

The Pebble app mutes system apps such as `com.android.shell` by default. Enable it once under
Notifications → Apps → "Show system apps" → Shell, then post a notification with any text:

```sh
adb shell 'cmd notification post -S bigtext -t "გამარჯობა, Валентин" test1 "Hello Привет · Oo Оо Hh Нн"'
```

Pass the whole command as one quoted string: adb does not escape spaces between arguments.

## License

MIT for the configuration and tools in this repository. Fonts keep their own licenses: SIL OFL for
Noto Sans Georgian and Go Noto Kurrent (`ttf/OFL-NotoSansGeorgian.txt`), Pebble's terms for the
Rebble Cyrillic glyphs.
