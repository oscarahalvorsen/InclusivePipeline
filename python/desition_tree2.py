from matrix import matrix

def display_available_groupings(groupings):
    """ Displays available row groupings with seat options. """
    for i, (start, end) in enumerate(groupings):
        print(f"Group {i + 1}: Rows from {start + 1} to {end + 1}")

def parse_groupings(matrix):
    """ Parses the matrix to identify row groupings that have available seats. """
    groupings = []
    start = None
    
    for i in range(len(matrix)):
        if any(seat == 1 or seat == 2 for seat in matrix[i]):  # Check if there's an available seat in the row
            if start is None:
                start = i
        elif start is not None:
            groupings.append((start, i - 1))
            start = None
    if start is not None:
        groupings.append((start, len(matrix) - 1))
    print(groupings)
    return groupings

def select_row(matrix):
    """ Allows the user to select a row group and then a specific row within the group. """
    row_groupings = parse_groupings(matrix)
    display_available_groupings(row_groupings)
    group_choice = int(input("Select a group number: ")) - 1
    start, end = row_groupings[group_choice]
    
    # Display rows within the group
    for i in range(start, end + 1):
        print(f"Row {i + 1}: ", matrix[i])
    
    row_choice = int(input(f"Select a row between {start + 1} and {end + 1}: ")) - 1
    return row_choice

def select_seat(row):
    """ Allows the user to select a seat from the chosen row. """
    available_seats = [i for i, seat in enumerate(row) if seat == 2]
    print("Available seats: ", available_seats)
    seat_choice = int(input("Select a seat number from the available options: "))
    return seat_choice

def main(matrix):
    row_choice = select_row(matrix)
    seat_choice = select_seat(matrix[row_choice])
    print(f"You have selected Seat: {seat_choice + 1} in Row: {row_choice + 1}")

main(matrix)
