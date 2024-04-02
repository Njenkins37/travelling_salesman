# Nick Jenkins Student ID: 001335147
from datetime import time
import csv
import Graph
import Destination_Algorithm
from Package import Package
from HashTable import MyHashTable

# declaration of variables to be used throughout the program
package_list = []
distance_list = []
time_list = []
hash_table = MyHashTable()
truck_list_one = [1, 2, 4, 5, 7, 8, 11, 17, 21, 23, 33, 37, 40]
truck_list_two = [3, 13, 14, 15, 16, 18, 20, 19, 24, 27, 29, 30, 31, 34, 36, 38]
truck_list_three = [6, 9, 25, 26, 28, 32, 35, 39, 10, 22, 12]
mileage_truck = []
values_to_be_summed = []
total_mileage = 26.1 + 40.9 + 30.3


# creates a dictionary from a file path
def create_dictionary(file_path):
    my_dictionary = {}
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            key1 = row[0]
            values = row[1:]
            my_dictionary[key1] = values

    return my_dictionary


# function creates a package object from the csv file and inserts the package into a list.
def load_package_data(file_name):
    with open(file_name) as packages:
        package_data = csv.reader(packages, delimiter=',')
        next(package_data)
        for pack in package_data:
            package_id = pack[0]
            package_utah_address = pack[1]
            package_city = pack[2]
            package_state = pack[3]
            zip_code = pack[4]
            package_ttd = pack[5]
            package_weight = pack[6]
            package_restrictions = pack[7]
            complete_package = Package(package_id, package_utah_address, package_city, package_state, zip_code,
                                       package_ttd,
                                       package_weight, package_restrictions)
            hash_table.insert(package_id, complete_package)
            insert_package(complete_package)


# insert a package into a package list
def insert_package(package_type):
    package_list.append(package_type)
    return package_list


def retrieve_package(package_id):
    for package_item in package_list:
        if package_item.package_id == package_id:
            return package_item


