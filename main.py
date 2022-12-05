# This is a sample Python script.
import PySimpleGUI as sg
import time

START_STRING = 'No 🍅 yet!'
DEFAULT_POMODORO_TIMER = 25
BTN_START_POMODORO = 'Start Pomodoro! 💪'
BTN_STOP_POMODORO = 'Make it stop! 😭'

class PomCounter:
    def __init__(self):
        # self.counter = count
        self.pomstring = ''

    def reset(self):
        # self.counter = 0
        self.pomstring = ''

    def countup(self):
        # self.counter += 1
        self.pomstring += '🍅'

    def pom_string(self):
        # i = 0
        if self.pomstring == '':
            return START_STRING
        else:
            return 'This much: ' + self.pomstring


class PomTimer:
    def __init__(self, mins=25):
        self.time_of_start = 0.0
        self.time_of_end = 0.0
        # self.was_started = False
        self.time_is_up = False
        # self.time_left = time_amount*60

    # def reset(self, time_amount=25*60):
    #     self.time_left = time_amount

    def start(self, mins=25):
        self.time_is_up = False
        self.time_of_start = time.time()
        self.time_of_end = self.time_of_start + mins*60

    def time_left(self):
        delta = self.time_of_end - time.time()
        if delta <= 0:
            self.time_is_up = True
            return 0
        return delta

    def time_left_str(self):
        time_left = time.gmtime(self.time_left())
        return ":".join([str(time_left[3]), str(time_left[4]), str(time_left[5])])

    def should_countup(self):
        if self.time_of_start and self.time_is_up:
            self.time_of_start = 0
            self.time_of_end = 0
            return True
        else:
            return False

    # def is_counting(self):
    #     if self.time_is_up:
    #         return False

        # if self.time_of_end:
        #     if self.time_left() > 0:
        #         return True
        #     else:
        #         self.time_is_up = True
        #         return False
        # else:
        #     return False


sg.theme("DarkGray10")
layout = [[sg.Text('Pomodoro Timer', font=("Tahoma", 22), grab=True)],
          [sg.VPush()],
          [sg.Text(START_STRING, key='-POMOS-')],
          [sg.Button(BTN_START_POMODORO, key='-ST_BUTTON-'), sg.Button('Exit')],
          [sg.Text(':'.join(['0', str(DEFAULT_POMODORO_TIMER), '00']), key='-TIMER-')],
          [sg.VPush()]
          ]

window = sg.Window(
    "Pomodoro Timer",
    layout,
    size=(300, 300),
    resizable=True,
    keep_on_top=True,
    no_titlebar=True,
    element_justification='center',
    font=('Segoe UI', 12),
    finalize=True,
    # button_color=['black', 'white']
    # font=("GOST Type A", 14)
    # grab_anywhere=True,
    # use_custom_titlebar=True,
    # titlebar_background_color=None
)

pc = PomCounter()
pt = PomTimer()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    while True:  # Event Loop
        event, values = window.read(timeout=100)
        if pt.should_countup():
            pc.countup()
            window['-POMOS-'].update(pc.pomstring)
            window['-ST_BUTTON-'].update(BTN_START_POMODORO)
        if not pt.time_is_up:
            window['-TIMER-'].update(pt.time_left_str())
        if event == '-ST_BUTTON-':
            pt.start(mins=0.1)
            window['-ST_BUTTON-'].update(BTN_STOP_POMODORO)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
