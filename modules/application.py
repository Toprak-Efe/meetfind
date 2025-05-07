from textual import on
from textual import events
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input, DataTable, Button, RichLog
from textual.containers import Vertical, Horizontal
from textual.coordinate import Coordinate
from modules.geodesics import CentroidPlanner
from modules.maps import gmaps_get_locations

class CoordinateTab(Widget):
    def __init__(self, cords):
        Widget.__init__(self)
        self.styles.border = ("round", "white")
        self.styles.align = ("center", "top")
        self.default_coordinates = cords

    def compose(self) -> ComposeResult:
        table_coordinates = DataTable(id="tableCoordinates")
        table_coordinates.styles.margin = (0, 1, 0, 1)
        table_coordinates.add_column("Name")
        table_coordinates.add_column("Lat")
        table_coordinates.add_column("Lon")
        table_coordinates.cursor_type = "row"
        for coordinate in self.default_coordinates:
            table_coordinates.add_row("Doe", coordinate[0], coordinate[1])
        yield table_coordinates 
        with Vertical() as v:
            v.styles.margin = (1, 0, 0, 0)
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
                    b = Button(label=("Add", "Delete")[j], id=("addLoc", "deleteLoc")[j])
                    b.styles.margin = (0, 1, 1, 1)
                    b.styles.height = "auto"
                    b.styles.width = "auto"
                    yield b
            b = Button(label="Find", id="findLoc")
            b.styles.margin = (0, 2, 1, 2)
            b.styles.width = "100%"
            yield b

    @on(Button.Pressed, selector="#addLoc")
    def add_location(self, event: Button.Pressed) -> None:
        if self.inputs[0].value == "" or self.inputs[1].value == "" or self.inputs[2].value == "":
            return
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        table_coordinates.add_row(self.inputs[0].value, self.inputs[1].value, self.inputs[2].value)

    class Find(Message):
        def __init__(self, coordinates: list[list[float]]):
            self.coordinates = coordinates
            super().__init__()

    @on(Button.Pressed, selector="#findLoc")
    def find_location(self, event: Button.Pressed) -> None:
        coordinates = []
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        if table_coordinates.row_count == 0:
            return
        for i in range(table_coordinates.row_count):
            row_key, _ = table_coordinates.coordinate_to_cell_key(Coordinate(i, 0))
            row = table_coordinates.get_row(row_key)
            coordinates.append([row[1], row[2]])
        self.post_message(self.Find(coordinates))

    @on(Button.Pressed, selector="#deleteLoc")
    def delete_location(self, event: Button.Pressed) -> None:
        table_coordinates = self.query_one("#tableCoordinates", DataTable)
        if table_coordinates.row_count == 0:
            return
        cursor = table_coordinates.cursor_coordinate
        row_key, _ = table_coordinates.coordinate_to_cell_key(cursor)
        table_coordinates.remove_row(row_key)

class MeetfindApp(App):
    def __init__(self, coordinates, category):
        App.__init__(self)
        self.coordinates = coordinates
        self.category = category 

    def compose(self) -> ComposeResult:
        coordinate_tab = CoordinateTab(self.coordinates)
        coordinate_tab.styles.dock = "left"
        coordinate_tab.styles.width = "30%"
        yield coordinate_tab
        with Vertical() as v:
            search_results = DataTable(id="searchResults")
            search_results.styles.border = ("round", "white")
            search_results.styles.height = "70%"
            for column in ("Name", "Type", "Rating", "Address", "Link"):
                search_results.add_columns(column)
            search_results.styles.margin = (0, 1, 1, 1)
            yield search_results
            rich_logger = RichLog(id="logger")
            rich_logger.styles.border = ("round", "white")
            rich_logger.styles.height = "30%"
            yield rich_logger

    @on(CoordinateTab.Find)
    def handle_find(self, event: CoordinateTab.Find):
        logger = self.query_one("#logger", RichLog)
        planner = CentroidPlanner()
        planner.setCoordinates(event.coordinates)
        centroid = planner.getCentroid()
        ret, locs = gmaps_get_locations(centroid, self.category, 200)
        if not ret:
            logger.write(f"Unable to retrieve locations.")
            return
        if len(locs) == 0:
            logger.write(f"Unable to find any locations within the specified radius.")
            return
        search_results = self.query_one("#searchResults", DataTable)
        search_results.clear()
        for result in locs:
            search_results.add_row(result["name"], self.category, result["rating"], result["address"], result["link"])

