from App import App
from Frames import IntroFrame, MenuFrame
import Config

def main():
    frame = IntroFrame()
    application = App(frame, (Config.screen_width, Config.screen_height))
    application.start()


if __name__ == '__main__':
    main()