from matrix import matrix  # Assuming matrix is defined in the module 'matrix'

def cap_values(matrix):
    """ Caps values of seats to 2, ignoring higher values. """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 2:
                matrix[i][j] = 2
    return matrix

def get_groupings(seat_map):
    """ Parses the seat map into groupings separated by empty rows. """
    groupings = []
    current_group = []
    row_counter = 0  # Initialize counter for non-zero rows
    for index, row in enumerate(seat_map):
        if any(seat != 0 for seat in row):
            row_counter += 1  # Increment for each non-zero row
            empty_seat_count = sum(1 for element in row if element == 2)
            current_group.append((row_counter, empty_seat_count, row))  # Store the row with the updated counter
        else:
            if current_group:
                groupings.append(current_group)
                current_group = []
    if current_group:
        groupings.append(current_group)
    return groupings

def get_seatmap_data(seat_map):
    total_seats = sum(1 for row in seat_map for element in row if element != 0)
    empty_seats = sum(1 for row in seat_map for element in row if element == 2)
    total_rows = sum(any(value != 0 for value in row) for row in seat_map) if seat_map else 0
    total_columns = sum(any(col != 0 for col in column) for column in zip(*seat_map)) if seat_map else 0
    return {"total_seats": total_seats, "empty_seats": empty_seats, "total_rows": total_rows, "total_columns": total_columns}

def display_groupings(groupings, seat_map_data):
    """ Displays available row groupings. """
    print(f"This venue contains a total of {seat_map_data['empty_seats']} empty seats, distributed over {seat_map_data['total_rows']} rows and {seat_map_data['total_columns']}.") 
    print(f"The available row groupings are, from front to back: ")
    if len(groupings)==2:
        print(f"Group {1} (front): Rows {group[0][0]} to {group[-1][0]}")
        print(f"Group {2} (back): Rows {group[0][0]} to {group[-1][0]}")
    if len(groupings)==3:
        print(f"Group {1} (front): Rows {group[0][0]} to {group[-1][0]}")
        print(f"Group {2} (middle): Rows {group[0][0]} to {group[-1][0]}")
        print(f"Group {3} (back): Rows {group[0][0]} to {group[-1][0]}")
    for i, group in enumerate(groupings):
        print(f"Group {i + 1}: Rows {group[0][0]} to {group[-1][0]}")

def choose_row(group, group_nr):
    """ Allows user to choose a specific row within a group. """
    while True:
        print(f"Available rows group {group_nr}: ", [index for index, empty_seat_count, row in group if empty_seat_count>0])
        chosen_row_index = get_user_input("Please enter the row number you would like to sit in (or type 'exit' to quit): ")
        if chosen_row_index == 'exit':
            return 'exit'
        
        chosen_row = next((row for index, empty_seat_count, row in group if index == chosen_row_index), None)
        if chosen_row:
            if any(seat == 2 for seat in chosen_row):
                if get_user_input(f"You chose row {chosen_row_index}. Are you happy with your choice? (yes/no)", str).lower() == 'yes':
                    print("Row chosen successfully!")
                    return chosen_row, chosen_row_index
                else:
                    return 'exit'
            else:
                print(f"Sorry, there are no empty seats in row nr. {chosen_row_index}.")
                if get_user_input("Would you like to choose another row? (yes/no): ", str).lower() != 'yes':
                    return 'exit'
        else:
                print(f"Sorry, row nr. {chosen_row_index} is not int grouping 2.")
                if get_user_input("Would you like to choose another row? (yes/no): ", str).lower() != 'yes':
                    return 'exit'

def choose_seat(row, row_nr):
    row_data = get_seatmap_data([row])
    i = 0
    row_numbered = [0 if n == 0 or n == 1 else (i:=i+1)-1 for n in row if n == 0 or (i:=i+1)]
    available_seats = [seat for seat in row_numbered if seat != 0]
    while True:
        print(f"There are a total of {row_data['empty_seats']} empty seats in row nr. {row_nr}")

        if (row_data['empty_seats'] == 1):
            index = row.index(2) if 2 in row else None
            print(f"The empty seat is on number seat nr. {row_numbered[index]}")
            
            if get_user_input(f"Do you want to chose seat nr. {row_numbered[index]} on row {row_nr}.? (yes/no)", str).lower() == 'yes':
                print(f"Seat chosen successfully! You have chosen seat nr. {row_numbered[index]} on row {row_nr}.")
                return index
        
        print(f"Available seats in row nr. {row_nr} are: {available_seats}")
        chosen_seat_index = get_user_input("Please enter the seat number you would like to sit in (or type 'exit' to quit): ")

        if chosen_seat_index == 'exit':
            return 'exit'

        if chosen_seat_index not in available_seats:
            print(f'Seat nr. {chosen_seat_index} is not an available seat in row {row_nr}.')
            if get_user_input("Would you like to choose another seat? (yes/no): ", str).lower() != 'yes':
                return 'exit'

        if get_user_input(f"You chose seat {chosen_seat_index} on row {row_nr}. Are you happy with your choice? (yes/no)", str).lower() == 'yes':
            print("Seat chosen successfully!")
            return available_seats.index(chosen_seat_index)
        else:
            return 'exit'
        

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

def main():
    seat_map = cap_values(matrix)
    groupings = get_groupings(seat_map)
    seat_map_data = get_seatmap_data(seat_map)
    display_groupings(groupings, seat_map_data)
    while True:
        group_choice = get_user_input("Please choose a grouping by its group number (or type 'exit' to quit): ")
        if group_choice == 'exit':
            break
        if 0 <= group_choice - 1 < len(groupings):
            row = choose_row(groupings[group_choice - 1], group_choice)
            if row == 'exit':
                break
            elif isinstance(row, tuple):
                choose_seat(row[0], row[1])
                break
        else:
            print("Invalid grouping choice.")

if __name__ == "__main__":
    main()
