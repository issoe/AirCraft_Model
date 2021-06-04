####################################################################################################################################
#################################### ------ Import library  ------ #################################################################
# from Users.khanhquang.Downloads.AirCraft_MODEL.Again.cur import findPassenger, findTaxi
from re import A

from numpy.core.defchararray import count
import sub
import pandas as pd
import random
import numpy as np
import re

####################################################################################################################################
# Initial parameters from MISS.TRANG
arr_APU = ["123", "234"]
w_1 = 1
w_2 = 1
w_3 = 1

# System parameters
n_flights_apron = 0
count_loop = 0
time_break = 10

####################################################################################################################################
#################################### ------ MEASURE TIME EXECUTION  ------ #########################################################
from operator import index, indexOf
import timeit
start = timeit.default_timer()

####################################################################################################################################
#################################### ------ DATA FRAME ARRAY --> df ------ #########################################################
# NOTE: DATA INPUT MUST BE SORTED
# 1. Read data from file "input.csv" and get the numberOfFlighs
dfr = pd.read_csv('input.csv', sep=';', header=None)
numberOfFlights = len(dfr.iloc[:, 0])

# 2. Clean DATA and adding into array-s
arr_codeFlights = []    # colum index = 3    ####### Initial array 
arr_schedule = []       # colum index = 4
arr_timeDeparture = []  # colum index = 5
arr_timeArrival = []    # colum index = 6
arr_last_colum = []     # colum index = 7

####### Process  
sub.create_arr_codeflights(dfr, arr_codeFlights, numberOfFlights)
sub.create_arr_schedule(dfr, arr_schedule, numberOfFlights)
sub.create_arr_timeDeparture(dfr, arr_timeDeparture, numberOfFlights)
sub.create_arr_timeArrival(dfr, arr_timeArrival, numberOfFlights)
sub.create_arr_lastColum(dfr, arr_last_colum, numberOfFlights)

# Test len of input 
if len(arr_codeFlights) == len(arr_schedule) == len(arr_timeDeparture) == len(arr_timeArrival) == len(arr_last_colum):
    print("Lengh of all array input is OKAY")

####################################################################################################################################
#################################### ------ 86 TERMINALS WITH 4 KINDS OF CORRESPONDING LEVELS ------ ###############################
arr_level_case1 = []
arr_level_case2 = []
arr_level_case3 = []
arr_level_case4 = []

arr_pos_case1 = [3, 36, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]
arr_pos_case2 = [1, 2, 31, 32, 33, 34, 37, 38, 40, 41, 42, 43, 51, 52, 53, 54, 71, 72, 73, 74,
              75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 100, 101, 102, 103, 104]
arr_pos_case3 = [4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27]
arr_pos_case4 = [11, 12, 13]

