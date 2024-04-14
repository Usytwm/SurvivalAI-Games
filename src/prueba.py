import pygame
import sys


def draw_board(screen, matrix, cell_size):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(
                j * cell_size, i * cell_size, cell_size, cell_size
            )  # tamano de la celda
            color = (
                (0, 255, 0) if matrix[i][j] != 0 else (255, 255, 255)
            )  # color de la celda
            pygame.draw.rect(screen, color, rect)  # dibija la celda
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # agrega un border a la celda


def main():
    pygame.init()

    # Define el tamaño de cada celda
    cell_size = 50

    # Matriz de ejemplo, modifica según tus necesidades
    matrix = [
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
    ]

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    # Ajusta el tamaño de la ventana basado en el tamaño de la matriz
    size = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tablero de Matriz")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Fondo negro
        draw_board(screen, matrix, cell_size)

        pygame.display.flip()
        clock.tick(60)  # 60 frames por segundo


if __name__ == "__main__":
    main()
