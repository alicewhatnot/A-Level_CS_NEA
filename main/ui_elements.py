import pygame
from settings import UI_FONT, COLOUR_INACTIVE, COLOUR_ACTIVE, COLOUR_BUTTON, COLOUR_CHECKBOX_BORDER, COLOUR_CHECKBOX_FILL, SUPERSCRIPT_MAP
class InputBox:
    def __init__(self, x, y, w, h, font=UI_FONT, text='', center_text=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.border_colour = COLOUR_INACTIVE  # border colour
        self.text_colour = pygame.Color('black')  # text stays black
        self.text = text
        self.display_text = text
        self.font = font
        self.center_text = center_text
        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)
        self.active = False
        self.superscript_mode = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            # border changes only when clicked
            self.border_colour = COLOUR_ACTIVE if self.active else COLOUR_INACTIVE

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.display_text = self.display_text[:-1]

            elif event.key == pygame.K_RIGHT:
                self.superscript_mode = False

            elif event.unicode == "^":
                self.text += "^"
                self.superscript_mode = True

            else:
                self.text += event.unicode
                if self.superscript_mode:
                    self.display_text += SUPERSCRIPT_MAP.get(event.unicode, event.unicode)
                else:
                    self.display_text += event.unicode

        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

    def draw(self, screen):
        # render text
        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

        if self.center_text:
            text_rect = self.txt_surface.get_rect(center=self.rect.center)
            screen.blit(self.txt_surface, text_rect.topleft)
        else:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # draw border only
        pygame.draw.rect(screen, self.border_colour, self.rect, 2)

    def getText(self):
        return self.text


class Checkbox:
    def __init__(self, x, y, w, h, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.checked = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked

    def draw(self, screen):
        pygame.draw.rect(screen, COLOUR_CHECKBOX_BORDER, self.rect, 2)
        if self.checked:
            pygame.draw.rect(screen, COLOUR_CHECKBOX_FILL, self.rect.inflate(-4, -4))
        label_surface = UI_FONT.render(self.label, True, (0, 0, 0))
        screen.blit(label_surface, (self.rect.x + 30, self.rect.y - 2))

    def getValue(self):
        return self.checked


class Button:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, COLOUR_BUTTON, self.rect)
        txt_surf = UI_FONT.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surf, (self.rect.x + 10, self.rect.y + 8))

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