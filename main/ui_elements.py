import pygame
import os
from settings import UI_FONT, COLOUR_INACTIVE, COLOUR_BUTTON, COLOUR_CHECKBOX_BORDER, COLOUR_CHECKBOX_FILL, SUPERSCRIPT_MAP

class InputBox:
    def __init__(self, x, y, w, h, font=UI_FONT, text='', center_text=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.border_colour = COLOUR_INACTIVE
        self.text_colour = pygame.Color('black')
        self.border_width = 2
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
            self.border_width = 3 if self.active else 2

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.display_text = self.display_text[:-1]

                # Turn off superscript if box is empty
                if not self.text:
                    self.superscript_mode = False

            elif event.key == pygame.K_RIGHT:
                self.superscript_mode = False

            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.border_width = 2

            elif event.key == pygame.K_RETURN:  # submit pressed
                self.submit()

            else:
                self.text += event.unicode

                if event.unicode == "^":
                    self.superscript_mode = True
                else:
                    if self.superscript_mode:
                        self.display_text += SUPERSCRIPT_MAP.get(event.unicode, event.unicode)
                    else:
                        self.display_text += event.unicode

        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

    def submit(self):
        """Called when the user presses Enter/Return"""
        # Reset superscript mode on submit
        self.superscript_mode = False
        # You can also deactivate the box if desired
        self.active = False
        self.border_width = 2
        # Here you could also process self.text as the submitted value

    def draw(self, screen):
        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

        if self.center_text:
            text_rect = self.txt_surface.get_rect(center=self.rect.center)
            screen.blit(self.txt_surface, text_rect.topleft)
        else:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

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
            tick_pos = (self.rect.centerx - self.tick_img.get_width() // 2,
                        self.rect.centery - self.tick_img.get_height() // 2)
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

