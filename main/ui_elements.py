import pygame
from settings import FONT, COLOR_INACTIVE, COLOR_ACTIVE, COLOR_BUTTON, COLOR_CHECKBOX_BORDER, COLOR_CHECKBOX_FILL

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, (0, 0, 0))
        self.active = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = COLOR_INACTIVE
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def getText(self):
        return self.text


class Checkbox:
    def __init__(self, x, y, label):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_CHECKBOX_BORDER, self.rect, 2)
        if self.checked:
            pygame.draw.rect(screen, COLOR_CHECKBOX_FILL, self.rect.inflate(-4, -4))
        label_surface = FONT.render(self.label, True, (0, 0, 0))
        screen.blit(label_surface, (self.rect.x + 30, self.rect.y - 2))

    def getValue(self):
        return self.checked


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_BUTTON, self.rect)
        txt_surf = FONT.render(self.text, True, (0, 0, 0))
        screen.blit(txt_surf, (self.rect.x + 10, self.rect.y + 8))

    def isClicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
