from driver import Driver


def main():
    next_step = Driver.greetings_screen()
    while True:
        next_step = next_step()


if __name__ == "__main__":
    main()
