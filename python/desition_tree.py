from matrix import matrix  # Assuming matrix is defined in the module 'matrix'

# caps value of 2, ignoring different colored seats
def cap_values(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 2:
                matrix[i][j] = 2
    return matrix

def parse_seat_map(seat_map):
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
    available_rows = [index for index, row in group if any(seat == 2 for seat in row)]
    if not available_rows:
        return None, None
    before = [index for index in available_rows if index < chosen_row_index]
    after = [index for index in available_rows if index > chosen_row_index]
    nearest_before = max(before) if before else None
    nearest_after = min(after) if after else None
    return nearest_before, nearest_after

def choose_row(group):
    while True:
        print("Available rows in this grouping: ", [index for index, row in group])
        user_input = input("Please enter the row index you would like to sit in (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            return 'exit'
        try:
            chosen_row_index = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric row index.")
            continue
        
        chosen_row = next((row for index, row in group if index == chosen_row_index), None)
        if chosen_row and any(seat == 2 for seat in chosen_row):
            print("Row chosen successfully! Exiting program.")
            return 'success'
        else:
            print("No empty seats in chosen row.")
            nearest_before, nearest_after = find_nearest_rows(group, chosen_row_index)
            print(f"Nearest available row before: {nearest_before}, after: {nearest_after}")
            if input("Would you like to choose another row? (yes/no): ").lower() != 'yes':
                break

def main():
    seat_map = cap_values(matrix)
    groupings = parse_seat_map(seat_map)
    while True:
        print(f"This venue contains {len(groupings)} groupings. The available row roupings are: ")
        for i, group in enumerate(groupings):
            print(f"Group {i + 1}: Rows {group[0][0]} to {group[-1][0]}")
        
        group_choice_input = input("Choose a grouping by number (or type 'exit' to quit): ")
        if group_choice_input.lower() == 'exit':
            break
        try:
            group_choice = int(group_choice_input) - 1
        except ValueError:
            print("Invalid input. Please enter a numeric group choice.")
            continue

        if 0 <= group_choice < len(groupings):
            result = choose_row(groupings[group_choice])
            if result == 'exit':
                break
            elif result == 'success':
                break
        else:
            print("Invalid grouping choice.")

if __name__ == "__main__":
    main()
