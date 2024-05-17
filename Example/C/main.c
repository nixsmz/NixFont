#include "../Output/font_bahnschrift_18.h"

#include <stdint.h>
#include <stdio.h>

static void print_string(const nixfont_font_t *font, const char *string) {
    nixfont_glyph_t *g = NULL;
    for(uint32_t i = 0; i < font->height; i++) {
        for(uint32_t c = 0; string[c]; c++) {
            g = (nixfont_glyph_t*)font->glyphs[string[c]-' '];
            for(uint32_t ii = 0; ii < g->offset_x; ii++) printf(" ");
            for(uint32_t ii = 0; ii < g->width; ii++) {
                if(i < g->offset_y) printf(" ");
                else if((i < g->offset_y+g->height) && g->bitmap) {
                    if(g->bitmap[(i-g->offset_y)*g->width+ii] >= 100) printf("#");
                    else printf(" ");
                } else printf(" ");
            }
            printf(" ");
        }
        printf("\n");
    }
}

int main() {
    print_string(&font_bahnschrift_18, "nixfont is nice !");
    return 0;
}
