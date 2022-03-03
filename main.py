from App import App
from Frames import MenuFrame


def main():
    frame = MenuFrame()
    application = App(frame, (800, 600))
    application.start()


if __name__ == '__main__':
    main()