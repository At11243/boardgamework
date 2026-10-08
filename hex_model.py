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

if __name__ == "__main__":
    from grid_definitions import barbarossa_grids

    region = barbarossa_grids["Map 2"]["regions"][0]
    grid = region["grid"]

    for column, row in [(0,0), (1,0), (2,0)]:
        center = hex_center(grid, column, row)
        print(f"Grid ({column}, {row}) -> center {center}")