from datetime import datetime, timedelta
from Package import Package


def package_delivery_algorithm(starting_location, dictionary, starting_time, package_list, mileage, count):
    location_values = []
    location_list = []
    values_to_be_summed = []
    packages_remaining = package_list
    package_address_list = []

    # takes the package address and adds it to a list to be referenced
    for package in package_list:
        package_address_list.append(package.address)

    miles_per_second = 18 / 3600
    dt = datetime.combine(datetime.today(), starting_time)
    seconds_variable = 0
    # main algorithm call. Creates a reference variable at the second key
    # and checks to see if the first key is the starting
    # location and the second key is in the package_address list.
    if count > 0:
        for key in dictionary.keys():
            # cutting the zip codes off of the addresses
            reference_variable = key[1]
            reformatted = reference_variable[:-8]
            final_form = reformatted[1:]

            # takes the values associated with each keys and adds it to a list
            if key[0] == starting_location and final_form in package_address_list:
                value = float(dictionary[key])
                location_values.append(value)

        # takes the lowest value
        try:
            lowest_value = min(location_values)

        except ValueError:
            lowest_value = 0

        # For loop gives me the reference variable to check to see if the destination still has a package
        for key, value in dictionary.items():
            if key[0] == starting_location and value == str(lowest_value):
                temp_variable = key[1]
                reformatted_variable = temp_variable[1:-8]

                # updates the starting location to be the second key and records the time
                if reformatted_variable in package_address_list:
                    values_to_be_summed.append(lowest_value)
                    starting_location = key[1]
                    location_list.append(starting_location)
                    seconds_variable = float(value) / miles_per_second
                    new_dt = dt + timedelta(seconds=seconds_variable)

                    for package in package_list:
                        address_to_be_referenced = str(package.address)
                        # checks to see if the second key is in the package address list
                        if str(starting_location).lstrip().startswith(address_to_be_referenced) \
                                and address_to_be_referenced in package_address_list:
                            # updates the package status to note the time the package was delivered
                            # and removes the package from the list
                            package.update_status('Delivered at ' + str(new_dt.time()))
                            packages_remaining.remove(package)
                            #print(package)
                            #print('Total mileage is: ' + str(lowest_value + mileage))

        # recursive call passing in the updated information
        package_delivery_algorithm(starting_location, dictionary, (dt + timedelta(seconds=seconds_variable)).time(),
                                   packages_remaining, mileage + float(lowest_value), count - 1)
