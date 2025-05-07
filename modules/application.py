from textual import on
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, DataTable, Button 
from textual.containers import Vertical, Horizontal
from textual.coordinate import Coordinate
from modules.geodesics import CentroidPlanner
from modules.maps import gmaps_get_locations
from typing import Callable, Union
import clipboard
import os

class CoordinateTab(Widget):
    def __init__(self,default_path, default_radi):
        def set_file_input_vaule(input: Input) -> None:
            if default_path is not None:
                input.value = default_path
        def set_radi_input_value(input: Input) -> None:
            if default_radi is not None:
                input.value = str(default_radi)
        self._template_inputs: list[tuple[str, InputType, Union[Callable[[Input], None], None]]] = [
            ("Latitude", "number", None),
            ("Longitude", "number", None),
            ("Radius", "number", set_radi_input_value),
            ("File", "text", set_file_input_vaule),
        ]
        self._template_buttons = [
            ("Add", "addLoc"),
            ("Delete", "deleteLoc"),
            ("Save", "saveLoc"),
            ("Load", "loadLoc"),
            ("Find", "findLoc")
        ]
        self._default_path = default_path
        Widget.__init__(self)
        self.styles.border = ("round", "white")
        self.styles.align = ("center", "top")

    def compose(self) -> ComposeResult:
        table_coordinates = DataTable(id="tableCoordinates")
        table_coordinates.styles.margin = (0, 1, 0, 1)
        table_coordinates.add_column("Lat")
        table_coordinates.add_column("Lon")
        table_coordinates.cursor_type = "row"
        yield table_coordinates 
        with Vertical() as v:
            v.styles.margin = (1, 0, 0, 0)
            v.styles.align = ("center", "bottom")
            v.styles.height = "auto"
            v.styles.dock = "bottom"
            for input in self._template_inputs:
                input_widget = Input(
                    placeholder=input[0],
                    type=input[1],
                    validate_on=["changed"],
                    id=input[0].lower() + "Input",
                    compact=True,
                )
                input_widget.styles.margin = (1, 1, 1, 1)
                input_widget.styles.height = 1
                if input[2] is not None:
                    input[2](input_widget)
                yield input_widget
            for i in range(0, len(self._template_buttons), 2):
                if i == len(self._template_buttons) - 1 and len(self._template_buttons)%2 == 1:
                    b = Button(label=self._template_buttons[i][0], id=self._template_buttons[i][1], compact=True)
                    b.styles.margin = (0, 1, 1, 1)
                    b.styles.width = "100%"
                    yield b
                    break
                with Horizontal() as h:
                    h.styles.align = ("center", "bottom")
                    h.styles.height = "auto"
                    for j in range(2):
                        b = Button(label=self._template_buttons[i+j][0], id=self._template_buttons[i+j][1], compact=True)
                        b.styles.margin = (0, 1, 1, 0)
                        b.styles.height = "auto"
                        yield b

    @on(Button.Pressed, selector="#addLoc")
    def add_location(self, event: Button.Pressed) -> None:
        queries = []
        for input in self._template_inputs[:2]:
            widget = self.query_one(f"#{input[0].lower()+"Input"}", Input)
            queries.append(widget)
            if widget.value == "":
                return
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        table_coordinates.add_row(queries[0].value, queries[1].value)

    class Find(Message):
        def __init__(self, coordinates: list[list[float]]):
            self.coordinates = coordinates
            super().__init__()

    @on(Button.Pressed, selector="#findLoc")
    def find_location(self, event: Button.Pressed) -> None:
        coordinates = []
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        if table_coordinates.row_count == 0:
            self.notify("Invalid input, at least one location is required for query.")
            return
        for i in range(table_coordinates.row_count):
            row_key, _ = table_coordinates.coordinate_to_cell_key(Coordinate(i, 0))
            row = table_coordinates.get_row(row_key)
            coordinates.append([row[0], row[1]])
        self.post_message(self.Find(coordinates))

    @on(Button.Pressed, selector="#deleteLoc")
    def delete_location(self, event: Button.Pressed) -> None:
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        if table_coordinates.row_count == 0:
            return
        cursor = table_coordinates.cursor_coordinate
        row_key, _ = table_coordinates.coordinate_to_cell_key(cursor)
        table_coordinates.remove_row(row_key)

    @on(Button.Pressed, selector="#loadLoc")
    def load_locations(self, event:Button.Pressed) -> None:
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        file_path = self.query_one("#fileInput", Input).value
        if file_path is None or file_path == "":
            self.notify("Please enter a path to load the input locations.")
            return
        if not os.path.exists(file_path):
            self.notify("Please enter a valid path to load the input locations.")
            return
        self.notify(f"Loading locations from file {os.path.abspath(file_path)}")
        coordinates = []
        with open(file_path, "r") as f:
            def parse_coordinate(line_text: str) -> tuple[bool, list[float]]:
                sectors = line_text.split(',')
                try:
                    lat, lon = float(sectors[0]), float(sectors[1])
                    return True, [lat, lon]
                except Exception:
                    lat, lon = 0.0, 0.0
                    return False, [lat, lon]

            for line in f:
                line = line.strip()
                ret, cords = parse_coordinate(line)
                if ret:
                    coordinates.append(cords)
        for coordinate in coordinates:
            table_coordinates.add_row(coordinate[0], coordinate[1])

    @on(Button.Pressed, selector="#saveLoc")
    def save_locations(self, event:Button.Pressed) -> None:
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        file_path = self.query_one("#fileInput", Input).value
        if file_path is None or file_path == "":
            self.notify("Please enter a path to save the input locations.")
            return
        self.notify(f"Writing to the file {os.path.abspath(file_path)}")
        with open(file_path, "w") as f:
            for i in range(table_coordinates.row_count):
                row_key, _ = table_coordinates.coordinate_to_cell_key(Coordinate(i, 0))
                row = table_coordinates.get_row(row_key)
                line = f"{row[0]}, {row[1]}\n"
                f.write(line)


class MeetfindApp(App):
    def __init__(self, category, file_path, radius):
        App.__init__(self)
        self.category = category
        self.file_path = file_path
        self.radius = radius

    def compose(self) -> ComposeResult:
        coordinate_tab = CoordinateTab(self.file_path, self.radius)
        coordinate_tab.styles.dock = "left"
        coordinate_tab.styles.width = "30%"
        yield coordinate_tab
        search_results = DataTable(id="searchResults")
        search_results.styles.border = ("round", "white")
        search_results.styles.height = "100%"
        for column in ("Name", "Type", "Rating", "Address", "Link"):
            search_results.add_columns(column)
        yield search_results

    @on(CoordinateTab.Find)
    def handle_find(self, event: CoordinateTab.Find):
        planner = CentroidPlanner()
        planner.setCoordinates(event.coordinates)
        centroid = planner.getCentroid()
        self.notify(f"Searching for centroid {centroid[0]}, {centroid[1]}")
        radius = self.query_one("#radiusInput", Input).value
        locs = []
        try:
            locs = gmaps_get_locations(centroid, self.category, radius)
        except Exception as e:
            self.notify(f"ERROR: Unable to get locations. {e}")
            return
        if len(locs) == 0:
            self.notify(f"INFO: Unable to find any location within the specified radius.")
            return
        search_results = self.query_one("#searchResults", DataTable)
        search_results.clear()
        for result in locs:
            search_results.add_row(result["name"], self.category.capitalize(), result["rating"], result["address"], result["link"])

