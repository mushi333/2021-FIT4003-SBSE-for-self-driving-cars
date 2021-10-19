from math import sqrt, pow
import csv


def CalculatePercentage(type, speed, runs):
    # v indicates velocity
    num_crashes_ped = 0
    num_crashes_car = 0
    total_crashes = 0
    car_x = 0
    car_y = 0
    car_xv = 0
    car_yv = 0
    ped_x = 0
    ped_y = 0
    ped_xv = 0
    ped_yv = 0

    # Run for each seperate run#
    for i in range(runs):
        # Run for any
        with open(type + '_crashes_' + str(i) + '.txt') as f:
            # Read all ines into 
            lines = f.readlines()

        # Retrieve values from single line
        for j in range(len(lines)):
            # Skip if it is iteration or pop
            if 'Iteration: #99' in lines[j]:
                break
            elif '#' in lines[j]:
                pass
            else:
                # Convert values to float
                car_x, car_y, car_xv, car_yv, ped_x, ped_y, ped_xv, ped_yv = lines[j].split(',')
                car_x = float(car_x)
                car_y = float(car_y)
                car_xv = float(car_xv)
                car_yv = float(car_yv)
                ped_x = float(ped_x)
                ped_y = float(ped_y)
                ped_xv = float(ped_xv)
                ped_yv = float(ped_yv)

                # Find car and ped velocities and calculate crash
                car_v = sqrt(pow(car_xv, 2) + pow(car_yv, 2))
                # ped_v = sqrt(pow(ped_xv, 2) + pow(ped_yv, 2))
                if (car_v >= speed):
                    num_crashes_car += 1
                else:
                    num_crashes_ped += 1
                total_crashes += 1
        
        # Calculates percentages and prints them
        car_crash_to_total = num_crashes_car / total_crashes
        ped_crash_to_total = num_crashes_ped / total_crashes
        percentage_car = str(round(100*car_crash_to_total))
        percentage_ped = str(round(100*ped_crash_to_total))
        print(type)
        print("speed = " + str(speed))
        print("car crash percentage %" + percentage_car)
        print("ped crash percentage %" + percentage_ped)

        with open(type + '_crash_data.csv', 'a') as f:
            writer = csv.writer(f)
            data = [type, speed, i,percentage_car, percentage_ped]
            writer.writerow(data)    

if __name__ == '__main__':
    # Set speed to be compared to and the number of runs
    speed = 5
    runs = 12

    # Set csv header
    header = ['Type', 'Speed', 'Run','Car Percentage', 'Pedestrian Percentage']

    # GA Run
    type = 'ga'
    with open(type + "_crash_data.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    CalculatePercentage(type, speed, runs)

    # MCTS run
    type = 'mcts'
    with open(type + "_crash_data.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    CalculatePercentage(type, speed, runs)
    exit()