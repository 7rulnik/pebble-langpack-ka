# Georgian glyphs for Pebble

A language pack for Pebble watches running PebbleOS (Core Devices and Rebble firmware). It adds
Georgian to the system fonts while keeping the English interface:

- Mkhedruli, Mtavruli capitals, Asomtavruli, Nuskhuri (U+10A0–10FF, U+1C90–1CBF, U+2D00–2D2F)
- ₾

## Combining with other packs

PebbleOS v4.42.0 and later, with Pebble app 1.18.0 or later, holds up to four language packs. The
selected pack translates the interface and every installed pack contributes its glyphs, so this
pack works next to any other: add `ru_RU` or `uk_UA` from the app's list for Cyrillic. The pack
carries an empty English translation, so selecting it keeps the interface in English, and
selecting another language keeps the Georgian glyphs.

Older firmware holds one pack at a time. For Georgian and Cyrillic together there, use
`pebble-langpack-georgian-russian.pbl` from
[v1.0.0](https://github.com/7rulnik/pebble-langpack-ka/releases/tag/v1.0.0).

## Install

Download `pebble-langpack-georgian.pbl` from the
[latest release](https://github.com/7rulnik/pebble-langpack-ka/releases/latest), copy it to
the phone and open it with the Pebble app. On Android, save it with a file manager first: opening
straight from the browser can fail. The app shows the pack under its file name until the watch
reconnects, then as `en_GE (v2)`.

From a Mac with adb:

```sh
adb push pebble-langpack-georgian.pbl /sdcard/Download/
adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE \
    -d file:///sdcard/Download/pebble-langpack-georgian.pbl
ID=$(adb shell content query --uri content://media/external/downloads --projection _id \
    --where "\"_display_name='pebble-langpack-georgian.pbl'\"" | sed -n 's/.*_id=\([0-9]*\).*/\1/p' | tail -1)
adb shell am start -a android.intent.action.VIEW -d "content://media/external/downloads/$ID" \
    -t application/octet-stream --grant-read-uri-permission -n coredevices.coreapp/.MainActivity
```

## How it looks

Georgian is drawn by [Noto Sans Georgian](https://github.com/notofonts/georgian), sized so that
its capitals and lowercase are as tall as Gothic's, with stem widths matching Gothic Regular and
Bold. Notification body font, 24 px bold: stock Latin, then Noto Sans Georgian Medium at 20 px:

```
                                                                                                 #
                                                                  ######                    #####                                    ##
 ##    ##           ##  ##                                       ########                 ######                                     ###
 ##    ##           ##  ##                                       ##    ##                ##                                           ###
 ##    ##           ##  ##                                              ##              ##                                             ##
 ##    ##    ###    ##  ##    ###           ####        ###       ####  ##     ###      # ###  ####        ##       ####  ####       ####        ###
 ##    ##   #####   ##  ##   #####         ######        ##      #########      ##     #############       ##      ############    ########       ##
 ##    ##  ##   ##  ##  ##  ##   ##       ##    ##       ###     ##    ###      ###    ###   ###  ###  ######      ##   ###   ##   ##    ##       ###
 ########  ##   ##  ##  ##  ##   ##       ##    ##        ###   ###    ###       ###   ##    ##    ##   ########  ##    ##    ##  ###     ##       ###
 ########  #######  ##  ##  ##   ##            ##          ###  ##      ##        ###  ##    ##    ##      #####  ##    ##    ##  ##      ##        ###
 ##    ##  #######  ##  ##  ##   ##         #####    ##     ##  ##      ##  ##     ##  ##    ##    ##      ##     ##    ##    ##  ##      ##  ##     ##
 ##    ##  ##       ##  ##  ##   ##        ######    ##     ##  ##      ##  ##     ##  ##    ##    ##      ##     ##    ##    ##  ##      ##  ##     ##
 ##    ##  ##   ##  ##  ##  ##   ##       ##    ##   ##     ##  ###    ###  ##     ##  ##          ##       ##    ##          ##  ###     ##  ##     ##
 ##    ##  ##   ##  ##  ##  ##   ##      ###    ###  ###   ###   ##    ##   ###   ###  ###         ##        ##   ###         ##   ##    ###  ###   ###
 ##    ##   #####   ##  ##   #####       ##      ##   #######    ########    #######    ##         ##        ###   ##         ##   ########    #######
 ##    ##    ###    ##  ##    ###        ##      ##    #####       ####       #####     ##        ##   ##     ##   ##        ##      #####      #####
                                         ##      ##                                                    ##     ###
                                         ##      ##                                                    ##     ##
                                          ##    ##                                                     ###    ##
                                          ########                                                      ########
                                            ####                                                         #####


```

### Sizing

The glyphs are rendered from the Noto Sans Georgian statics in `ttf/` (SIL OFL), including ₾. Noto
is rendered smaller than the slot's nominal size so that cap height and x-height equal Gothic's;
the baseline stays at the slot height (`height` + `offset` in `lang/fonts.json`):

| Slot | Gothic cap / x-height | Noto px | Weight, regular / bold slot |
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

The pack reports locale `en_GE` and the name "English + Georgian", following Core Devices'
`en_IL` / `en_SA` convention for English-UI packs with extra glyphs. The name stays in Latin
because the watch reports pack names to the app in 30 bytes, and "English + ქართული" takes 31.

## Rebuild

Built with [pebble-lang-gen](https://github.com/Pyxzure/pebble-lang-gen):

```sh
git clone https://github.com/Pyxzure/pebble-lang-gen && cd pebble-lang-gen
rm lang/kanji.txt
cp <this repo>/lang/* lang/
cp <this repo>/ttf/*.ttf ttf/
cp <this repo>/translation/000.po translation/
msgfmt -o translation/000 translation/000.po        # brew install gettext
python3 -m venv .venv && .venv/bin/pip install freetype-py
.venv/bin/python build.py                           # -> build/langpack.pbl
```

`tools/pbf_inspect.py` lists a pack's slots and glyph ranges and renders text as ASCII; it also
decodes the stock PebbleOS PBF fonts (v3, RLE4), which is how the sizes above were measured:

```sh
python3 tools/pbf_inspect.py build/langpack.pbl "გამარჯობა ₾" 6
```

## Testing from a Mac

The Pebble app mutes system apps such as `com.android.shell` by default. Enable it once under
Notifications → Apps → "Show system apps" → Shell, then post a notification with any text:

```sh
adb shell 'cmd notification post -S bigtext -t "გამარჯობა" test1 "Hello გამარჯობა · 25₾"'
```

Pass the whole command as one quoted string: adb does not escape spaces between arguments.

## License

MIT for the configuration and tools in this repository. Noto Sans Georgian keeps its SIL OFL
(`ttf/OFL-NotoSansGeorgian.txt`).
