import pygal
from pygal import Config
from pandas import Series
from pandas import DataFrame
from panel_factories import OSXWindowFactory
from pygal_panel import PygalAssembler
from pygal_panel import PygalWidget
from pygal.style import DarkColorizedStyle
from PyCell import registry
from PyCell.custom_cell import Custom
from kivy.clock import mainthread
from kivy.app import App

registry += [
    {
    'name': 'Make_Chart',
    'module': 'PyCell.pygal_cell',
    'categories': ['Data', 'Output']
    },
    {
    'name': 'Add_To_Chart',
    'module': 'PyCell.pygal_cell',
    'categories': ['Data', 'Output']
    }
    ]

class Pygal_Chart(object):
    assembler = PygalAssembler()

    def __init__(self, mkchart, title='Default', show_legend=True,
                 x_title=None, y_title=None, show_dots=False, range=None,
                 xrange=None, show_x_guides=False, show_y_guides=False,
                 fill=False, human_readable=True, style=DarkColorizedStyle):

        self.context = App.get_running_app().root.ids.main_ui
        style.background = 'transparent'
        style.plot_background = 'transparent'
        style.opacity = '.7'
        config = Config()
        config.show_legend = show_legend
        config.human_readable = human_readable
        config.fill = fill
        config.title = title
        config.x_title = x_title
        config.y_title = y_title
        config.show_dots = show_dots
        config.xrange = xrange
        config.range = range
        config.show_x_guides = show_x_guides
        config.show_y_guides = show_y_guides
        config.style = style
        self.config = config
        self.chart = mkchart(config)
        self.view = None

    def show(self):
        if self.view is None:
            pg = PygalWidget(str(id(self.chart)), self.chart)
            Pygal_Chart.assembler.chart = pg
            factory = App.get_running_app().main.window_factory
            self.view = Pygal_Chart.assembler.create_panel(factory)
        self.context.add_widget(self.view)


class Make_Chart(Custom):
    kind = {'line': 'line', 'bar': 'bar'}

    def __init__(self):
        self.inputs = {'kind': Make_Chart.kind, 'title': None}
        self.outputs = {'chart': None}
        self.chart = None

    def make_chart(self):
        kind = self.inputs['kind']
        title = self.inputs['title']
        if kind == 'line':
            return Pygal_Chart(pygal.Line, title=title)
        else:
            return Pygal_Chart(pygal.Bar, title=title)

    def process(self):
        self.chart = self.make_chart()
        self.outputs['chart'] = self.chart
        return super().process()


class Add_To_Chart(Custom):
    def __init__(self):
        self.inputs = {'chart': None, 'label': None, 'data': None}
        self.outputs = {'chart': None}

    def add_to_chart(self):
        try:
            data = self.inputs['data'].df
        except:
            data = self.inputs['data']

        if isinstance(data, list):
            self.inputs['chart'].chart.add(self.inputs['label'], data)
        elif isinstance(data, Series):
            if data.index.name is None:
                if self.inputs['label'] is None:
                    label = 'data'
                else:
                    label = self.inputs['label']
            else:
                label = data.index.name
            self.inputs['chart'].chart.add(label, data.values)
        elif isinstance(data, DataFrame):
            for header, value in data.iteritems():
                self.inputs['chart'].chart.add(str(header), value)
        else:
            raise

    def process(self):
        assert isinstance(self.inputs['chart'], Pygal_Chart), (
               "Chart input should be a Pygal_Chart!")
        self.add_to_chart()
        self.outputs['chart'] = self.inputs['chart']
        return super().process()

