import pygame


class DropdownMenu:
    def __init__(self, x, y, width, height, font, main_text, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.main_text = main_text
        self.options = options
        self.selected_option = None
        self.show_options = False
        self.option_rects = []

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
        text_surface = self.font.render(self.main_text if self.selected_option is None else self.selected_option, True,
                                        (0, 0, 0))
        win.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        if self.show_options:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width,
                                          self.rect.height)
                self.option_rects.append(option_rect)
                pygame.draw.rect(win, (200, 200, 200), option_rect)
                option_text = self.font.render(option, True, (0, 0, 0))
                win.blit(option_text, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_options = not self.show_options
                self.option_rects = []  # Reset option rects to avoid stale positions
            elif self.show_options:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.show_options = False
                        break

    def get_selected_option(self):
        return self.selected_option
