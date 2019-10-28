def print_menu(menu_items):
    selection = 0

    def print_menu_internal(menu_items):
        list_count = 1
        choice = 0
        print(30 * "-", "MENU", 30 * "-")
        if len(menu_items) > 0:
            choice = input("Enter your choice: [{}-{}] ".format("1", (len(menu_items) + 1)))
        else:
            print("-----No modules found-----")
        for menu_item in menu_items:
            print("{}. {}".format(list_count, menu_item.modulePrettyName))
            list_count = list_count + 1
        print("{}. {}".format(list_count, 'Exit/Return'))
        print(64 * "-")

        try:
            choice = int(choice)
        except Exception as e:
            print(e)
            choice = 0

        # Check if the value is above the number of menu items
        try:
            while choice > (len(menu_items) + 1):
                print("Please select a valid menu item: ")
                choice = 0
        except Exception as e:
            print(e)
            choice = 0

        # Check if the value was zero
        while choice <= 0:
            print("Please select a valid menu item:")
            choice = 0

        return choice

    while selection == 0:
        print_menu_internal(menu_items)
    selection = int(selection) - 1
    return selection
