from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys

CHARSET = str(''.join([chr(x) for x in range(ord(" "), ord("~"))]))

def get_glyph(text: str, font: ImageFont.FreeTypeFont) -> dict:
    img = Image.new('RGB', [font.size, font.size], (0,0,0))
    ImageDraw.Draw(img).text((0,0), text[0] if text[0] != " " else " W", font=font, fill="#FFFFFF")
    letter = np.asarray(img.convert('L'))
    stats, zx, zy = {"x": (0, font.size-1), "y": (0, font.size-1)}, [], []
    if text[0] != " ":
        for i in range(font.size):
            if len(list(filter(lambda x: x > 0, letter[i,:]))) > 0: zy.append(i)
            if len(list(filter(lambda x: x > 0, letter[:,i]))) > 0: zx.append(i)
        xmin, xmax, ymin, ymax = min(zx), max(zx), min(zy), max(zy)
        stats["x"] = (xmin, xmax)
        stats["y"] = (ymin, ymax)
        stats["bitmap"] = letter[ymin:ymax, xmin:xmax]
    else:
        i = 0
        while len(list(filter(lambda x: x > 0, letter[:,i]))) < 1: i += 1
        stats["x"] = (0, i)
        stats["bitmap"] = None
    return stats

font_size = 18
font_file = "bahnschrift.ttf"
font_chars = str("".join(sorted(set(CHARSET))))
font_name = (f"font_{font_file.split(".")[0]}_{font_size}").lower()
font = ImageFont.truetype(font_file, size=font_size, encoding="unic")

# Writing C file
with open(f"{font_name}.c", "w+") as output_c:
    output_c.write(f'#include "{font_name}.h"\n\n#include <stdlib.h>\n\n')
    chars_list, max_height = [], 0
    for c in CHARSET:
        try:
            glyph = get_glyph(c, font)
            glyph_name = f"{font_name}_glyph_{ord(c):04x}"
            width, height = glyph["x"][1] - glyph["x"][0], glyph["y"][1] - glyph["y"][0]
            if height > max_height: max_height = height
            output_c.write(f'static const nixfont_glyph_t {glyph_name} = {"{"}\n')
            output_c.write(f'\t.offset_x = {glyph["x"][0]},\n')
            output_c.write(f'\t.offset_y = {glyph["y"][0]},\n')
            output_c.write(f'\t.width = {width},\n')
            output_c.write(f'\t.height = {height},\n')
            if glyph["bitmap"] is not None: 
                output_c.write(f'\t.bitmap = (uint8_t[]){"{"}\n')
                for i in range(height):
                    output_c.write(f'\t\t{",".join(
                        [str(f"0x{x:02x}") for x in glyph["bitmap"][i]]
                    )}{"" if i == (height-1) else ","}\n')
                output_c.write(f'\t{"}"}\n')
            else: output_c.write(f'\t.bitmap = NULL\n')
            output_c.write('};\n\n')
            chars_list.append(glyph_name)
        except: print(f"Error with char {ord(c)}.")
    output_c.write(f'static const nixfont_font_t {font_name} = {"{"}\n')
    output_c.write(f'\t.height = {max_height},\n')
    output_c.write(f'\t.count = {len(chars_list)},\n')
    if len(chars_list) > 0:
        output_c.write(f'\t.glyphs = (nixfont_glyph_t[]){"{"}\n\t\t&')
        output_c.write(f'{",\n\t\t&".join(chars_list)}\n')
        output_c.write(f'\t{"}"}\n')
    else: output_c.write(f'\t.glyphs = NULL\n')
    output_c.write('};\n\n')
    output_c.close()

# Writing header file
with open(f"{font_name}.h", "w+") as output_h:
    output_h.write(f'#ifndef _NIXFONT_{font_name.upper()}_H_\n')
    output_h.write(f'#define _NIXFONT_{font_name.upper()}_H_\n\n')
    output_h.write('// Libraries\n#include <stdint.h>\n\n')
    output_h.write('// Structures\n' +
                   'typedef struct {\n' +
                   '\tuint32_t offset_x;\n' +
                   '\tuint32_t offset_y;\n' +
                   '\tuint32_t width;\n' +
                   '\tuint32_t height;\n' +
                   '\tconst uint8_t *bitmap;\n' +
                   '} nixfont_glyph_t;\n\n' +
                   'typedef struct {\n' +
                   '\tuint32_t height;\n' +
                   '\tuint32_t count;\n' +
                   '\tconst nixfont_glyph_t *glyphs;\n' +
                   '} nixfont_font_t;\n\n')
    output_h.write(f'// Font\n')
    output_h.write(f'extern const nixfont_font_t {font_name};\n\n')
    output_h.write(f'#endif\n')
    output_h.close()
