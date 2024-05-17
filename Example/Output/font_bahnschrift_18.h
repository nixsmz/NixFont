#ifndef _NIXFONT_FONT_BAHNSCHRIFT_18_H_
#define _NIXFONT_FONT_BAHNSCHRIFT_18_H_

// Libraries
#include <stdint.h>

// Structures
typedef struct {
	uint32_t offset_x;
	uint32_t offset_y;
	uint32_t width;
	uint32_t height;
	const uint8_t *bitmap;
} nixfont_glyph_t;

typedef struct {
	uint32_t height;
	uint32_t count;
	const nixfont_glyph_t **glyphs;
} nixfont_font_t;

// Font
extern const nixfont_font_t font_bahnschrift_18;

#endif
