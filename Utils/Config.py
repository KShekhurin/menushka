import Perspective

local_rus = {
    "": "",
    "новая_игра": "Новая игра",
    "настройки": "Настройки",
    "выйти": "Выйти",
    "продолжить": "Продолжить",
    "сохраниться": "Сохраниться",
    "сохранить_игру": "Сохранить игру",
    "загрузить": "Загрузить",
    "загрузить_игру": "Загрузить игру",
    "рыба": "Съешь ещё больше этих сладких французских булок.",
    "громкость_звуков": "Громкость звуков: ",
    "громкость_музыки": "Громкость музыки: ",
    "сохранить_изменения": "Сохранить изменения",
    "вернуться": "Вернуться",
    "русский": "Русский",
    "китайский": "Китайский",
    "латинский": "Латинский",
    "пусто": "Пусто",
    "якуб_мотив_1": "Нажимай уже на кнопку!",
    "якуб_мотив_2": "Ну чего ты ждешь?",
    "якуб_мотив_3": "Особое приглашение нужно?",
    "якуб_мотив_4": "Часики-то тикают..",
    "якуб_зол_1": "Безобразие!",
    "якуб_зол_2": "Как не стыдно!",
    "якуб_зол_3": "Имейте совесть!",
    "якуб_прив_1": "Приветствую!",
    "якуб_прив_2": "Чтобы начать игру,",
    "якуб_прив_3": "нажмите на кнопку",
    "якуб_прив_4": "Новая игра.",
    "якуб_прив_5": "Чтобы перейти в",
    "якуб_прив_6": "настройки, нажмите",
    "якуб_прив_7": "на кнопку Настройки.",
    "якуб_прив_8": "Поменять язык можно",
    "якуб_прив_9": "при помощи свитка.",
    "якуб_прив_10": "Если хотите выйти,",
    "якуб_прив_11": "нажмите уже наконец Выйти!"
}

local_chi = {
    "": "",
    "новая_игра": "新游戏",
    "настройки": "设置",
    "выйти": "出去",
    "продолжить": "继续",
    "сохраниться": "保存",
    "сохранить_игру": "保存游戏",
    "загрузить": "下载",
    "загрузить_игру": "下载游戏",
    "рыба": "多吃那些甜的法式面包。",
    "громкость_звуков": "音量：",
    "громкость_музыки": "音乐音量：",
    "сохранить_изменения": "保存更改",
    "вернуться": "返回",
    "русский": "俄语",
    "китайский": "中国人",
    "латинский": "拉丁语",
    "пусто": "空的",
    "якуб_мотив_1": "已经按下按钮了！",
    "якуб_мотив_2": "那么，你还等什么呢？",
    "якуб_мотив_3": "需要特别邀请吗？",
    "якуб_мотив_4": "时钟在滴答作响。。",
    "якуб_зол_1": "丑陋！",
    "якуб_зол_2": "多可惜！",
    "якуб_зол_3": "有良心！",
    "якуб_прив_1": "你好！",
    "якуб_прив_2": "开始游戏",
    "якуб_прив_3": "点击按钮",
    "якуб_прив_4": "新游戏。",
    "якуб_прив_5": "要去",
    "якуб_прив_6": "设置，点击",
    "якуб_прив_7": "到设置按钮。",
    "якуб_прив_8": "您可以更改语言",
    "якуб_прив_9": "在卷轴的帮助下。",
    "якуб_прив_10": "如果你想出去",
    "якуб_прив_11": "点击已经终于退出！"
}

