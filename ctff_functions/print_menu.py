def print_menu(menu_items):
    selection = 0

    def print_menu_internal(menu_items):
        list_count = 1
        print(30 * "-", "MENU", 30 * "-")
        for menu_item in menu_items:
            print("{}. {}".format(list_count, menu_item.modulePrettyName))
            list_count = list_count + 1
        print("{}. {}".format(list_count, 'Exit/Return'))
        print(64 * "-")

        if len(menu_items) > 0:
            choice = input("Enter your choice: [{}-{}] ".format("1", (len(menu_items) + 1)))
        else:
            print("No menu items available")
            choice = 0

        try:
            choice = int(choice)
            if choice > (len(menu_items) + 1):
                choice = 0
            else:
                choice = int(choice)
        except Exception as e:
            choice = 0
        return choice

    while selection <= 0:
        selection = print_menu_internal(menu_items)
        if selection <= 0:
            print("Please select a valid menu item")

    selection = int(selection) - 1
    return selection
