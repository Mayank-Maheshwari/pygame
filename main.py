import pygame
from random import shuffle

black = (0, 0, 0)
white = (255, 255, 255)

row_count = 4
column_count = 4
square_side = 150

total_no_block = column_count * row_count

frame_height = column_count * 200
frame_width = row_count*200+200

pygame.init()
display = pygame.display.set_mode((frame_width, frame_height))
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(x, y, height, width, color, light_color, text, size, action=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(display, light_color, (x, y, width, height))
        pygame.draw.rect(display, color, (x, y, width, height), 2)
        if click[0] == 1:
            if action is not None:
                action()
    else:
        pygame.draw.rect(display, color, (x, y, width, height))
    message_display(text, x + width / 2, y + height / 2, font_size=size)


def message_display(text, x, y, font_size):
    largeText = pygame.font.Font('freesansbold.ttf', font_size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    display.blit(TextSurf, TextRect)


def game_quit():
    pygame.quit()
    quit()


def start():
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(white)
        message_display("Welcome", 400, 100, 100)
        message_display("To", 400, 200, 100)
        message_display("8-Puzzle", 400, 300, 100)

        button(frame_width * 0.2, frame_height * .8, 50, 150, (0, 200, 200), (0, 255, 255), "Start", 30, "main")
        button(frame_width * 0.7, frame_height * .8, 50, 150, (200, 200, 0), (255, 255, 0), "Quit", 30, "game_quit")

        pygame.display.update()
        clock.tick(60)


class Square:
    zero_square = None

    def __init__(self, x, y, side, message, ):
        self.x = x
        self.y = y
        self.side = side
        self.message = message
        if self.message == '0':
            Square.zero_square = self

    def draw_square(self, color, light_color, size=50):
        if self == Square.zero_square:
            return
        pygame.draw.rect(display, light_color, (self.x, self.y, self.side, self.side))
        pygame.draw.rect(display, color, (self.x, self.y, self.side, self.side), 1)
        if self.message is not None:
            message_display(self.message, self.x + self.side / 2, self.y + self.side / 2, font_size=size)


class Problem:
    problem = [i for i in range(total_no_block)]

    shuffle(problem)

    @staticmethod
    def create_problem():
        Problem.problem.clear()
        for slide in Puzzel.slides:
            Problem.problem.append(int(slide.message))
        Problem.print_problem()
        Problem.check_goal()

    @staticmethod
    def print_problem():
        print(Problem.problem)

    @staticmethod
    def check_goal():
        if sorted(Problem.problem) == Problem.problem:
            print("goal")


class Puzzel:
    slides = [Square(frame_width * 0.15 + 5 + ((i % row_count) * square_side), frame_height * 0.05 + 5 + (int(i / column_count) * square_side), square_side-5,
                     str(Problem.problem[i])) for i in range(total_no_block)]

    x_coodinates = [frame_width*0.15+5+i*square_side for i in range(row_count)]
    y_coodinates = [frame_height*0.05+5+i*square_side for i in range(column_count)]
    @staticmethod
    def paint():
        Square(frame_width * 0.15, frame_height * 0.05, row_count*square_side + 5, None).draw_square(black, white)
        for i in Puzzel.slides:
            i.draw_square(black, white)

    @staticmethod
    def move_up():
        if Square.zero_square.y == frame_height*0.05+(column_count-1)*square_side+5:
            return
        else:
            side = Puzzel.find_Square_below(Square.zero_square.y, Square.zero_square.x)
            if side is None:
                return
            side.x, Square.zero_square.x = Square.zero_square.x, side.x
            side.y, Square.zero_square.y = Square.zero_square.y, side.y
            a, b = Puzzel.slides.index(side), Puzzel.slides.index(Square.zero_square)
            Puzzel.slides[a], Puzzel.slides[b] = Puzzel.slides[b], Puzzel.slides[a]
            Problem.create_problem()

    @staticmethod
    def move_down():
        if Square.zero_square.y == frame_height*0.05+5:
            return
        else:
            side = Puzzel.find_Square_above(Square.zero_square.y, Square.zero_square.x)
            if side is None:
                return
            side.x, Square.zero_square.x = Square.zero_square.x, side.x
            side.y, Square.zero_square.y = Square.zero_square.y, side.y
            a, b = Puzzel.slides.index(side), Puzzel.slides.index(Square.zero_square)
            Puzzel.slides[a], Puzzel.slides[b] = Puzzel.slides[b], Puzzel.slides[a]

            Problem.create_problem()

    @staticmethod
    def move_left():
        if Square.zero_square.x == frame_width*1.15+(row_count-1)*square_side+5:
            return
        else:
            side = Puzzel.find_square_right(Square.zero_square.y, Square.zero_square.x)
            if side is None:
                return
            side.x, Square.zero_square.x = Square.zero_square.x, side.x
            side.y, Square.zero_square.y = Square.zero_square.y, side.y
            a, b = Puzzel.slides.index(side), Puzzel.slides.index(Square.zero_square)
            Puzzel.slides[a], Puzzel.slides[b] = Puzzel.slides[b], Puzzel.slides[a]
            Problem.create_problem()

    @staticmethod
    def move_right():
        if Square.zero_square.x == frame_width*1.15+5:
            return
        else:
            side = Puzzel.find_square_left(Square.zero_square.y, Square.zero_square.x)
            if side is None:
                return
            side.x, Square.zero_square.x = Square.zero_square.x, side.x
            side.y, Square.zero_square.y = Square.zero_square.y, side.y
            a, b = Puzzel.slides.index(side), Puzzel.slides.index(Square.zero_square)
            Puzzel.slides[a], Puzzel.slides[b] = Puzzel.slides[b], Puzzel.slides[a]
            Problem.create_problem()

    @staticmethod
    def find_Square_below(y, x):
        i = Puzzel.y_coodinates.index(y)
        found_y = Puzzel.y_coodinates[i + 1]
        for slide in Puzzel.slides:
            if x == slide.x:
                if slide.y ==found_y:
                    return slide
    @staticmethod
    def find_Square_above(y, x):
        i = Puzzel.y_coodinates.index(y)
        found_y = Puzzel.y_coodinates[i - 1]

        for slide in Puzzel.slides:
            if x == slide.x:
                if slide.y ==found_y:
                    return slide
    @staticmethod
    def find_square_right(y, x):
        i = Puzzel.x_coodinates.index(x)
        found_x = Puzzel.x_coodinates[i+1]
        for slide in Puzzel.slides:
            if y == slide.y:
                if slide.x == found_x:
                        return slide

    @staticmethod
    def find_square_left(y, x):
        i = Puzzel.x_coodinates.index(x)
        found_x = Puzzel.x_coodinates[i-1]
        for slide in Puzzel.slides:
            if y == slide.y:
                if slide.x == found_x:
                        return slide

def main():
    pygame.display.set_caption('8-Puzzle')
    Problem.print_problem()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("left")
                    Puzzel.move_left()
                if event.key == pygame.K_RIGHT:
                    print("right")
                    Puzzel.move_right()
                if event.key == pygame.K_UP:
                    print("up")
                    Puzzel.move_up()
                if event.key == pygame.K_DOWN:
                    print("down")
                    Puzzel.move_down()
        display.fill(white)
        Puzzel.paint()
        #button(100,530, 60, 175, (200, 200, 200), (225, 225, 225), "New Game", 30)
        pygame.display.update()


if __name__ == "__main__":
    main()
