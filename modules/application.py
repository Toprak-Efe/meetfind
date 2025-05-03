from textual import events
from textual.color import Color
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Input, DataTable, Placeholder, Button, Log
from textual.containers import Vertical, Horizontal, HorizontalGroup, VerticalGroup

g_logger = Log()

class CoordinateTab(Widget):
    def compose(self) -> ComposeResult:
        self.styles.border = ("round", "white")
        self.styles.align = ("center", "top")
        
        self.w_coordinates = DataTable()
        self.w_coordinates.styles.margin = (0, 1, 0, 1)
        self.w_coordinates.add_column("Name")
        self.w_coordinates.add_column("Lat")
        self.w_coordinates.add_column("Lon")
        yield self.w_coordinates 
        
        with Vertical() as v:
            #v.styles.border = ("round", "white")
            v.styles.align = ("center", "bottom")
            v.styles.height = "auto"
            v.styles.dock = "bottom"
        
            self.inputs = [
                Input(
                    placeholder=("Name", "Latitude", "Longitude")[j],
                    type=("text", "number", "number")[j],
                    validate_on=["changed"],
                    id=("name", "latitude", "longitude")[j],
                    compact=True
                )
            for j in range(3)]

            for input in self.inputs:
                input.styles.margin = (0, 1, 1, 1)
                yield input
            
            with Horizontal() as h:
                h.styles.align = ("center", "bottom")
                h.styles.height = "auto"
                for j in range(2):
                    b = Button(label=("Add", "Find")[j], id=("addLoc", "findLoc")[j])
                    b.styles.margin = (0, 1, 0, 1)
                    b.styles.height = "auto"
                    b.styles.width = "auto"
                    yield b

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "addLoc":
            if self.inputs[0].value == "":
                return
            if self.inputs[1].value == "" or self.inputs[2].value == "":
                return
            log = g_logger
            log.write_line(f"{self.inputs[0].value}, {len(self.inputs[1].value)}, {self.inputs[2].value}")
            self.w_coordinates.add_row(self.inputs[0].value, self.inputs[1].value, self.inputs[2].value)
        if event.button.id == "findLoc":
            # Create a message to the main app
            pass

class MeetfindApp(App):
    def compose(self) -> ComposeResult:
        self.w_c = CoordinateTab()
        self.w_c.styles.dock = "left"
        self.w_c.styles.width = "30%"
        g_logger.styles.border = ("round", "white")
        g_logger.styles.background = Color(0, 0, 0)
        yield self.w_c
        yield g_logger 

    def on_key(self, event: events.Key) -> None:
        if event.key == 'q':
            self.exit()

    def on_find(self) -> None:
        # Get the coordinates, find the centroid. use Google API to get nice Cafe's and print them out with hyperlinks in markdown.
        pass
