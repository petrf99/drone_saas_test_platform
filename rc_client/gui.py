import pygame

from tech_utils.logger import init_logger
logger = init_logger("RCClientGUI")

from rc_client.config import *

def pygame_init(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title="RC Controller"):
    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
    except pygame.error as e:
        logger.error(f"[ERROR] Pygame init failed: {e}", exc_info=True)
        raise

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    return screen, clock


pygame.font.init()
font = pygame.font.SysFont("Arial", FONT_SIZE)

controller_options = ["keyboard", "keyboard_mouse", "gamepad", "radio"]

def draw_text_input(screen, label, value, rect, selected):
    pygame.draw.rect(screen, SELECTED_BG if selected else INPUT_BG, rect)
    text_surface = font.render(f"{label}: {value}", True, FONT_COLOR)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))

def draw_dropdown(screen, label, options, selected_index, rect, active):
    pygame.draw.rect(screen, SELECTED_BG if active else INPUT_BG, rect)
    text_surface = font.render(f"{label}: {options[selected_index]}", True, FONT_COLOR)
    screen.blit(text_surface, (rect.x + 5, rect.y + 5))

def draw_button(screen, text, rect, hovered):
    pygame.draw.rect(screen, BUTTON_HOVER if hovered else BUTTON_COLOR, rect)
    text_surface = font.render(text, True, FONT_COLOR)
    screen.blit(text_surface, (rect.x + 10, rect.y + 5))

def start_screen(screen, clock):
    username = ""
    password = ""
    selected_input = "username"
    controller_index = 0
    dropdown_active = False

    input_username = pygame.Rect(100, 100, 400, 40)
    input_password = pygame.Rect(100, 160, 400, 40)
    dropdown_rect = pygame.Rect(100, 220, 400, 40)
    start_button = pygame.Rect(100, 300, 200, 40)

    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))

        # Draw UI
        draw_text_input(screen, "Username", username, input_username, selected_input == "username")
        draw_text_input(screen, "Password", '*' * len(password), input_password, selected_input == "password")
        draw_dropdown(screen, "Controller", controller_options, controller_index, dropdown_rect, dropdown_active)

        mouse_pos = pygame.mouse.get_pos()
        hovered = start_button.collidepoint(mouse_pos)
        draw_button(screen, "Start Flight", start_button, hovered)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_username.collidepoint(event.pos):
                    selected_input = "username"
                elif input_password.collidepoint(event.pos):
                    selected_input = "password"
                elif dropdown_rect.collidepoint(event.pos):
                    dropdown_active = not dropdown_active
                elif start_button.collidepoint(event.pos):
                    return username.strip(), password.strip(), controller_options[controller_index]

            elif event.type == pygame.KEYDOWN:
                if selected_input in ["username", "password"]:
                    if event.key == pygame.K_BACKSPACE:
                        if selected_input == "username":
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    elif event.key == pygame.K_TAB:
                        selected_input = "password" if selected_input == "username" else "username"
                    elif event.key == pygame.K_RETURN:
                        return username.strip(), password.strip(), controller_options[controller_index]
                    else:
                        char = event.unicode
                        if selected_input == "username":
                            username += char
                        else:
                            password += char
                elif dropdown_active:
                    if event.key == pygame.K_DOWN:
                        controller_index = (controller_index + 1) % len(controller_options)
                    elif event.key == pygame.K_UP:
                        controller_index = (controller_index - 1) % len(controller_options)
