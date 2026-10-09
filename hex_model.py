from math import floor



def hex_center(grid, column, row):
    """ Return a hex center in coordinates within its map image."""

    #Calculate the position in VASSAL's grid orientation.
    grid_x = grid["x0"] + column * grid["dx"]
    grid_y = grid["y0"] + row * grid["dy"]

    #Alternate columns are shifted by half the spacing. 
    if column % 2 != 0:
        grid_y += grid["dy"] / 2

    #VASSAL swaps the axes for a sidways grid
    if grid["sideways"]:
        return grid_y, grid_x

    return grid_x, grid_y

def nearest_hex(grid, image_x, image_y):
    """Find the closest hex center to an image position."""

    #Convert the click into the grid's orientation.
    if grid["sideways"]:
        grid_x, grid_y = image_y, image_x
    else:
        grid_x, grid_y = image_x, image_y

    approximate_column = floor(
        (grid_x - grid["x0"]) / grid["dx"]
    )

    best = None
    best_distance = float("inf")

    #Check nearby centers, including staggered columns.
    for column in range(
        approximate_column - 1 ,
        approximate_column + 3,
    ):
        shift = grid["dy"] / 2 if column % 2 else 0 

        approximate_row = floor(
            (grid_y - grid["y0"] - shift) / grid["dy"]
        )

        for row in range(approximate_row - 1 , approximate_row + 3):
            center_x, center_y = hex_center(grid, column, row)

            distance = (
                (center_x - image_x) ** 2
                + (center_y - image_y) ** 2
            )

            if distance < best_distance:
                best_distance = distance
                best = (column, row, center_x, center_y)

    return best

def printed_hex_number(region, column, row):
    """Convert internal grid indices to the game's hex number"""

    grid = region["grid"]
    numbering = region["numbering"]

    xs = [x for x, y in region["boundary"]]
    ys = [y for x, y in region["boundary"]]

    width = max(xs) - min(xs)
    height = max(ys) - min(ys)

    #Region dimension control descending numbering in VASSAL
    max_rows = floor(height / grid["dx"] + 0.5)
    max_columns = floor(width / grid["dy"] + 0.5)

    horizontal_descends = numbering["hDescend"] == "true"
    vertical_descends = numbering["vDescend"] == "true"

    numbered_column = column
    numbered_row = row 

    if grid["sideways"]:
        if vertical_descends:
            numbered_column = max_rows - column

        if horizontal_descends:
            numbered_row = max_columns - row
    else:
        if horizontal_descends:
            numbered_column = max_columns - column

        if vertical_descends:
            numbered_row = max_rows - row

    #Numbering can shift on alternate grid columns
    if numbering["stagger"] == "true" and column % 2 != 0:
        descends = (
            horizontal_descends
            if grid["sideways"]
            else vertical_descends
        )

        numbered_row += -1 if descends else 1

    horizontal = numbered_column + int(numbering["hOff"])
    vertical = numbered_row + int(numbering["vOff"])

    horizontal_digits = int(numbering["hLeading"]) + 1 
    vertical_digits = int(numbering["vLeading"]) + 1

    horizontal_text = f"{horizontal:0{horizontal_digits}d}"
    vertical_text = f"{vertical:0{vertical_digits}d}"

    separator = numbering["sep"]

    if numbering["first"] == "H": 
        return horizontal_text + separator + vertical_text

    return vertical_text + separator + horizontal_text

def hex_vertices(grid, center_x, center_y):
    """Return six vertices, ordered to match our side numbers."""

    dx = grid["dx"]
    dy = grid["dy"]

    if grid["sideways"]:
        offsets = [
            (0, -2 * dx / 3),
            (dy / 2 , -dx / 3 ),
            (dy / 2 , dx / 3 ),
            (0, 2 * dx / 3),
            (-dy / 2, dx / 3),
            (-dy / 2 , -dx / 3)
        ]
    else: 
        offsets = [
            (-dx / 3, -dy / 2),
            (dx / 3, -dy / 2),
            (2 * dx / 3, 0),
            (dx / 3, dy / 2),
            (-dx / 3, dy / 2),
            (-2 * dx / 3, 0),
        ]

    return [
        (center_x + x , center_y + y)
        for x,y in offsets
    ]

def nearest_hexside(grid, center_x, center_y, click_x, click_y):
    """Return the nearest side and its two endpoints."""

    vertices = hex_vertices(grid, center_x, center_y)
    best = None
    best_distance = float("inf")

    for side in range(6):
        start = vertices[side]
        end = vertices[(side + 1 ) % 6]

        vx = end[0] - start[0]
        vy = end[1] - start[1]

        fraction = (
            (click_x - start[0]) * vx 
            + (click_y - start[1]) * vy
        ) / (vx * vx + vy * vy)

        fraction = max(0, min(1, fraction))

        closest_x = start[0] + fraction * vx
        closest_y = start[1] + fraction * vy

        distance = (
            (click_x - closest_x) ** 2 
            + (click_y - closest_y ) ** 2 
        )

        if distance < best_distance:
            best_distance = distance 
            best = (side, start, end)

    return best


if __name__ == "__main__":
    from campaign_grid_definitions import barbarossa_grids

    region = barbarossa_grids["Map 2"]["regions"][0]

    center = hex_center(region["grid"], 8, 45)
    number = printed_hex_number(region, 8, 45)

    print(f"Region: {region['name']}")
    print(f"Center: {center}")
    print(f"Printed Hex: {number}")