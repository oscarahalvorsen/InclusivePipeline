from matrix import matrix  # Assuming matrix is defined in the module 'matrix'

def cap_values(matrix):
    """ Caps values of seats to 2, ignoring higher values. """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 2:
                matrix[i][j] = 2
    return matrix

def parse_seat_map(seat_map):
    """ Parses the seat map into groupings separated by empty rows. """
    groupings = []
    current_group = []
    for index, row in enumerate(seat_map):
        if any(seat != 0 for seat in row):
            current_group.append((index, row))
        else:
            if current_group:
                groupings.append(current_group)
                current_group = []
    if current_group:
        groupings.append(current_group)
    return groupings

def find_nearest_rows(group, chosen_row_index):
    """ Finds nearest rows with available seats. """
    available_rows = [index for index, row in group if any(seat == 2 for seat in row)]
    if not available_rows:
        return None, None
    before = [index for index in available_rows if index < chosen_row_index]
    after = [index for index in available_rows if index > chosen_row_index]
    return max(before, default=None), min(after, default=None)

def get_user_input(prompt, input_type=int):
    """ Generic function to get user input and handle common errors. """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            return 'exit'
        try:
            return input_type(user_input)
        except ValueError:
            print("Invalid input. Please try again.")

def display_groupings(groupings):
    """ Displays available row groupings. """
    print(f"This venue contains {len(groupings)} groupings. The available row groupings are: ")
    for i, group in enumerate(groupings):
        print(f"Group {i + 1}: Rows {group[0][0]} to {group[-1][0]}")

def choose_row(group):
    """ Allows user to choose a specific row within a group. """
    while True:
        print("Available rows in this grouping: ", [index for index, row in group])
        chosen_row_index = get_user_input("Please enter the row index you would like to sit in (or type 'exit' to quit): ")
        if chosen_row_index == 'exit':
            return 'exit'
        
        chosen_row = next((row for index, row in group if index == chosen_row_index), None)
        if chosen_row and any(seat == 2 for seat in chosen_row):
            print("Row chosen successfully! Exiting program.")
            return 'success'
        else:
            print("No empty seats in chosen row.")
            nearest_before, nearest_after = find_nearest_rows(group, chosen_row_index)
            print(f"Nearest available row before: {nearest_before}, after: {nearest_after}")
            if get_user_input("Would you like to choose another row? (yes/no): ", str).lower() != 'yes':
                return 'exit'

def main():
    seat_map = cap_values(matrix)
    groupings = parse_seat_map(seat_map)
    display_groupings(groupings)
    while True:
        group_choice = get_user_input("Please choose a grouping by its group number (or type 'exit' to quit): ")
        if group_choice == 'exit':
            break
        if 0 <= group_choice - 1 < len(groupings):
            result = choose_row(groupings[group_choice - 1])
            if result in ['exit', 'success']:
                break
        else:
            print("Invalid grouping choice.")

if __name__ == "__main__":
    main()
