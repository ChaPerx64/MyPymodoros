import PySimpleGUI as sg
import time

BTN_1 = '-ST_BUTTON-'

START_STRING = 'No 🍅 yet!'
BTN_START_POMODORO = 'Start Pomodoro! 💪'
BTN_STOP_POMODORO = 'Make it stop! 😭'
BTN_START_REST = "Take a rest! 🔫😜"
BTN_SKIP_REST = "Enough 🤖"
POMODORO_DURATION = 25
REST_DURATION = 5
SHOULD_REST = False


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
    def __init__(self):
        self.time_of_start = 0.0
        self.time_of_end = 0.0
        # self.was_started = False
        self.time_is_up = False
        # self.time_left = time_amount*60

    def reset(self):
        self.__init__()

    def start(self, mins=25):
        self.time_is_up = False
        self.time_of_start = time.time()
        self.time_of_end = self.time_of_start + mins * 60

    def time_left(self):
        delta = self.time_of_end - time.time()
        if delta <= 0:
            self.time_is_up = True
            return 0
        return delta

    def time_left_str(self):
        time_left = time.gmtime(self.time_left())
        mins = self.time_to_two_digits(time_left[4])
        secs = self.time_to_two_digits(time_left[5])
        return ":".join([mins, secs])

    def should_countup(self):
        if self.time_of_start and self.time_is_up:
            self.time_of_start = 0
            self.time_of_end = 0
            return True
        else:
            return False

    @staticmethod
    def time_to_two_digits(t_str):
        t_str = str(t_str)
        if len(t_str) == 1:
            t_str = '0' + t_str
        return t_str


sg.theme("DarkGray10")
layout = [[sg.Text('Pomodoro\nTimer', font=("Tahoma", 16), grab=True, justification='center')],
          [sg.VPush()],
          [sg.Text('', key='-TIMER-', font=("Tahoma", 36))],
          [sg.VPush()],
          [sg.Button(BTN_START_POMODORO, key=BTN_1)],
          [sg.VPush()],
          [sg.Text(START_STRING, key='-POMOS-'), sg.Push(), sg.Button('Q')],
          ]

window = sg.Window(
    "Pomodoro Timer",
    layout,
    size=(280, 360),
    resizable=True,
    keep_on_top=True,
    no_titlebar=True,
    element_justification='center',
    font=('Segoe UI Emoji', 11),
    finalize=True,
    margins=(50, 30)
)

pc = PomCounter()
pt = PomTimer()
rt = PomTimer()

if __name__ == '__main__':
    while True:  # Event Loop
        event, values = window.read(timeout=100)
        if rt.should_countup():
            rt.reset()
            window[BTN_1].update(BTN_START_POMODORO)
            SHOULD_REST = False
        if pt.should_countup():
            pt.reset()
            pc.countup()
            SHOULD_REST = True
            window['-POMOS-'].update(pc.pomstring)
            window[BTN_1].update(BTN_START_REST)
        else:
            if SHOULD_REST:
                window['-TIMER-'].update(rt.time_left_str())
            else:
                window['-TIMER-'].update(pt.time_left_str())
        if event == BTN_1:
            if SHOULD_REST:
                if rt.time_of_start:
                    rt.reset()
                    window[BTN_1].update(BTN_START_POMODORO)
                    window['-TIMER-'].update(pt.time_left_str())
                    SHOULD_REST = False
                else:
                    rt.start(mins=REST_DURATION)
                    window[BTN_1].update(BTN_SKIP_REST)
            else:
                if pt.time_of_start:
                    pt.reset()
                    window[BTN_1].update(BTN_START_POMODORO)
                    window['-TIMER-'].update(pt.time_left_str())
                else:
                    pt.start(POMODORO_DURATION)
                    window[BTN_1].update(BTN_STOP_POMODORO)
        if event == sg.WIN_CLOSED or event == 'Q':
            break
    window.close()
