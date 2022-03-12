from App import App
from Frames import MenuFrame
import Config

def main():
    frame = MenuFrame()
    application = App(frame, (Config.screen_width, Config.screen_height))
    application.start()


if __name__ == '__main__':
    main()