#ifndef _NIXFONT_FONT_BAHNSCHRIFT_14_H_
#define _NIXFONT_FONT_BAHNSCHRIFT_14_H_

// Libraries
#include <stdint.h>

// Structures
#ifndef _NIXFONT_STRUCTURES_
#define _NIXFONT_STRUCTURES_
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
#endif

// Font
extern const nixfont_font_t font_bahnschrift_14;

#endif