arr_priority_1 = [4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
arr_priority_2 = [8, 9, 15, 16, 17, 18, 19, 20, 21, 22]
arr_priority_3 = [4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22]

# Array contained level and the flight previous-- ["No flight previous" ,nameOfFlight, kindOfFlight]
sub.create_initial_level(arr_level_case1, len(arr_pos_case1), arr_level_case2, len(arr_pos_case2), arr_level_case3, len(arr_pos_case3), arr_level_case4, len(arr_pos_case4))

####################################################################################################################################
#################################### ------ MY Def ------ #####
def isValidFlight(position):
    if len(dfr[1][position]) != 4 and len(dfr[1][position]) != 9:
        # print("[Fault_001]", position, ", codeFlight:", df[1][position])
        return False

    countValid = 0
    arr_validFlight = []
    if len(dfr[1][position]) == 4:
        arr_validFlight.append(dfr[1][position][0:4])
    if len(dfr[1][position]) == 9:
        arr_validFlight.append(dfr[1][position][5:9])

    for valid in arr_validFlight:
        try:
            testNumber = int(valid[1:4])
        except:
            # print("[Fault_001]", position, ", codeFlight:", df[1][position])
            return False

        if valid == "A320" or valid == "A321" or (valid[0:1] == "A" and 340 < testNumber < 600) or (valid[0:1] == "B" and 200 < testNumber < 800):
            countValid += 1
    
    if countValid == len(arr_validFlight):
        return True
    else: 
        # print("[Fault_001]", position, ", codeFlight:", df[1][position])
        return False


def Objective_Function(kindOfFlight, time, position, isVN):
    global w_1, w_2, w_3, count_loop, n_flights_apron, numberOfFlights
    count_loop += 1
    
    R_Apron = n_flights_apron/numberOfFlights

    avg_Taxi, max_Taxi = sub.findTaxi(position)
    R_Taxi = float(avg_Taxi/max_Taxi)
    
    actualAreaPassenger, maxAreaPassenger = sub.findPassenger(isVN)
    R_Service = (maxAreaPassenger - actualAreaPassenger) / maxAreaPassenger

    return w_1 * R_Apron + w_2 * R_Taxi + w_3 * R_Service

def get_level_from_position(position):
    index = 0
    for pos in arr_pos_case1:
        if position == pos:
            return arr_level_case1[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case2:
        if position == pos:
            return arr_level_case2[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case3:
        if position == pos:
            return arr_level_case3[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case4:
        if position == pos:
            return arr_level_case4[index][0]
        index += 1

    print("Fault at getting level of flight")    
    return -10
    

def update_level(position, newlevel, curr_kindFlight, curr_flightNo):
    for index in range(0, len(arr_pos_case1)):
        if position == arr_pos_case1[index]:
            arr_level_case1[index][0] = newlevel
            arr_level_case1[index][1] = curr_kindFlight
            arr_level_case1[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_pos_case2)):
        if position == arr_pos_case2[index]:
            arr_level_case2[index][0] = newlevel
            arr_level_case2[index][1] = curr_kindFlight
            arr_level_case2[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_pos_case3)):
        if position == arr_pos_case3[index]:
            arr_level_case3[index][0] = newlevel
            arr_level_case3[index][1] = curr_kindFlight
            arr_level_case3[index][2] = curr_flightNo
            return

    for index in range(0, len(arr_pos_case4)):
        if position == arr_pos_case4[index]:
            arr_level_case4[index][0] = newlevel
            arr_level_case4[index][1] = curr_kindFlight
            arr_level_case4[index][2] = curr_flightNo
            return

    print("The position wasnot found for updating at:", position, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])
    return -1

def get_previous_flight(position):
    for index in range(0, len(arr_pos_case1)):
        if position == arr_pos_case1[index]:
            return arr_level_case1[index][1], arr_level_case1[index][2]

    for index in range(0, len(arr_pos_case2)):
        if position == arr_pos_case2[index]:
            return arr_level_case2[index][1], arr_level_case2[index][2]

    for index in range(0, len(arr_pos_case3)):
        if position == arr_pos_case3[index]:
            return arr_level_case3[index][1], arr_level_case3[index][2]

    for index in range(0, len(arr_pos_case4)):
        if position == arr_pos_case4[index]:
            return arr_level_case4[index][1], arr_level_case4[index][2]

    print("Fault at finding previous flight")    
    return -3, -4

def update_n_Apron(timeCurrent):
    global n_flights_apron
    numberOfApron = 0
    for look in arr_priority_3:
        temp_level = get_level_from_position(look)
        if (temp_level + time_break) > timeCurrent:
            numberOfApron += 1
    n_flights_apron = numberOfApron

def find_terminal(arr_1, arr_2, arr_3, arr_4, prio_1, prio_2, prio_3, kindOfFlight, isVN, time_A, time_D, last_colum):
    initial_value_Ojective = 4
    
    # 1. Check the priority of "APU"
    mode_APU = False
    temp_APU = re.sub("[^0-9]", "", isVN)       # get the number from a string "isVN"
    for idx in range(0, len(arr_APU)):
        if temp_APU == arr_APU[idx]:
            mode_APU = True
            break

    # 2. var_time to determining exactly time for finding terminal
    var_time = time_D
    if time_A != -1:
        var_time = time_A

    # 3. Run the code with the priority first -- [If terminal was found in this case, it will return IMMEDIATELY]
    _position = -2
    _level = -2
    min_objective = 4

    if (((time_A != -1) and (60 < (time_D - time_A) < 90)) or (time_A == -1)) and (kindOfFlight != "A320") and (kindOfFlight != "A321") and (kindOfFlight != "AT72"):
        if isVN[0:2] == "VN":
            for idx in prio_1:      # idx = position
                temp_level = get_level_from_position(idx)                               # FIX
                temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)  # FIX
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    # Initial value objective
                    if initial_value_Ojective == 4:
                        initial_value_Ojective = temp_objective
                    
                    # Get value for return 
                    min_objective = temp_objective
                    _position = idx
                    _level = temp_level
        else:
            for idx in prio_2:
                temp_level = get_level_from_position(idx)                               # FIX
                temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)  # FIX
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    # Initial value objective
                    if initial_value_Ojective == 4:
                        initial_value_Ojective = temp_objective
                    
                    # Get value for return 
                    min_objective = temp_objective
                    _position = idx
                    _level = temp_level
        
        # Check fault here and return value 
        if _position != -2:
            update_n_Apron(time_D)      # TODO:
            return _position, _level, initial_value_Ojective, min_objective
        else:
            print("Fault at finding terminal", _position)

    # 4. Run the code without the priority
    _position = -2
    _level = -2
    min_objective = 4
    if kindOfFlight == "A20" or kindOfFlight == "AT72":
        for idx in arr_1:
            temp_level = get_level_from_position(idx)                                # <FIX>
            temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                # only get ONE time
                if initial_value_Ojective == 4:
                    initial_value_Ojective = min_objective

                min_objective = temp_objective
                _position = idx
                _level = temp_level
    
    if kindOfFlight == "A321" or kindOfFlight == "A20" or kindOfFlight == "AT72":
        for idx in arr_2:
            if (mode_APU == True) and (idx == 37 or idx == 38 or idx == 40 or idx == 41 or idx == 42 or idx == 43):
                continue
            else:
                temp_level = get_level_from_position(idx)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    if initial_value_Ojective == 4:
                        initial_value_Ojective = min_objective

                    min_objective = temp_objective
                    _position = idx
                    _level = temp_level

    if (kindOfFlight == "AT72") or (kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600) or (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for idx in arr_3:
            temp_level = get_level_from_position(idx)                                # <FIX>
            temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                # Only get ONE time
                if initial_value_Ojective == 4:
                    initial_value_Ojective = min_objective

                min_objective = temp_objective
                _position = idx
                _level = temp_level

    # The rest of flights
    for idx in arr_4:
        temp_level = get_level_from_position(idx)                                # <FIX>
        temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>
        if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
            # Only get ONE time
            if initial_value_Ojective == 4:
                initial_value_Ojective = min_objective

            min_objective = temp_objective
            _position = idx
            _level = temp_level

    update_n_Apron(time_D)
    if min_objective == 4:
        print("It cannot find a suitable terminal")

    return _position, _level, initial_value_Ojective, min_objective


####################################################################################################################################
#################################### ------ Driver code  ------ ##############
# Create 30 set of chromosome 
# for order in range(1, 31):

indexFlight = 0
order = 1
arr_res = []
arr_waiting_flight = []

arr_CurrPos1 = np.random.choice(arr_pos_case1, len(arr_pos_case1))
arr_CurrPos2 = np.random.choice(arr_pos_case2, len(arr_pos_case2))
arr_CurrPos3 = np.random.choice(arr_pos_case3, len(arr_pos_case3))
arr_CurrPos4 = np.random.choice(arr_pos_case4, len(arr_pos_case4))
arr_CurrPri1 = np.random.choice(arr_priority_1, len(arr_priority_1))
arr_CurrPri2 = np.random.choice(arr_priority_2, len(arr_priority_2))
arr_CurrPri3 = np.random.choice(arr_priority_3, len(arr_priority_3))


for time_minute in range(0, 1440):
    while (time_minute == arr_timeDeparture[indexFlight]) or (arr_timeDeparture[indexFlight] == -1):
        # IGNORE FLIGHT IF IT'S INVALID
        while isValidFlight(indexFlight) == False:
            indexFlight += 1
        
        # CASE 1 ----- [?--SGN--?]
        if arr_schedule[indexFlight] == '1':
            # 1. Find a suitable position            
            pos, level, init_t, final_l = find_terminal(arr_CurrPos1, arr_CurrPos2, arr_CurrPos3, arr_CurrPos4, arr_CurrPri1, arr_CurrPri2, arr_CurrPri3, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))

            # 2. Update again level with time_Departure
            newlevel = arr_timeDeparture[indexFlight]
            update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

            # 3. Add the flight to the result
            arr_res.append([indexFlight, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][1], init_t, final_l])

            # 4. Next Flight
            indexFlight += 1
        
        # CASE 2 ----- [SGN--?--SGN]
        if arr_schedule[indexFlight] == '2':
            ##--------------------- PHASE 1 ---------------------##
            # 1. Find a suitable position
            pos, level, init_t, final_l = find_terminal(arr_CurrPos1, arr_CurrPos2, arr_CurrPos3, arr_CurrPos4, arr_CurrPri1, arr_CurrPri2, arr_CurrPri3, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))

            # 2. Add the flight to a just found position
            # 2.1 UPDATE time_A and time_D
            time_A = 0
            if level == 0:
                time_A = -1
            else:
                time_A = level
            time_D = arr_timeDeparture[indexFlight] # maybe time_D = time_minute    

            # 2.2 Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 3. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])

            # 4. Adding the result_array
            arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])
            
            ##--------------------- PHASE 2 ---------------------##
            ### Getting "ONLY" the second flight to queue
            flightNO_temp = ''
            if len(dfr[1][indexFlight]) == 4:
                flightNO_temp = dfr[1][indexFlight]
            elif len(dfr[1][indexFlight]) == 9:
                flightNO_temp = dfr[1][indexFlight][5:9]
            else:                                       # <FIX> -- maybe delete this line
                print("Get len df [1][index] fault")    # <FIX> -- maybe delete this line
            
            ### Adding 
            arr_waiting_flight.append([arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][1], flightNO_temp, str(arr_last_colum[indexFlight])])

            ### ALWAYS SORT WHEN ADD FLIGHT TO WAITING_FLIGHT
            try:
                arr_waiting_flight.sort(key=sub.takeOne)  # OKAY
            except:
                print("Fault sorted")

            # 5. Next flight
            indexFlight += 1

        # CASE 3 ----- [SGN--?]
        if arr_schedule[indexFlight] == '3':
            # 1. Find a suitable position
            pos, level, init_t, final_l = find_terminal(arr_CurrPos1, arr_CurrPos2, arr_CurrPos3, arr_CurrPos4, arr_CurrPri1, arr_CurrPri2, arr_CurrPri3, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))
            
            # 2. Add the flight to a just found position
            # 2.1 UPDATE time_A and time_D
            time_A = 0
            if level == 0:
                time_A = -1
            else:
                time_A = level
            time_D = arr_timeDeparture[indexFlight] # maybe time_D = time_minute    

            # 2.2 Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 3. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

            # 4. Adding the result_array
            arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])

            # 5. Next flight 
            indexFlight += 1

        # CASE 4 ----- [?--SGN]
        if arr_schedule[indexFlight] == '4':
            # 1. Add flight to waiting array
            arr_waiting_flight.append([arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][0], dfr[1][indexFlight], str(arr_last_colum[indexFlight])])
            
            # 2. Next flight
            indexFlight += 1  

        ########################################################################################################
        ########################################################################################################
        # ADD "flight in queue" to "the head of flight" 
        try:
            while time_minute == arr_waiting_flight[0][0]:  
                # 1. Find a suitable position
                pos, level, init_t, final_l = find_terminal(arr_CurrPos1, arr_CurrPos2, arr_CurrPos3, arr_CurrPos4, arr_CurrPri1, arr_CurrPri2, arr_CurrPri3, arr_waiting_flight[0][2], arr_waiting_flight[0][1], -1, arr_waiting_flight[0][0], arr_waiting_flight[0][3])
                
                # 2. UPDATE NEW LEVEL HERE 
                newlevel = arr_waiting_flight[0][0]
                update_level(pos, newlevel, arr_waiting_flight[0][2], arr_waiting_flight[0][1])

                # 3. Remove the first element in waiting flights array
                temp_1 = arr_waiting_flight[0][0]
                temp_2 = arr_waiting_flight[0][1]
                temp_3 = arr_waiting_flight[0][2]
                temp_4 = arr_waiting_flight[0][3]
                arr_waiting_flight.remove([temp_1, temp_2, temp_3, temp_4])     
        except:
            print("Fault at processing waiting flight", time_minute)    

# Crossing over 
print("======Show the result======")
for row in arr_res:
    print(row)


####################################################################################################################################
print("\n--------Statistics---------------")
stop = timeit.default_timer()
print('Time: ', stop - start)  