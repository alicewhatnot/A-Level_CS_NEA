import pygame
from settings import UI_FONT, COLOUR_INACTIVE, COLOUR_BUTTON, COLOUR_CHECKBOX_BORDER, COLOUR_CHECKBOX_FILL, SUPERSCRIPT_MAP, IGNORE_KEYS

class InputBox:
    def __init__(self, x, y, w, h, font=UI_FONT, text='', center_text=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.border_colour = COLOUR_INACTIVE
        self.text_colour = pygame.Color('black')
        self.border_width = 2
        self.text = text  # actual text
        self.display_text = text  # what is rendered
        self.font = font
        self.center_text = center_text
        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)
        self.active = False
        self.superscript_mode = False
        self.allow_get = True

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.border_width = 3 if self.active else 2

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END]:
                self.superscript_mode = False

            elif event.key == pygame.K_BACKSPACE:
                # Check if Ctrl is held
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    # Ctrl+Backspace: delete all text
                    self.text = ""
                    self.display_text = ""
                    self.superscript_mode = False
                else:
                    if not self.text:
                        return
                    # Remove last character from actual text
                    removed_char = self.text[-1]
                    self.text = self.text[:-1]

                    # Rebuild display_text
                    self.display_text = self.buildDisplayText(self.text)
                    # Update superscript mode if last char was ^
                    self.superscript_mode = self.text.endswith('^')

            elif event.key not in IGNORE_KEYS:
                char = event.unicode
                if char == "^":
                    if self.text and (self.text[-1].isalnum() or self.text[-1] == ")"):
                        self.text += char
                        self.superscript_mode = True
                else:
                    if self.superscript_mode:
                        self.display_text += SUPERSCRIPT_MAP.get(char, char)
                        self.text += char
                    else:
                        self.text += char
                        self.display_text += char

            # Always rebuild display_text in case of inconsistencies
            self.display_text = self.buildDisplayText(self.text)
            self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

    def buildDisplayText(self, text):
        """Rebuilds display_text from text, applying superscript after ^"""
        result = ""
        superscript_next = False
        for c in text:
            if c == "^":
                superscript_next = True
            else:
                if superscript_next:
                    result += SUPERSCRIPT_MAP.get(c, c)
                    superscript_next = False
                else:
                    result += c
        return result

    def draw(self, screen):
        full_surface = self.font.render(self.display_text, True, self.text_colour)

        if full_surface.get_width() > self.rect.width - 10:
            clip_rect = pygame.Rect(
                full_surface.get_width() - (self.rect.width - 10),
                0,
                self.rect.width - 10,
                full_surface.get_height()
            )
            visible_surface = full_surface.subsurface(clip_rect)
        else:
            visible_surface = full_surface

        if self.center_text:
            text_rect = visible_surface.get_rect(center=self.rect.center)
            screen.blit(visible_surface, text_rect.topleft)
        else:
            screen.blit(visible_surface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.border_colour, self.rect, self.border_width)

    def getText(self):
        return self.text


class Checkbox:
    def __init__(self, x, y, w, h, label="", tick_img=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.checked = False
        self.tick_img = tick_img

    def draw(self, screen):
        pygame.draw.rect(screen, COLOUR_CHECKBOX_BORDER, self.rect, 2)
        if self.checked and self.tick_img:
            tick_pos = (self.rect.centerx - self.tick_img.get_width() // 2, self.rect.centery - self.tick_img.get_height() // 2)
            screen.blit(self.tick_img, tick_pos)
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked

    def getValue(self):
        return self.checked

class Button:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.scale = 1.0
        self.hover_scale = 1.05  # scale when hovered

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.scale = self.hover_scale
        else:
            self.scale = 1.0

    def draw(self, screen):
        scaled_rect = self.rect.copy()
        scaled_rect.width = int(self.rect.width * self.scale)
        scaled_rect.height = int(self.rect.height * self.scale)
        scaled_rect.center = self.rect.center  # keep the center in place

        pygame.draw.rect(screen, COLOUR_BUTTON, scaled_rect)
        txt_surf = UI_FONT.render(self.text, True, (0, 0, 0))
        text_rect = txt_surf.get_rect(center=scaled_rect.center)
        screen.blit(txt_surf, text_rect.topleft)

    def isClicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Text:
    def __init__(self, x, y, text, colour=(0, 0, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour

    def draw(self, screen):
        txt_surface = UI_FONT.render(self.text, True, self.colour)
        screen.blit(txt_surface, (self.x, self.y))

    def setText(self, new_text):
        self.text = new_text

