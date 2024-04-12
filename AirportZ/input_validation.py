def input_check(choice, max_choice):


    while True:
        try:
            choice = int(choice)
            if choice > 0 and choice < max_choice+1:
                break
            else:
                choice = input(f"Please choose a whole number between 1-{max_choice}: ")
        except: choice = input(f"Please choose a whole number between 1-{max_choice}: ")

    return choice
