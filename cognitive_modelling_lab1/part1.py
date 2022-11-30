# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from matplotlib import pyplot as plt


def start(type="middle"):
    return 0


def perceptualstep(type="middle"):
    if type == "slow":
        return 200
    elif type == "middle":
        return 100
    elif type == "fast":
        return 50
    else:
        raise Exception("Bad type")


def cognitivestep(type="middle"):
    if type == "slow":
        return 170
    elif type == "middle":
        return 70
    elif type == "fast":
        return 25
    else:
        raise Exception("Bad type")


def motorstep(type="middle"):
    if type == "slow":
        return 100
    elif type == "middle":
        return 70
    elif type == "fast":
        return 30
    else:
        raise Exception("Bad type")


def example1():
    print(f"Total time: {start() + perceptualstep() + cognitivestep() + motorstep()}")


def example2(completeness="extremes"):
    if completeness == "extremes":
        time1 = start("fast") + perceptualstep("fast") + cognitivestep("fast") + motorstep("fast")
        print(f"Fastman: {time1}")

        time2 = start("middle") + perceptualstep("middle") + cognitivestep("middle") + motorstep("middle")
        print(f"Middleman: {time2}")

        time3 = start("slow") + perceptualstep("slow") + cognitivestep("slow") + motorstep("slow")
        print(f"Slowman: {time3}")
        return time1, time2, time3

    elif completeness == "all":
        for perceptual_speed in ["fast", "middle", "slow"]:
            for cognitive_speed in ["fast", "middle", "slow"]:
                for motor_speed in ["fast", "middle", "slow"]:
                    time = start() + perceptualstep(perceptual_speed) + cognitivestep(cognitive_speed) + motorstep(
                        motor_speed)
                    print(
                        f"Perceptual: {perceptual_speed} | Cognitive: {cognitive_speed} | Motor: {motor_speed} | Final time: {time}")


def example3(completeness="extremes"):
    if completeness == "extremes":
        time1 = 2 * perceptualstep("fast") + 2 * cognitivestep("fast") + motorstep("fast")
        print(f"Fastman: {time1}")

        time2 = 2 * perceptualstep("middle") + 2 * cognitivestep("middle") + motorstep("middle")
        print(f"Middleman: {time2}")

        time3 = 2 * perceptualstep("slow") + 2 * cognitivestep("slow") + motorstep("slow")
        print(f"Slowman: {time3}")
        return time1, time2, time3

    elif completeness == "all":
        for perceptual_speed in ["fast", "middle", "slow"]:
            for cognitive_speed in ["fast", "middle", "slow"]:
                for motor_speed in ["fast", "middle", "slow"]:
                    time = start() + 2 * perceptualstep(perceptual_speed) + 2 * cognitivestep(
                        cognitive_speed) + motorstep(motor_speed)
                    print(
                        f"Perceptual: {perceptual_speed} | Cognitive: {cognitive_speed} | Motor: {motor_speed} | Final time: {time}")


def example4(completeness="extremes"):
    times = []
    for second_stimulus_delay in [40, 80, 110, 150, 210, 240]:
        print("===============================================")
        print(f"Second_stimulus_delay = {second_stimulus_delay}")
        if completeness == "extremes":
            relative_delay = second_stimulus_delay - perceptualstep("fast")
            relative_delay = 0 if relative_delay < 0 else relative_delay
            time1 = 2 * perceptualstep("fast") + relative_delay + 2 * cognitivestep("fast") + motorstep("fast")
            print(f"Fastman: {time1}")

            relative_delay = second_stimulus_delay - perceptualstep("middle")
            relative_delay = 0 if relative_delay < 0 else relative_delay
            time2 = 2 * perceptualstep("middle") + relative_delay + 2 * cognitivestep("middle") + motorstep("middle")
            print(f"Middleman: {time2}")

            relative_delay = second_stimulus_delay - perceptualstep("slow")
            relative_delay = 0 if relative_delay < 0 else relative_delay
            time3 = 2 * perceptualstep("slow") + relative_delay + 2 * cognitivestep("slow") + motorstep("slow")
            print(f"Slowman: {time3}")
            # return time1, time2, time3

        elif completeness == "all":
            for perceptual_speed in ["fast", "middle", "slow"]:
                for cognitive_speed in ["fast", "middle", "slow"]:
                    for motor_speed in ["fast", "middle", "slow"]:
                        relative_delay = second_stimulus_delay - perceptualstep(perceptual_speed)
                        relative_delay = 0 if relative_delay < 0 else relative_delay
                        time = 2 * perceptualstep(perceptual_speed) + relative_delay + 2 * cognitivestep(
                            cognitive_speed) + motorstep(motor_speed)
                        times.append(time)
                        print(
                            f"Perceptual: {perceptual_speed} | Cognitive: {cognitive_speed} | Motor: {motor_speed} | Final time: {time}")
    print(f"Max time: ", max(times))


def modify_error(error, type_of_task):
    if type_of_task == "slow":
        return error / 2
    elif type_of_task == "middle":
        return error * 2
    elif type_of_task == "fast":
        return error * 3
    else:
        raise Exception("Bad type")


def example5():
    times = []
    error_probs = []
    for perceptual_speed in ["fast", "middle", "slow"]:
        for cognitive_speed in ["fast", "middle", "slow"]:
            for motor_speed in ["fast", "middle", "slow"]:
                error = 0.01
                error = modify_error(error, perceptual_speed)
                error = modify_error(error, perceptual_speed)
                error = modify_error(error, cognitive_speed)
                error = modify_error(error, cognitive_speed)
                error = modify_error(error, motor_speed)
                if error > 1:
                    error = 1
                time = start() + 2 * perceptualstep(perceptual_speed) + 2 * cognitivestep(
                    cognitive_speed) + motorstep(motor_speed)
                times.append(time)
                error_probs.append(error)
                print(
                    f"Perceptual: {perceptual_speed} | Cognitive: {cognitive_speed} | Motor: {motor_speed} | Final time: {time}")

    plt.plot(times, error_probs, 'o', color='black')
    plt.xlabel("Time in ms")
    plt.ylabel("Error probability")
    plt.show()


if __name__ == '__main__':
    # example1()
    # example2(completeness="all")
    # example3(completeness="all")
    # example4(completeness="all")
    example5()
