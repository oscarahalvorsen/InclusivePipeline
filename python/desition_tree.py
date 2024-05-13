from matrix import matrix

#caps value of 2, ignoring different colored seets
def cap_values(matrix):
    # Iterate over each row in the matrix
    for i in range(len(matrix)):
        # Iterate over each element in the row
        for j in range(len(matrix[i])):
            # If the element is greater than 2, set it to 2
            if matrix[i][j] > 2:
                matrix[i][j] = 2
    return matrix

def parse_seat_map(seat_map):
    groupings = []
    current_group = []
    for index, row in enumerate(seat_map):
        if any(seat != 0 for seat in row):  # Check if the row has any non-zero entries
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
        return None, None  # No available rows in the group
    before = [index for index in available_rows if index < chosen_row_index]
    after = [index for index in available_rows if index > chosen_row_index]
    nearest_before = max(before) if before else None
    nearest_after = min(after) if after else None
    return nearest_before, nearest_after

def choose_row(group):
    while True:
        print("Available rows in this grouping: ", [index for index, row in group])
        chosen_row_index = int(input("Please enter the row index you would like to sit in: "))
        chosen_row = next((row for index, row in group if index == chosen_row_index), None)
        if chosen_row and any(seat == 2 for seat in chosen_row):
            print("Row chosen successfully!")
            return
        else:
            print("No empty seats in chosen row.")
            nearest_before, nearest_after = find_nearest_rows(group, chosen_row_index)
            print(f"Nearest available row before: {nearest_before}, after: {nearest_after}")
            if input("Would you like to choose another row? (yes/no): ") != 'yes':
                break

def main():
    seat_map=cap_values(matrix)
    groupings = parse_seat_map(seat_map)
    while True:
        print("Row Groupings Available: ")
        for i, group in enumerate(groupings):
            print(f"Group {i + 1}: Rows {group[0][0]} to {group[-1][0]}")
        
        group_choice = int(input("Choose a grouping by number: ")) - 1
        if 0 <= group_choice < len(groupings):
            choose_row(groupings[group_choice])
        else:
            print("Invalid grouping choice.")
        
        if input("Would you like to exit? (yes/no): ") == 'yes':
            break

if __name__ == "__main__":
    main()
