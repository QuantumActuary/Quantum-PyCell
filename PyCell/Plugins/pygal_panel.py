import os
from environment import Window
from typography import Styles
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp
from panel_factory import PanelAssembler
import pygal

pygal_cache = '__cache__'
os.makedirs(pygal_cache, exist_ok=True)


class PygalWidget(Image):

    def __init__(self, name, chart):
        super(PygalWidget, self).__init__()
        self.chart = chart
        self.name = name
        self.chart.width = self.width / dp(1)
        self.chart.height = self.height / dp(1)
        self.filename = os.path.join(pygal_cache, '{}.png'.format(self.name))
        self.chart.render_to_png(self.filename, dpi=dp(72))
        self.source = self.filename
        self.size_update = False
        self.allow_stretch = True
        self.keep_ratio = False

        # children
        # None

        # bindings
        self.bind(size=self.size_changed)

    def dismiss(self):
        self.unbind(size=self.size_changed)

    def size_changed(self, inst, val):
        self.chart.width = val[0] / dp(1)
        self.chart.height = val[1] / dp(1)
        self.size_update = True

    def refresh(self, *args):
        self.chart.render_to_png(self.filename, dpi=dp(72))
        self.reload()
        self.size_update = False

class PygalAssembler(PanelAssembler):
    """
    An assembler for pygal panel contents.

    :ivar _chart: The pygal chart object to put into a panel
    """
    class UI_Pygal_Inner(BoxLayout):
        def __init__(self, chart, **kwargs):
            super().__init__(**kwargs)
            self.graph = chart

            # children
            self.add_widget(self.graph)

            # bindings
            self.bind(size=self.graph.size_changed)

        def dismiss(self):
            self.graph.dismiss()
            self.unbind(size=self.graph.size_changed)
            self.remove_widget(self.graph)

        def on_touch_up(self, touch):
            if self.graph.size_update:
                self.graph.refresh()
    #         super().on_touch_up(touch)
            return False

    def __init__(self):
        super().__init__()
        self._chart = None

    @property
    def chart(self):
        return self._chart

    @chart.setter
    def chart(self, chart):
        if isinstance(chart, PygalWidget):
            self._chart = chart
        else:
            print("Please supply a PygalWidget object!")

    def build_inner(self):
        if self._chart is not None:
            return PygalAssembler.UI_Pygal_Inner(self._chart)
        else:
            print("Cannot build pygal panel due to missing chart.")

    def create_panel(self, factory):
        factory.add_panel()
        factory.add_icon(Styles.title_icon(Styles.icon('1', 'Heydings-Common')))
        factory.add_title(Styles.title('PLOT VIEWPORT'))
        inner = self.build_inner()
        factory.add_inner(inner)
        factory.add_dismiss()
        result = factory.get_panel()
        result.size = (dp(400), dp(250))
        self._chart.size = result.size
        self._chart.refresh()
        return result

