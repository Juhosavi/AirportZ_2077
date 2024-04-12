import os
import time

def logo():
    airportz = (
        "\033[91m"
        " █████  ██ ██████  ██████   ██████  ██████  ████████     ███████ \n"
        "██   ██ ██ ██   ██ ██   ██ ██    ██ ██   ██    ██           ███\n"
        "███████ ██ ██████  ██████  ██    ██ ██████     ██          ███\n"
        "██   ██ ██ ██   ██ ██      ██    ██ ██   ██    ██         ███\n"
        "██   ██ ██ ██   ██ ██       ██████  ██   ██    ██        ███████\n"
        "\033[0m"
    )
    print(airportz)

#logo()


def plane_animation():

    # Define the screen size
    width, height = 40, 20

    # Initialize the airplane's position and speed
    x, y = 0, height // 2
    speed = 2  # Increased animation speed

    # ASCII art representation of the airplane
    airplane_shape = [
                               "    ____       _",
                               " | __\_\_o,___/ \"",
                               " ([___\_\_____-\'",
                               " |     o'        "
    ]


    # Main loop
    while True:
        # Clear the console and print a lot of empty lines
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 50)  # Add a lot of empty lines

        # Draw the airplane
        for i in range(len(airplane_shape)):
            print(" " * x + airplane_shape[i])

        # Update the airplane's position
        x += speed

        # Limit the airplane's movement within the console
        if x < 0:
            x = 0
            speed = 1  # Change direction when reached the left edge

        elif x + len(airplane_shape[0]) >= width:
            x = width - len(airplane_shape[0])
            speed = -1  # Change direction when reached the right edge

        # Check if the airplane has returned to its starting position
        if x == 0:
            print("Landed")
            time.sleep(2)
            print("\nYou are attacked by zombies!\n\n")
            time.sleep(3)
            zombie_animation()
            break

        # Pause briefly to display the animation
        time.sleep(0.1)  # Increased animation speed

# plane_animation()
def player_tombstone():

    image = [
        "  ___   ",
        " /   \\ ",
        "| RIP | ",
        "|     |  ",
        "|     |  ",
        "|___  |  "
        "GAME OVER"
    ]

    # Set delay
    delay = 0.4

    for row in image:
        print(row)
        time.sleep(delay)

    time.sleep(3)
    exit()

def zombie_animation():

    # Define the screen size
    width, height = 40, 20

    # Initialize the airplane's position and speed
    x, y = 0, height // 2
    speed = 2  # Increased animation speed

    # ASCII art representation of the airplane

    zombie_shape = [
        "                            ..... ",
        "                           C C  /            ",
        "                          /<   /             ",
        "           ___ __________/_#__=o             ",
        "          /(- /(\_\________   \              ",
        "          \ ) \ )_      \o     \             ",
        "          /|\ /|\       |'     |             ",
        "                        |     _|             ",
        "                        /o   __\             ",
        "                       / '     |             ",
        "                      / /      |             ",
        "                     /_/\______|             ",
        "                    (   _(    <              ",
        "                     \    \    \             ",
        "                      \    \    |            ",
        "                       \____\____\           ",
        "                       ____\_\__\_\          ",
        "                     /`   /`     o\          ",
        "                     |___ |_______|..  "
    ]
    while True:
        # Clear the console and print a lot of empty lines
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 50)  # Add a lot of empty lines

        # Draw the airplane
        for i in range(len(zombie_shape)):
            print(" " * x + zombie_shape[i])

        # Update the airplane's position
        x += speed

        # Limit the airplane's movement within the console
        if x < 0:
            x = 0
            speed = 1  # Change direction when reached the left edge

        elif x + len(zombie_shape[0]) >= width:
            x = width - len(zombie_shape[0])
            speed = -1  # Change direction when reached the right edge
        if x == 0:
            time.sleep(2)
            break

        # Pause briefly to display the animation
        time.sleep(0.1)  # Increased animation speed

# player_death()

