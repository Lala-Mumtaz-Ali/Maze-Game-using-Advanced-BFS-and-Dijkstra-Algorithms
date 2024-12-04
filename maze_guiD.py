import sys
import pygame
from maze_solverD import dijkstra  # Importing the Dijkstra function

# Box class for the grid elements
class box():
    def __init__(self, x, y, width, height, text, color, weight=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.weight = weight  # Add weight attribute

    def getPos(self):
        return (self.x, self.y)

    def getText(self):
        return self.text

    def setText(self, newText):
        self.text = newText

    def setWeight(self, weight):
        self.weight = weight  # Method to set weight

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width, self.height))
        if not(self.text == " " or self.text == "#" or self.text == "S" or self.text == "E"):
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(str(self.text), 1, (0, 0, 0))
            canvas.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))

    def hover(self, pos):
        if (pos[0] > self.x and pos[0] < self.x + self.width):
            if (pos[1] > self.y and pos[1] < self.y + self.height):
                return True
        return False

# Create grid of box objects
def setup(weights=None):
    grid = [[] for _ in range(7)]  # Keep the grid size as 7x7
    box_size = 50  # Size of each box (both width and height)
    margin = 5     # Margin between boxes
    grid_width = (box_size + margin) * 7 - margin  # Total grid width
    grid_height = (box_size + margin) * 7 - margin  # Total grid height

    start_x = (WIDTH - grid_width) // 2  # Center the grid horizontally
    start_y = (HEIGHT - grid_height) // 2  # Center the grid vertically

    for row in range(len(grid)):
        for col in range(len(grid)):
            # Set weight from the weights list or default to 1
            weight = weights[row][col] if weights else 1
            gridBox = box(
                start_x + col * (box_size + margin), 
                start_y + row * (box_size + margin), 
                box_size, 
                box_size, 
                " ", 
                (255, 255, 255),
                weight
            )
            grid[row].append(gridBox)
    return grid

def redraw(grid, canvas, path_text):
    canvas.fill(BLACK)
    
    for row in grid:
        for col in row:
            col.draw(canvas)

    font = pygame.font.SysFont('comicsans', 25)
    path_surface = font.render(f"Shortest Path: {path_text}", True, WHITE)
    canvas.blit(path_surface, ((WIDTH - path_surface.get_width()) // 2, 10))

def debugPrintGrid(grid):
    print("Current Grid Weights:")
    for row in grid:
        print([box.weight for box in row])

# Grid to Python nested lists
def getMazeArray(grid):
    mazeArray = []
    for row in grid:
        row_list = []
        for box in row:
            row_list.append(box.weight)  # Get the weight of the box, not the box itself
        mazeArray.append(row_list)
    return mazeArray

def paintPath(grid, startX, startY, path):
    currentCol = startX
    currentRow = startY
    pathArray = list(path)
    
    for direction in range(len(path)-1):
        if pathArray[direction] == "U":
            currentRow -= 1
        elif pathArray[direction] == "D":
            currentRow += 1
        elif pathArray[direction] == "L":
            currentCol -= 1
        elif pathArray[direction] == "R":
            currentCol += 1
        
        grid[currentRow][currentCol].color = (0, 0, 255)

if __name__ == '__main__':
    pygame.init()

    # Color, size parameters
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WIDTH = 600  
    HEIGHT = 600  

    START = None
    END = None

    STARTROW = None
    STARTCOL = None

    path_text = ""

    CANVAS = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze')
    CANVAS.fill(BLACK)

    # Define predefined weights
    PREDEFINED_WEIGHTS = [
        [1, 1, 1, 2, 1, 3, 1],
        [1, 3, 2, 1, 1, 2, 1],
        [1, 1, 1, 1, 2, 1, 1],
        [3, 2, 1, 1, 1, 1, 3],
        [1, 1, 1, 2, 1, 3, 1],
        [1, 2, 1, 1, 1, 1, 1],
        [1, 1, 3, 2, 1, 1, 1],
    ]

    GRID = setup(PREDEFINED_WEIGHTS)
    SOLVEBUTTON = box((WIDTH - 200) // 2, HEIGHT - 100, 200, 40, 'Find', WHITE)
    RESETBUTTON = box((WIDTH - 200) // 2, HEIGHT - 50, 200, 40, 'Reset', WHITE)

    while True:
        redraw(GRID, CANVAS, path_text)
        SOLVEBUTTON.draw(CANVAS)
        RESETBUTTON.draw(CANVAS)

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SOLVEBUTTON.hover(pos):
                    if START and END:
                        print("Finding shortest path...")

                        debugPrintGrid(GRID)

                        path, weight = dijkstra(GRID)
                        if STARTCOL is not None and STARTROW is not None:
                            paintPath(GRID, STARTCOL, STARTROW, path)
                            print(f"Shortest path found with weight: {weight}")
                            path_text = f"{path} (Weight: {weight})"
                        else:
                            print("Start point not set.")
                    else:
                        print("Missing start or end.")

                if RESETBUTTON.hover(pos):
                    GRID = setup(PREDEFINED_WEIGHTS)
                    START = None
                    END = None
                    STARTROW = None
                    STARTCOL = None
                    path_text = "None"
                    print("Resetting grid.")


                for row in GRID:
                    for col in row:
                        if col.hover(pos):
                            if col.getText() == " ":
                                col.setText("#")
                                col.color = BLACK
                            else:
                                col.setText(" ")
                                col.color = WHITE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    for row in range(len(GRID)):
                        for col in range(len(GRID[row])):
                            if GRID[row][col].hover(pos):
                                GRID[row][col].setText("S")
                                GRID[row][col].color = GREEN
                                START = GRID[row][col]
                                STARTROW, STARTCOL = row, col

                if event.key == pygame.K_e:
                    for row in range(len(GRID)):
                        for col in range(len(GRID[row])):
                            if GRID[row][col].hover(pos):
                                GRID[row][col].setText("E")
                                GRID[row][col].color = RED
                                END = GRID[row][col]
        pygame.display.update()
