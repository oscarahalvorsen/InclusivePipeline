import pyttsx3
from matrix import matrix  # Assuming matrix is defined in the module 'matrix'

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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
    text = (f"This venue contains a total of {seat_map_data['empty_seats']} empty seats, distributed over {seat_map_data['total_rows']} rows and {seat_map_data['total_columns']}. "
            f"The available row groupings are, from front to back: ")
    speak(text)
    if len(groupings) == 2:
        group_text = (f"Group {1} (front): Rows {groupings[0][0][0]} to {groupings[0][-1][0]}\n"
                      f"Group {2} (back): Rows {groupings[1][0][0]} to {groupings[1][-1][0]}")
        speak(group_text)
    if len(groupings) == 3:
        group_text = (f"Group {1} (front): Rows {groupings[0][0][0]} to {groupings[0][-1][0]}\n"
                      f"Group {2} (middle): Rows {groupings[1][0][0]} to {groupings[1][-1][0]}\n"
                      f"Group {3} (back): Rows {groupings[2][0][0]} to {groupings[2][-1][0]}")
        speak(group_text)
    for i, group in enumerate(groupings):
        group_text = f"Group {i + 1}: Rows {group[0][0]} to {group[-1][0]}"
        speak(group_text)

def choose_row(group, group_nr):
    """ Allows user to choose a specific row within a group. """
    while True:
        available_rows = [index for index, empty_seat_count, row in group if empty_seat_count > 0]
        text = f"Available rows group {group_nr}: {available_rows}"
        speak(text)
        chosen_row_index = get_user_input("Please enter the row number you would like to sit in (or type 'exit' to quit): ")
        if chosen_row_index == 'exit':
            return 'exit'
        
        chosen_row = next((row for index, empty_seat_count, row in group if index == chosen_row_index), None)
        if chosen_row:
            if any(seat == 2 for seat in chosen_row):
                text = f"You chose row {chosen_row_index}. Are you happy with your choice? (yes/no)"
                speak(text)
                if get_user_input(text, str).lower() == 'yes':
                    speak("Row chosen successfully!")
                    return chosen_row, chosen_row_index
                else:
                    return 'exit'
            else:
                text = f"Sorry, there are no empty seats in row nr. {chosen_row_index}."
                speak(text)
                if get_user_input("Would you like to choose another row? (yes/no): ", str).lower() != 'yes':
                    return 'exit'
        else:
                text = f"Sorry, row nr. {chosen_row_index} is not in grouping {group_nr}."
                speak(text)
                if get_user_input("Would you like to choose another row? (yes/no): ", str).lower() != 'yes':
                    return 'exit'

def choose_seat(row, row_nr):
    row_data = get_seatmap_data([row])
    i = 0
    row_numbered = [0 if n == 0 or n == 1 else (i:=i+1)-1 for n in row if n == 0 or (i:=i+1)]
    available_seats = [seat for seat in row_numbered if seat != 0]
    while True:
        text = f"There are a total of {row_data['empty_seats']} empty seats in row nr. {row_nr}"
        speak(text)

        if (row_data['empty_seats'] == 1):
            index = row.index(2) if 2 in row else None
            text = f"The empty seat is on number seat nr. {row_numbered[index]}"
            speak(text)
            
            text = f"Do you want to choose seat nr. {row_numbered[index]} on row {row_nr}? (yes/no)"
            speak(text)
            if get_user_input(text, str).lower() == 'yes':
                text = f"Seat chosen successfully! You have chosen seat nr. {row_numbered[index]} on row {row_nr}."
                speak(text)
                return index
        
        text = f"Available seats in row nr. {row_nr} are: {available_seats}"
        speak(text)
        chosen_seat_index = get_user_input("Please enter the seat number you would like to sit in (or type 'exit' to quit): ")

        if chosen_seat_index == 'exit':
            return 'exit'

        if chosen_seat_index not in available_seats:
            text = f'Seat nr. {chosen_seat_index} is not an available seat in row {row_nr}.'
            speak(text)
            if get_user_input("Would you like to choose another seat? (yes/no): ", str).lower() != 'yes':
                return 'exit'

        text = f"You chose seat {chosen_seat_index} on row {row_nr}. Are you happy with your choice? (yes/no)"
        speak(text)
        if get_user_input(text, str).lower() == 'yes':
            speak("Seat chosen successfully!")
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
            text = "Invalid input. Please try again."
            speak(text)

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
            text = "Invalid grouping choice."
            speak(text)

if __name__ == "__main__":
    main()
