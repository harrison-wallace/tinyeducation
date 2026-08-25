#!/usr/bin/env python3
"""
Phonics Keyboard Game - A simple alphabet/phonics learning game for young children.
Run with: python3 game.py --help
"""

import argparse
import os
import sys
import warnings

# Suppress the harmless AVX2 performance warning from some pygame builds
warnings.filterwarnings("ignore", message=".*avx2.*", category=RuntimeWarning)

# Determine the directory this script lives in so we can find assets reliably
# even when the game is run from the repo root or elsewhere.
GAME_DIR = os.path.dirname(os.path.abspath(__file__))

# Hide pygame's community message for a clean startup (must be before import pygame)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Asset paths (always absolute, works no matter where you run from)
FONT_PATH = os.path.join(GAME_DIR, "SchoolYard-Regular.otf")
CORRECT_WAV_PATH = os.path.join(GAME_DIR, "correct.wav")
SOUNDS_DIR = os.path.join(GAME_DIR, "phonic-sounds")

# --------------------------- CLI ARGUMENTS ---------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Phonics Keyboard Game - Help kids learn letters and keyboard skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Controls:
  SPACE / ENTER / Click "Ready"   Start or retry the game
  ESC                             Quit at any time
  Matching letter key             Advance when the letter is shown

Examples:
  python3 game.py                 # Large windowed (auto-sized to your screen)
  python3 game.py -f              # Fullscreen
  python3 game.py --width 1920 --height 1080   # Force exact size
        """.strip()
    )
    parser.add_argument(
        "-f", "--fullscreen", action="store_true",
        help="Run in fullscreen mode (can be disorienting on Linux)"
    )
    parser.add_argument(
        "--width", type=int, default=None,
        help="Window width when not in fullscreen (auto-detected large size by default)"
    )
    parser.add_argument(
        "--height", type=int, default=None,
        help="Window height when not in fullscreen (auto-detected large size by default)"
    )
    return parser.parse_args()

args = parse_args()

# --------------------------- PYGAME INIT ---------------------------

import pygame  # type: ignore  # noqa: E402

print("Phonics Keyboard Game")
print("-" * 40)
print("   Initializing pygame...")

pygame.init()
pygame.mixer.init()
print("   Pygame ready (SDL", pygame.version.SDL, ")")

# Create window
if args.fullscreen:
    print("   Opening in FULLSCREEN mode...")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    # Smart default: use a large window based on actual desktop size
    # (avoids tiny 1280x720 default and problems with exact screen-size windowed on Linux)
    if args.width is None or args.height is None:
        info = pygame.display.Info()
        dw, dh = info.current_w, info.current_h
        # Choose a large window size that still feels immersive but leaves room
        # for window borders + taskbar/panel (common complaint on 1080p Linux)
        target_w = min(int(dw * 0.96), dw - 60, 1920)
        target_h = min(int(dh * 0.92), dh - 80, 1080)
        args.width = max(800, target_w)
        args.height = max(600, target_h)

    print(f"   Opening windowed mode at {args.width}x{args.height}...")
    screen = pygame.display.set_mode((args.width, args.height))

width, height = screen.get_size()

if not args.fullscreen and (width, height) != (args.width, args.height):
    print(f"   (Window manager adjusted actual size to {width}x{height})")

pygame.display.set_caption("Phonics Keyboard Game")

# --------------------------- LOAD ASSETS ---------------------------

print("   Loading font...")
title_font = pygame.font.Font(FONT_PATH, 150)
game_font = pygame.font.Font(FONT_PATH, 1200)
menu_font = pygame.font.Font(FONT_PATH, 100)
countdown_font = pygame.font.Font(FONT_PATH, 300)

print("   Loading sounds (26 letter sounds + feedback)...")
correct_sound = pygame.mixer.Sound(CORRECT_WAV_PATH)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_sounds = {}
missing = []
for letter in letters:
    path = os.path.join(SOUNDS_DIR, f"alphasounds-{letter.lower()}.mp3")
    try:
        alphabet_sounds[letter.lower()] = pygame.mixer.Sound(path)
    except Exception as e:
        missing.append(letter)
        print(f"   WARNING: Could not load sound for {letter}: {e}")

if missing:
    print(f"   Loaded {len(alphabet_sounds)}/26 sounds. Missing: {''.join(missing)}")
else:
    print(f"   All {len(alphabet_sounds)} sounds loaded successfully.")

print("   Ready!\n")

def animate_bounce(upper, lower):
    for i in range(10):  # 10 frames of bounce animation
        offset = (i % 5) * 20 if i < 5 else (10 - i % 5) * 20  # Up and down bounce
        combined_text = f"{upper} {lower}"
        text = game_font.render(combined_text, True, (0, 0, 255))
        screen.fill((255, 255, 255))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - offset))
        pygame.display.flip()
        pygame.time.wait(50)  # 50ms per frame

def countdown():
    for text in ["3", "2", "1", "Go!"]:
        screen.fill((255, 255, 255))
        countdown_text = countdown_font.render(text, True, (0, 0, 0))
        screen.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # 1 second per number

def draw_gradient_background(start_color, end_color):
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

while True:  # Main loop for retries / returning to menu
    # Start menu with gradient background
    draw_gradient_background((135, 206, 235), (255, 255, 255))  # Light blue to white

    title_text = title_font.render("Phonics Game", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 180))
    screen.blit(title_text, title_rect)

    # Subtitle / instructions
    subtitle = menu_font.render("Learn your letters!", True, (50, 50, 50))
    subtitle_rect = subtitle.get_rect(center=(width // 2, height // 2 - 80))
    screen.blit(subtitle, subtitle_rect)

    # Draw "Ready" button
    ready_text = menu_font.render("Ready", True, (0, 0, 0))
    ready_rect = ready_text.get_rect(center=(width // 2, height // 2 + 30))
    ready_button_rect = pygame.Rect(ready_rect.left - 20, ready_rect.top - 20, ready_rect.width + 40, ready_rect.height + 40)
    pygame.draw.rect(screen, (0, 255, 0), ready_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), ready_button_rect, 2)
    screen.blit(ready_text, ready_rect)

    # Clear instructions for keyboard users
    instr1 = pygame.font.Font(FONT_PATH, 36).render("Click Ready  or  press SPACE / ENTER", True, (30, 30, 30))
    instr1_rect = instr1.get_rect(center=(width // 2, height // 2 + 130))
    screen.blit(instr1, instr1_rect)

    instr2 = pygame.font.Font(FONT_PATH, 32).render("Press ESC anytime to quit", True, (80, 80, 80))
    instr2_rect = instr2.get_rect(center=(width // 2, height // 2 + 175))
    screen.blit(instr2, instr2_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                    waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ready_button_rect.collidepoint(event.pos):
                    waiting = False
    
    # Game play
    current_index = 0
    times = []
    
    while current_index < len(letters):
        current_letter_upper = letters[current_index]
        current_letter_lower = current_letter_upper.lower()
        current_sound = alphabet_sounds[current_letter_lower]
        sound_length_ms = current_sound.get_length() * 1000
        
        start_time = pygame.time.get_ticks()
        
        screen.fill((255, 255, 255))
        combined_text = f"{current_letter_upper} {current_letter_lower}"
        text = game_font.render(combined_text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()
        
        current_sound.play()
        last_play_time = start_time
        
        correct_pressed = False
        while not correct_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Allow window close via X button
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()  # Allow exit with ESC key
                    pressed_key = pygame.key.name(event.key).upper()
                    if pressed_key in letters:  # Only accept A-Z keys
                        if pressed_key == current_letter_upper:
                            correct_pressed = True
                            break
            # Check if it's time to replay the sound (after duration + 1 second)
            current_time = pygame.time.get_ticks()
            if current_time - last_play_time > sound_length_ms + 1000:
                current_sound.play()
                last_play_time = current_time
        
        end_time = pygame.time.get_ticks()
        time_taken = (end_time - start_time) / 1000
        times.append(time_taken)
        
        screen.fill((0, 255, 0))
        combined_text = f"{current_letter_upper} {current_letter_lower}"
        text = game_font.render(combined_text, True, (0, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()
        correct_sound.play()
        pygame.time.wait(3000)
        
        animate_bounce(current_letter_upper, current_letter_lower)
        
        if current_index < len(letters) - 1:
            countdown()
        
        current_index += 1
    
    # End screen with total time and average
    total_time = sum(times)
    avg_time = total_time / len(times) if times else 0

    draw_gradient_background((135, 206, 235), (255, 255, 255))

    title = menu_font.render("Great job!", True, (0, 0, 0))
    title_rect = title.get_rect(center=(width // 2, height // 2 - 200))
    screen.blit(title, title_rect)

    total_text = menu_font.render(f"Total Time: {total_time:.2f}s", True, (0, 0, 0))
    avg_text = menu_font.render(f"Average: {avg_time:.2f}s per letter", True, (0, 0, 0))
    screen.blit(total_text, (width // 2 - total_text.get_width() // 2, height // 2 - 100))
    screen.blit(avg_text, (width // 2 - avg_text.get_width() // 2, height // 2 - 40))

    # Draw "Retry" button (left)
    retry_text = menu_font.render("Retry", True, (0, 0, 0))
    retry_rect = retry_text.get_rect(center=(width // 2 - 180, height // 2 + 100))
    retry_button_rect = pygame.Rect(retry_rect.left - 20, retry_rect.top - 20, retry_rect.width + 40, retry_rect.height + 40)
    pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), retry_button_rect, 2)
    screen.blit(retry_text, retry_rect)

    # Draw "Exit" button (right)
    exit_text = menu_font.render("Exit", True, (0, 0, 0))
    exit_rect = exit_text.get_rect(center=(width // 2 + 180, height // 2 + 100))
    exit_button_rect = pygame.Rect(exit_rect.left - 20, exit_rect.top - 20, exit_rect.width + 40, exit_rect.height + 40)
    pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), exit_button_rect, 2)
    screen.blit(exit_text, exit_rect)

    # Keyboard hint
    hint = pygame.font.Font(FONT_PATH, 32).render("SPACE or click Retry   -   ESC to quit", True, (60, 60, 60))
    hint_rect = hint.get_rect(center=(width // 2, height // 2 + 190))
    screen.blit(hint, hint_rect)

    pygame.display.flip()

    ended = True
    while ended:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                    ended = False  # retry
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    ended = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()