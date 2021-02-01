from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView

from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty

from kivy.clock import Clock

import time
import csv

def export_csv(arg):
    pass

class Timer(BoxLayout):
    """
    ~~timer will have a task title, start and end timestamps, and a field for notes.~~
    timer will live display count while timer is running
    once done is clicked, the timer will be comitted to a log
    """
    Defaults = {'title': 'New task', 'note': 'Notes go here'}
    title = StringProperty(Defaults['title'])
    note = StringProperty(Defaults['note'])
    elapsed_time = NumericProperty(0)
    button_function_text = StringProperty('START')

    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.reset()

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.display_timer = None
        self.title = self.Defaults['title']
        self.note = self.Defaults['note']
        self.elapsed_time = 0

    def button_handler(self):
        if self.end_time:
            self.button_function_text ='START'
            #need to update self.title and self.note otherwise backend thinks they havent changed and doesnt reset the text. this is also the only time we take the data out of the front end for logging.
            self.title = self.ids.title.text
            self.note = self.ids.note.text
            self.log()
            self.reset()

        elif self.start_time:
            self.button_function_text = 'SUBMIT'
            self.end()
        else:
            self.button_function_text = 'STOP'
            self.start()

    def start(self):
        self.start_time = time.time()
        self.display_timer = Clock.schedule_interval(self.update_elapsed_time, 0.05)
        print('STARTED')

    def end(self):
        self.end_time = time.time()
        self.display_timer.cancel()
        self.elapsed_time = self.end_time - self.start_time
        print('ENDED')

    def update_elapsed_time(self, dt):
        self.elapsed_time = time.time() - self.start_time

    def log(self):
        data = [self.start_time, self.end_time, self.title, self.note]
        with open("log_cache.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print(data)


class Row(GridLayout):
    """docstring for Row."""
    start_time = StringProperty('start')
    end_time = StringProperty('end')
    title = StringProperty('title')
    note = StringProperty('note')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4


class RowViewer(RecycleView):
    def __init__(self, **kwargs):
        super().__init__()
        self.data = self.load_data()
        # self.data = [{'start_time':str(x), 'end_time':str(x), 'title':str(x), 'note':str(x)} for x in range(5)]

    def load_data(self):
        with open("log_cache.csv", 'r', newline ='') as file:
            reader = csv.DictReader(file, fieldnames = ['start_time', 'end_time', 'title', 'note'])
            data = [{'start_time':'start_time', 'end_time':'end_time', 'title':'title', 'note':'note'}]
            for row in reader:
                data.append(row)
            return data


class MainApp(App):
    """
    app will have two screens:
        - main screen has timer interface
        - second screen has log viewer, with ability to edit notes
    app will have an export csv button
    app will have a select all button
    app will have deselect all button
    app will have a clear selected from log button
    app should save on exit
    """

    def build(self):
        timer = Timer()
        # sheet = LogViewer()
        # return sheet
        return RowViewer()

if __name__ == '__main__':
    MainApp().run()