local_lat = {
    "": "",
    "новая_игра": "Novum ludum",
    "настройки": "Occasus",
    "выйти": "Exite",
    "продолжить": "Perge",
    "сохраниться": "Salvare",
    "сохранить_игру": "Salvum ludum",
    "загрузить": "Download",
    "загрузить_игру": "Download ludum",
    "рыба": "Plus comedunt ex illis dulcibus paunculis Gallicis.",
    "громкость_звуков": "Sanum volumen:",
    "громкость_музыки": "Volumen Musicum:",
    "сохранить_изменения": "Servare Mutationes",
    "вернуться": "Redi",
    "русский": "Russica",
    "китайский": "Seres",
    "латинский": "Latinae",
    "пусто": "Inanis",
    "якуб_мотив_1": "Preme ipsum iam!",
    "якуб_мотив_2": "Hem, quid moraris?",
    "якуб_мотив_3": "Egesne invitationem specialem?",
    "якуб_мотив_4": "Horologium utilatate..",
    "якуб_зол_1": "Turpis!",
    "якуб_зол_2": "Quid pudor est!",
    "якуб_зол_3": "Habeto conscientiam!",
    "якуб_прив_1": "Salvete!",
    "якуб_прив_2": "Incipere ludum",
    "якуб_прив_3": "click in puga pyga",
    "якуб_прив_4": "Novum ludum.",
    "якуб_прив_5": "Ire ad",
    "якуб_прив_6": "occasus, preme",
    "якуб_прив_7": "ad Occasus deprimendo.",
    "якуб_прив_8": "Linguam mutare potes",
    "якуб_прив_9": "ope libri.",
    "якуб_прив_10": "Si vis egredi",
    "якуб_прив_11": "click iam tandem Exit!"
}

screen_width = 800
screen_height = 600
window_title = "Игрушка"

helper_motivational_phrases = (
    "якуб_мотив_1",
    "якуб_мотив_2",
    "якуб_мотив_3",
    "якуб_мотив_4"
)
helper_anger_phrases = (
    "якуб_зол_1",
    "якуб_зол_2",
    "якуб_зол_3"
)
helper_greeting_phrases = (
    "якуб_прив_1",
    "якуб_прив_2",
    "якуб_прив_3",
    "якуб_прив_4",
    "якуб_прив_5",
    "якуб_прив_6",
    "якуб_прив_7",
    "якуб_прив_8",
    "якуб_прив_9",
    "якуб_прив_10",
    "якуб_прив_11"
)
helper_blink_freq = 4000
helper_motivational_phrase_freq = 10000

current_local = local_rus



items_data = {
    "mandarin": ((80, 80), "menu_slider_circle_pic", "Мандарин - царь фруктов"),
    "plate": ((90, 60), "item_plate_pic", "Тарелка разукрашенная")
}

inventory_items_data = {
    "mandarin": ((30, 30), "menu_slider_circle_pic", "Мандарин - царь фруктов"),
    "plate": ((40, 30), "item_plate_pic", "Тарелка разукрашенная")
}

items_in_location = {
    "summer": (
            ("mandarin", (562, 319), (544, 453)),
            ("plate", (405, 300), (398, 450))
    ),
    "church": ()
}

portals_in_location = {
    "summer": (
        ((200, 538), (725, 600), "church")
    ),
    "church": (
       ((200, 538), (725, 600), "summer") 
    )
}

scenes_data = {
    "summer": (
        (0, 0, 0), "scene_field_background_pic", (500, 600),
        Perspective.CustomPerspective(
            Perspective.PerspectiveSetter(
                (406, 290),
                (800, 600),
                (0, 600)
            ),
            [
                (800, 600),
                (0, 600),
                (242, 430),
                (523, 430),
            ]
        ), 
        items_in_location["summer"], 
        portals_in_location["summer"]),
    "church": (
        (0, 0, 0), "scene_church_background_pic", (500, 600),
        Perspective.CustomPerspective(
            Perspective.PerspectiveSetter(
                (406, 250),
                (800, 600),
                (-100, 600)
            ),
            [
                (800, 600),
                (-100, 600),

                (279, 367),
                (516, 362),

                (520, 418),

                (666, 397),
            ]
        ), 
        items_in_location["church"], 
        portals_in_location["church"])
}

'''
Perspective.TrapezoidPerspective(screen_height, 440, 50, 750, 185, 615)
        Perspective.CustomPerspective(
            Perspective.PerspectiveSetter(
                (406, 290),
                (800, 600),
                (0, 600)
            )
        ), 
'''