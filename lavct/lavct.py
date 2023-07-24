import sys
import pygame
import csv
import math
import signal


DEFAULT_SCREEN_WIDTH = 720
DEFAULT_SCREEN_HEIGHT = 350

WIDTH_OFFSET = 25
HEIGHT_OFFSET = 15

# Bandwidth = 16.257 MHz -> pixel clock ~= 61.5 ns

pixel_period = 62.5

skip_lines = 0

back_porch = 1531

# Pixel size
pixel_size_x = 1
pixel_size_y = 1

# RGB values
color_r = 170
color_g = 170
color_b = 170


# Function to draw a pixel
def draw_pixel(screen, x, y, color):
    pygame.draw.rect(screen, color, (x, y, pixel_size_x, pixel_size_y))


# parse csv file and refresh screen pixels
def refresh_scren(screen, screen_buffer):
    video_prev = 0
    video_high_start = 0
    video_high_end = 0
    hsync_prev = 0
    line_number = 0

    for row in screen_buffer:
        # Time [ns],HSYNC,VSYNC,INTENSITY,VIDEO
        t = int(row[0])
        hsync = int(row[1])
        vsync = int(row[2])
        intensity = int(row[3])
        video = int(row[4])

        # reset line number if vsync is low
        if vsync == 0:
            line_number = 0
            continue

        # hsync transition (high -> low)
        if hsync == 0 and hsync_prev == 1:
            hsync_prev = 0
            line_number += 1 + skip_lines
            line_start_time = t + back_porch
            continue

        # hsync transition (low -> high)
        if hsync == 1 and hsync_prev == 0:
            hsync_prev = 1
            continue

        # video transition (low -> high)
        if video == 1 and video_prev == 0:
            video_prev = 1
            video_high_start = t

        # video transition (high -> low)
        if video == 0 and video_prev == 1:
            video_prev = 0
            video_high_end = t

            pixel_count = round((video_high_end - video_high_start) / pixel_period)
            x_pos = (
                round((video_high_start - line_start_time) / pixel_period)
                + WIDTH_OFFSET
            )

            for _ in range(0, pixel_count):
                draw_pixel(screen, x_pos, line_number, (color_r, color_g, color_b))
                x_pos = x_pos + 1


def parse_csv(filename):
    screen_buffer = []
    # Read csv
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for idx, row in enumerate(reader):
            # skip header
            if idx == 0:
                continue
            screen_buffer.append(row)
    return screen_buffer


def clear_secreen(screen):
    screen.fill((0, 0, 0))
    pygame.display.flip()


def signal_handler(sig, frame):
    print("\nProcess terminated by user")
    pygame.quit()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = sys.argv[1:]

    global pixel_period, back_porch, skip_lines
    global pixel_size_x, pixel_size_y
    global color_r, color_g, color_b

    if len(args) < 1:
        print("\nYou must specify a csv file to process")
        sys.exit(0)

    filename = args[0]

    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Logic Analyzer Video Capture Tool")

    # Create the window
    flags = pygame.RESIZABLE
    screen = pygame.display.set_mode(
        (DEFAULT_SCREEN_WIDTH + WIDTH_OFFSET, DEFAULT_SCREEN_HEIGHT + HEIGHT_OFFSET),
        flags,
    )
    clock = pygame.time.Clock()

    # Parse file and create screen_buffer
    screen_buffer = parse_csv(filename)

    # Main loop
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Use `a` and `d` to change pixel_period
            if keys[pygame.K_d]:
                clear_secreen(screen)
                pixel_period = pixel_period + 0.1
                print(f"pixel_period: {pixel_period}")
                refresh_scren(screen, screen_buffer)
            if keys[pygame.K_a]:
                clear_secreen(screen)
                pixel_period = pixel_period - 0.1
                print(f"pixel_period: {pixel_period}")
                refresh_scren(screen, screen_buffer)
            # Use `q` and `e` to change back_porch
            if keys[pygame.K_e]:
                clear_secreen(screen)
                back_porch = back_porch + 1
                print(f"back_porch: {back_porch}")
                refresh_scren(screen, screen_buffer)
            if keys[pygame.K_q]:
                clear_secreen(screen)
                back_porch = back_porch - 1
                print(f"back_porch: {back_porch}")
                refresh_scren(screen, screen_buffer)
            # Use `1`, `2` and `3` to change resolution
            if keys[pygame.K_1]:
                clear_secreen(screen)
                pixel_size_y = 1
                skip_lines = 0
                print(f"720x350 - default")
                screen = pygame.display.set_mode(
                    (
                        DEFAULT_SCREEN_WIDTH + WIDTH_OFFSET,
                        DEFAULT_SCREEN_HEIGHT + HEIGHT_OFFSET,
                    ),
                    flags,
                )
            if keys[pygame.K_2]:
                clear_secreen(screen)
                pixel_size_y = 1
                skip_lines = 1
                print(f"720x700 - scanlines emulation")
                screen = pygame.display.set_mode(
                    (
                        DEFAULT_SCREEN_WIDTH + WIDTH_OFFSET,
                        DEFAULT_SCREEN_HEIGHT * 2 + HEIGHT_OFFSET,
                    ),
                    flags,
                )
            if keys[pygame.K_3]:
                clear_secreen(screen)
                pixel_size_y = 2
                skip_lines = 1
                print(f"720x700 - pixel_size_y = 2")
                screen = pygame.display.set_mode(
                    (
                        DEFAULT_SCREEN_WIDTH + WIDTH_OFFSET,
                        DEFAULT_SCREEN_HEIGHT * 2 + HEIGHT_OFFSET,
                    ),
                    flags,
                )
            if keys[pygame.K_8]:
                clear_secreen(screen)
                color_r = 170
                color_g = 91
                color_b = 0
                print(f"Color: amber")

            if keys[pygame.K_9]:
                clear_secreen(screen)
                color_r = 0
                color_g = 170
                color_b = 0
                print(f"Color: green")
            if keys[pygame.K_0]:
                clear_secreen(screen)
                color_r = 170
                color_g = 170
                color_b = 170
                print(f"Color: white")

        clock.tick(60)  # Limit to 60 frames per second
        refresh_scren(screen, screen_buffer)
        pygame.display.flip()


if __name__ == "__main__":
    main()