if __name__ == '__main__':
    # creates a dictionary and a list for the packages
    csv_file_path = 'packages.csv'
    # package_dictionary = create_dictionary(csv_file_path)
    # my_package_list = list(package_dictionary.values())
    load_package_data(csv_file_path)

    # creates a dictionary and a list for the distance values
    csv_file_path = 'distances.csv'
    distance_dictionary = create_dictionary(csv_file_path)
    my_distance_list = list(distance_dictionary.values())

    # beginning of the interface that the user will interact with
    print("Welcome to WGUPS where we can get a package at 9:05AM and somehow deliver it before 10:30 AM.\n"
          "What would you like to know about our packages?\n")
    print("1. A single package search (1-40)")
    print("2. Search for all packages at the end of the day. This section will give you the total mileage.")
    print("3. Search by time to see if your package has been delivered or not. ")
    print("4. Quit the Program")
    choice = input("Your Decision?")

    # creating the variables to hold list data for various functions later
    utah_graph = Graph.Graph()
    merged_array = []
    address_array = []
    second_address_array = []
    package_address = []
    test_list = []
    already_visited_list = []
    starting_time = time(8, 0, 0)

    truck_package_list_one = []
    truck_package_list_two = []
    truck_package_list_three = []

    # Looping the package into the list to send into the algorithm.
    for package in package_list:
        if int(package.package_id) in truck_list_one:
            truck_package_list_one.append(package)
    for package in package_list:
        if int(package.package_id) in truck_list_two:
            truck_package_list_two.append(package)
    for package in package_list:
        if int(package.package_id) in truck_list_three:
            truck_package_list_three.append(package)

    for package in package_list:
        if package.package_id == '25' or package.package_id == '26':
            package.update_address('5383 S 900 East #104')

    # Big O of n^2 looping the keys into a double key dictionary with the distance as the values.
    # Graph created with vertexes and undirected graph with weights is created
    for i in range(len(my_distance_list) - 1):
        for j in range(len(my_distance_list) - 1):
            vertex_a = my_distance_list[i][0]
            vertex_b = my_distance_list[j + 1][0]
            weight = my_distance_list[j + 1][i + 1]

            utah_graph.add_vertex(vertex_a)
            utah_graph.add_vertex(vertex_b)
            utah_graph.add_undirected_edge(vertex_a, vertex_b, weight)
    # list of lists for dictionary
    package_address.insert(0, 'HUB')
    address_connections = []

    for key in utah_graph.edge_weights:
        address_connections.append(key)

    temp_key = 'HUB'

    # removing values with 0 as the edge weight because the algorithm will always take the 0 routes if left in.
    value_to_remove = '0.0'
    key_to_remove = ' HUB'
    new_test_dictionary = {key: value for key, value in utah_graph.edge_weights.items()
                           if value != value_to_remove and key[1] != key_to_remove}
    # testing a new dictionary to see if removing the HUB location and leaving edge weights of 0 to see if it improves
    # function
    second_test_dictionary = {key: value for key, value in utah_graph.edge_weights.items() if key[1] != key_to_remove}

    starting_location = address_connections[0][0]
    starting_location_list = []
    for package in package_list:
        if package.package_id == '9':
            package.update_address('410 S State St')
            package.update_zip_code('84111')

    mileage = 0

    Destination_Algorithm.package_delivery_algorithm(starting_location, second_test_dictionary,
                                                     starting_time,
                                                     truck_package_list_one, mileage,
                                                     len(truck_package_list_one))
    # takes the time stamp of the first algorithm call and formats the time stamp
    for package in package_list:
        end_time = package.status
        correct_end_time = end_time[13:]
        time_list.append(correct_end_time)

    Destination_Algorithm.package_delivery_algorithm(starting_location, second_test_dictionary,
                                                     starting_time,
                                                     truck_package_list_two, mileage,
                                                     len(truck_package_list_two))
    # converts the time stamp from the latest time in truck one and passes it into the third algorithm call
    time_converter = max(time_list)
    hour = int(time_converter[:2])
    minutes = int(time_converter[3:-3])
    seconds = int(time_converter[6:])
    time_for_truck_three = time(hour, minutes, seconds)

    Destination_Algorithm.package_delivery_algorithm(starting_location, second_test_dictionary,
                                                     time_for_truck_three, truck_package_list_three,
                                                     mileage,
                                                     len(truck_package_list_three))

    # finishes the interface after the algorithm has run.
    if choice == str(1):
        package_to_search = input("Type in your package number from 1 - 40. \n")
        for package in package_list:
            if package.package_id == package_to_search:
                if int(package.package_id) in truck_list_one:
                    package.update_status(str(package.status) + " by truck one")
                    print(package)
                elif int(package.package_id) in truck_list_two:
                    package.update_status(str(package.status) + " by truck two")
                    print(package)
                elif int(package.package_id) in truck_list_three:
                    package.update_status(str(package.status) + " by truck three")
                    print(package)
    elif choice == str(2):
        for package in package_list:
            if int(package.package_id) in truck_list_one:
                package.update_status(str(package.status) + " by truck one")
                print(package)
            elif int(package.package_id) in truck_list_two:
                package.update_status(str(package.status) + " by truck two")
                print(package)
            elif int(package.package_id) in truck_list_three:
                package.update_status(str(package.status) + " by truck three")
                print(package)

        print("Our trucks have just finished their day with a total mileage of " + str(total_mileage) + '. \n')
    elif choice == str(3):
        time_input = input("Give me a time to search for in HH:MM:SS format.")
        try:
            hour = int(time_input[:2])
            minute = int(time_input[3:-3])
            second = int(time_input[6:])
            time_to_search = time(hour, minute, second)
            for package in package_list:
                time_to_manipulate = package.status
                hour = int(time_to_manipulate[13:-6])
                minute = int(time_to_manipulate[16:-3])
                second = int(time_to_manipulate[19:])
                delivery_time = time(hour, minute, second)

                if time_to_search > delivery_time:
                    if int(package.package_id) in truck_list_one:
                        package.update_status('delivered at ' + str(delivery_time) + " by truck one")
                    elif int(package.package_id) in truck_list_two:
                        package.update_status('delivered at ' + str(delivery_time) + " by truck two")
                    elif int(package.package_id) in truck_list_three:
                        package.update_status('delivered at ' + str(delivery_time) + " by truck three")
                    print(package)
                else:
                    if int(package.package_id) in truck_list_one:
                        package.update_status("En route in truck 1")
                    elif int(package.package_id) in truck_list_two:
                        package.update_status("En route in truck 2")
                    elif int(package.package_id) in truck_list_three:
                        package.update_status("En route in truck 3")

                    print(package)

        except ValueError:
            print("You did not enter the time in correctly. Please try again.")
