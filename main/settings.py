import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 1440, 900
SIDEBAR_WIDTH = 350

# Font
MATHS_FONT = pygame.font.Font("main/STIXTwoText-Italic.otf", 30)
UI_FONT = pygame.font.SysFont("Arial", 20)

SUPERSCRIPT_MAP = {
    # Numbers
    "0": "⁰", "1": "¹", "2": "²", "3": "³",
    "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷",
    "8": "⁸", "9": "⁹",
    
    # Operators / symbols
    "+": "⁺", "-": "⁻", "=": "⁼",
    "(": "⁽", ")": "⁾",
    
    # Lowercase letters
    "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ",
    "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ⁱ", "j": "ʲ",
    "k": "ᵏ", "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ",
    "p": "ᵖ", "r": "ʳ", "s": "ˢ", "t": "ᵗ", "u": "ᵘ",
    "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ",

    # Uppercase letters
    "A": "ᴬ", "B": "ᴮ", "D": "ᴰ", "E": "ᴱ", "G": "ᴳ",
    "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ",
    "M": "ᴹ", "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "R": "ᴿ",
    "T": "ᵀ", "U": "ᵁ", "V": "ⱽ", "W": "ᵂ"
}

# colours
COLOUR_INACTIVE = pygame.Color('black')
COLOUR_BUTTON = pygame.Color('gray60')
COLOUR_CHECKBOX_BORDER = pygame.Color('black')
COLOUR_CHECKBOX_FILL = pygame.Color('green')
COLOUR_FAIL = pygame.Color('red')

# Backgrounds
COLOUR_BACKGROUND = (255, 255, 255)
COLOUR_SIDEBAR = (230, 230, 230)

# Frame rate
FPS = 60
