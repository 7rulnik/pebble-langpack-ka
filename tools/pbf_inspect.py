#!/usr/bin/env python3
"""Inspect a Pebble language pack (.pbl) or a single PBF font: list slots, glyph ranges and
render sample text as ASCII. Understands PBF v2 (pebble-lang-gen output) and v3 with 16-bit
offsets and RLE4 compression (PebbleOS stock fonts).

    python3 tools/pbf_inspect.py releases/pack.pbl "Hello გამარჯობა" 6
    python3 tools/pbf_inspect.py GOTHIC_24_BOLD.pbf "Hello"
"""
import struct, sys, os

def load_pbf(d):
    version, max_h, n, wild, tsize, cpb = struct.unpack_from('<BBHHBB', d, 0)
    size, features = struct.unpack_from('<BB', d, 8) if version == 3 else (8, 0)
    off16, rle = bool(features & 1), bool(features & 2)
    pos = size
    ht = [struct.unpack_from('<BBH', d, pos + 4 * i) for i in range(tsize)]
    pos += 4 * tsize
    fmt = ('<L' if cpb == 4 else '<H') + ('H' if off16 else 'L')
    esz = cpb + (2 if off16 else 4)
    glyphs = {}
    for _, bucket, acc in ht:
        for j in range(bucket):
            cp, off = struct.unpack_from(fmt, d, pos + acc + j * esz)
            glyphs[cp] = off
    gstart = pos + sum(b for _, b, _ in ht) * esz

    def glyph(cp):
        base = gstart + glyphs[cp]
        w, hu, left, top, adv = struct.unpack_from('<BBbbb', d, base)
        data = d[base + 5:]
        if rle:
            bits, units, i = [], hu, 0
            while units > 0:
                byte = data[i]; i += 1
                for _ in range(2):
                    if units == 0:
                        break
                    bits += [(byte >> 3) & 1] * ((byte & 7) + 1)
                    byte >>= 4; units -= 1
            h = len(bits) // w if w else 0
            bits = bits[:w * h]
        else:
            h = hu
            bits = [(data[k >> 3] >> (k & 7)) & 1 for k in range(w * h)]
        return dict(w=w, h=h, left=left, top=top, adv=adv, rows=[bits[r * w:(r + 1) * w] for r in range(h)])

    return dict(version=version, max_h=max_h, n=n, wildcard=wild, glyphs=glyphs, glyph=glyph)

def load_pbl(d):
    """Pebble resource pack: manifest (num, crc, timestamp), 256 table entries, then contents."""
    num, _, _ = struct.unpack_from('<III', d, 0)
    start = 12 + 256 * 16
    out = []
    for i in range(num):
        _, off, length, _ = struct.unpack_from('<IIII', d, 12 + 16 * i)
        out.append(d[start + off:start + off + length])
    return out

def ranges(cps):
    cps, out = sorted(cps), []
    for cp in cps:
        if out and cp == out[-1][1] + 1:
            out[-1][1] = cp
        else:
            out.append([cp, cp])
    return ', '.join(f'{a:04X}' if a == b else f'{a:04X}-{b:04X}' for a, b in out)

def render(font, text, extra=()):
    fonts = [font, *extra]
    x, cells = 0, []
    for ch in text:
        for f in fonts:
            if ord(ch) in f['glyphs'] and ord(ch) != f['wildcard']:
                g = f['glyph'](ord(ch)); cells.append((x, g)); x += g['adv']; break
        else:
            x += 4
    H = font['max_h'] + 8; W = x + 2
    canvas = [[' '] * W for _ in range(H)]
    for x0, g in cells:
        for r, row in enumerate(g['rows']):
            for c, v in enumerate(row):
                y, xx = g['top'] + r + 1, x0 + g['left'] + c
                if v and 0 <= y < H and 0 <= xx < W:
                    canvas[y][xx] = '#'
    return '\n'.join(''.join(r).rstrip() for r in canvas)

if __name__ == '__main__':
    path = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else ''
    slot = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    d = open(path, 'rb').read()
    if path.endswith('.pbl'):
        contents = load_pbl(d)
        print(f'{os.path.basename(path)}: {len(contents)} resources, {len(d)} bytes')
        for i, c in enumerate(contents):
            if i == 0:
                hdr = c[c.find(b'Project'):].split(b'\x00')[0].decode('utf-8', 'replace').strip().replace('\n', ' | ')
                print(f'  000 translation: {hdr}'); continue
            if not c:
                print(f'  {i:03d}: empty'); continue
            f = load_pbf(c)
            print(f"  {i:03d}: v{f['version']} h={f['max_h']} glyphs={f['n']} {len(c)} bytes  {ranges(f['glyphs'])[:120]}")
        if text and contents[slot]:
            print(render(load_pbf(contents[slot]), text))
    else:
        f = load_pbf(d)
        print(f"{os.path.basename(path)}: v{f['version']} h={f['max_h']} glyphs={f['n']}  {ranges(f['glyphs'])}")
        if text:
            print(render(f, text))
