import pygame
from typing import List, Tuple, Dict, Set

# Initialize Pygame
pygame.init()

# Constants
TITLE: str = "Big Isle!!!"
TILE_SIZE: int = 100
GRID_SIZE: int = 8
GRID_PIXEL_SIZE: int = TILE_SIZE * GRID_SIZE
UI_HEIGHT: int = 100
OUTLINE_BUFFER: int = 50
WINDOW_WIDTH: int = GRID_PIXEL_SIZE + OUTLINE_BUFFER
WINDOW_HEIGHT: int = GRID_PIXEL_SIZE + OUTLINE_BUFFER + UI_HEIGHT
WINDOW_SIZE: Tuple[int, int] = (WINDOW_WIDTH, WINDOW_HEIGHT)

# OFFSET USED TO CENTER THE GRID IN THE WINDOW
OFFSET_X: int = (WINDOW_WIDTH - GRID_PIXEL_SIZE) // 2
OFFSET_Y: int = (WINDOW_HEIGHT - GRID_PIXEL_SIZE) // 2

WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
BLACK: Tuple[int, int, int] = (0, 0, 0)

RED_PLAYER: str = 'R'
BLACK_PLAYER: str = 'B'

blue_tiles: int = 32
red_tiles: int = 32

# Grid layout
GRID: List[List[str]] = [
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ',' ', ' ', ' ', ' ']
]


# Create window
screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)

# Grid surface (logical grid space)
grid_surface = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE))
grid_rect = grid_surface.get_rect(
    center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT - UI_HEIGHT) // 2)
)

pygame.display.set_caption(TITLE)

# Game state
current_player: str = RED_PLAYER
tiles_left: Dict[str, int] = {RED_PLAYER: red_tiles, BLACK_PLAYER: blue_tiles}

running: bool = True
clock: pygame.time.Clock = pygame.time.Clock()
font: pygame.font.Font = pygame.font.SysFont(None, 32)


# Contiguous block calculation
def largest_contiguous(grid: List[List[str]], color: str) -> int:
    visited: Set[Tuple[int, int]] = set()
    max_size: int = 0

    def dfs(r: int, c: int) -> int:
        stack: List[Tuple[int, int]] = [(r, c)]
        size: int = 0

        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            size += 1

            neighbors: List[Tuple[int, int]] = [(1,0),(-1,0),(0,1),(0,-1)]
            for dr, dc in neighbors:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] == color:
                    stack.append((nr, nc))

        return size

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == color and (r, c) not in visited:
                max_size = max(max_size, dfs(r, c))

    return max_size


# ===================== GAME LOOP =======================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            
            if grid_rect.collidepoint(mx, my):
                gx = mx - grid_rect.x
                gy = my - grid_rect.y

                col = gx // TILE_SIZE
                row = gy // TILE_SIZE
                
                # Location for other game logic in event loop.
                if GRID[row][col] == ' ' and tiles_left[current_player] > 0:
                    GRID[row][col] = current_player
                    tiles_left[current_player] -= 1
                    current_player = BLACK_PLAYER if current_player == RED_PLAYER else RED_PLAYER
                    
    screen.fill(WHITE)
    grid_surface.fill(WHITE)

    # Draw grid to grid_surface
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            pygame.draw.rect(
                grid_surface,
                BLACK,
                (x, y, TILE_SIZE, TILE_SIZE),
                2
            )

            tile = GRID[r][c]
            if tile == RED_PLAYER:
                pygame.draw.rect(
                    grid_surface,
                    RED,
                    (x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
                )
            elif tile == BLACK_PLAYER:
                pygame.draw.rect(
                    grid_surface,
                    BLACK,
                    (x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)
                )
                
    screen.blit(grid_surface, grid_rect)

    red_size = largest_contiguous(GRID, RED_PLAYER)
    black_size = largest_contiguous(GRID, BLACK_PLAYER)

    turn_text = font.render(
        f"Turn: {'Red' if current_player == RED_PLAYER else 'Black'}", True, BLACK
    )
    score_text = font.render(f"R:{red_size}  B:{black_size}", True, BLACK)
    tiles_text = font.render(
        f"Tiles R:{tiles_left[RED_PLAYER]} B:{tiles_left[BLACK_PLAYER]}", True, BLACK
    )

    ui_y = grid_rect.bottom + 10

    screen.blit(turn_text, turn_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y)))
    screen.blit(score_text, score_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y + 30)))
    screen.blit(tiles_text, tiles_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y + 60)))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
