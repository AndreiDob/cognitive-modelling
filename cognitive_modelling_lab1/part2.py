### 
### This code is developed by Christian P. Janssen of Utrecht University
### It is intended for students from the Master's course Cognitive Modeling
### Large parts are based on the following research papers:
### Janssen, C. P., & Brumby, D. P. (2010). Strategic adaptation to performance objectives in a dual‐task setting. Cognitive science, 34(8), 1548-1560. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1551-6709.2010.01124.x
### Janssen, C. P., Brumby, D. P., & Garnett, R. (2012). Natural break points: The influence of priorities and cognitive and motor cues on dual-task interleaving. Journal of Cognitive Engineering and Decision Making, 6(1), 5-29. https://journals.sagepub.com/doi/abs/10.1177/1555343411432339
###
### If you want to use this code for anything outside of its intended purposes (training of AI students at Utrecht University), please contact the author:
### c.p.janssen@uu.nl


###
### import packages
###
from matplotlib import pyplot as plt
from numpy import random

import numpy

###
###
### Global parameters. These can be called within functions to change (Python: make sure to call GLOBAL)
###
###


###
### Car / driving related parameters
###
import numpy as np

steeringUpdateTime = 250  # in ms ## How long does one steering update take? (250 ms consistent with Salvucci 2005 Cognitive Science)
timeStepPerDriftUpdate = 50  ### msec: what is the time interval between two updates of lateral position?
startingPositionInLane = 0.27  # assume that car starts already slightly away from lane centre (in meters) (cf. Janssen & Brumby, 2010)

# parameters for deviations in car drift due the simulator environment: See Janssen & Brumby (2010) page 1555
gaussDeviateMean = 0
gaussDeviateSD = 0.13  ##in meter/sec

# When the car is actively controlled, calculate a value using equation (1) in Janssen & Brumby (2010). However, some noise is added on top of this equation to account for variation in human behavior. See Janssen & Brumby (2010) page 1555. Also see function "updateSteering" on how this function is used
gaussDriveNoiseMean = 0
gaussDriveNoiseSD = 0.1  # in meter/sec

### The car is controlled using a steering wheel that has a maximum angle. Therefore, there is also a maximum to the lateral velocity coming from a steering update
maxLateralVelocity = 1.7  # in m/s: maximum lateral velocity: what is the maximum that you can steer?
minLateralVelocity = -1 * maxLateralVelocity

startvelocity = 0  # a global parameter used to store the lateral velocity of the car

###
### Switch related parameters
###
retrievalTimeWord = 200  # ms. ## How long does it take to think of the next word when interleaving after a word (time not spent driving, but drifting)
retrievalTimeSentence = 300  # ms. ## how long does it take to retrieve a sentence from memory (time not spent driving, but drifting)

###
### parameters for typing task
###
timePerWord = 0  ### ms ## How much time does one word take
wordsPerMinuteMean = 39.33  # parameters that control typing speed: when typing two fingers, on average you type this many words per minute. From Jiang et al. (2020; CHI)
wordsPerMinuteSD = 10.3  ## this si standard deviation (Jiang et al, 2020)


## Function to reset all parameters. Call this function at the start of each simulated trial. Make sure to reset GLOBAL parameters.
def resetParameters():
    global timePerWord
    global retrievalTimeWord
    global retrievalTimeSentence
    global steeringUpdateTime
    global startingPositionInLane
    global gaussDeviateMean
    global gaussDeviateSD
    global gaussDriveNoiseMean
    global gaussDriveNoiseSD
    global timeStepPerDriftUpdate
    global maxLateralVelocity
    global minLateralVelocity
    global startvelocity
    global wordsPerMinuteMean
    global wordsPerMinuteSD

    timePerWord = 0  ### ms

    retrievalTimeWord = 200  # ms
    retrievalTimeSentence = 300  # ms

    steeringUpdateTime = 250  # in ms
    startingPositionInLane = 0.27  # assume that car starts already away from lane centre (in meters)

    gaussDeviateMean = 0
    gaussDeviateSD = 0.13  ##in meter/sec
    gaussDriveNoiseMean = 0
    gaussDriveNoiseSD = 0.1  # in meter/sec
    timeStepPerDriftUpdate = 50  ### msec: what is the time interval between two updates of lateral position?
    maxLateralVelocity = 1.7  # in m/s: maximum lateral velocity: what is the maximum that you can steer?
    minLateralVelocity = -1 * maxLateralVelocity
    startvelocity = 0  # a global parameter used to store the lateral velocity of the car
    wordsPerMinuteMean = 39.33
    wordsPerMinuteSD = 10.3


##calculates if the car is not accelerating more than it should (maxLateralVelocity) or less than it should (minLateralVelocity)  (done for a vector of numbers)
def velocityCheckForVectors(velocityVectors):
    global maxLateralVelocity
    global minLateralVelocity

    velocityVectorsLoc = velocityVectors

    if (type(velocityVectorsLoc) is list):
        ### this can be done faster with for example numpy functions
        velocityVectorsLoc = velocityVectors
        for i in range(len(velocityVectorsLoc)):
            if (velocityVectorsLoc[i] > 1.7):
                velocityVectorsLoc[i] = 1.7
            elif (velocityVectorsLoc[i] < -1.7):
                velocityVectorsLoc[i] = -1.7
    else:
        if (velocityVectorsLoc > 1.7):
            velocityVectorsLoc = 1.7
        elif (velocityVectorsLoc < -1.7):
            velocityVectorsLoc = -1.7

    return velocityVectorsLoc


## Function to determine lateral velocity (controlled with steering wheel) based on where car is currently positioned. See Janssen & Brumby (2010) for more detailed explanation. Lateral velocity update depends on current position in lane. Intuition behind function: the further away you are, the stronger the correction will be that a human makes
def vehicleUpdateActiveSteering(LD):
    latVel = 0.2617 * LD * LD + 0.0233 * LD - 0.022
    returnValue = velocityCheckForVectors(latVel)
    return returnValue


### function to update steering angle in cases where the driver is NOT steering actively (when they are distracted by typing for example)
def vehicleUpdateNotSteering():
    global gaussDeviateMean
    global gaussDeviateSD

    vals = numpy.random.normal(loc=gaussDeviateMean, scale=gaussDeviateSD, size=1)[0]
    returnValue = velocityCheckForVectors(vals)
    return returnValue


### Function to run a trial. Needs to be defined by students (section 2 and 3 of assignment)

def run_trial_word(nrWordsPerSentence=5, nrSentences=3, nrSteeringMovementsWhenSteering=2):
    resetParameters()
    locDrifts = []
    trialTime = 0
    time_interval_ms = []
    elapsed_time = 0
    sequence_border = []
    vehicle_position = startingPositionInLane
    wpm = random.normal(wordsPerMinuteMean, wordsPerMinuteSD)
    timePerWord = int(60000 / wpm)
    for sentence_no in range(nrSentences):
        print(f"================= Sentence {sentence_no} ==================")
        for word_no in range(nrWordsPerSentence):
            print(f"--------------- Word {word_no} ---------------")
            time_to_type_word = 0
            # Calculate how long it takes to type a word and add this to the trial time
            if word_no == 0:
                time_to_type_word += retrievalTimeSentence
            time_to_type_word += retrievalTimeWord
            time_to_type_word += timePerWord
            print("time_to_type_word", time_to_type_word)

            print("Deviation updates:")
            # Calculate the deviation of the car in the time we are typing that word
            number_of_updates = time_to_type_word // 50
            for update_no in range(number_of_updates):
                lateral_velocity = vehicleUpdateNotSteering()  # in m/s
                deviation_on_this_update = lateral_velocity * 50 / 1000  # in meters
                # We consider vehicle position as negative/positive = left/right.
                vehicle_position += deviation_on_this_update
                print("Update NO", update_no)
                print("deviation_on_this_update", deviation_on_this_update)
                print("vehicle_position", vehicle_position)
                locDrifts.append(vehicle_position)
                elapsed_time += 50
                time_interval_ms.append(elapsed_time)
            sequence_border.append(elapsed_time)

            print("Correction updates:")
            # We finished typing the word and drifting away, now we focus on steering back
            for steering_movement_no in range(nrSteeringMovementsWhenSteering):
                print("Steering phase ", steering_movement_no)
                lateral_velocity = vehicleUpdateActiveSteering(vehicle_position)
                no_updates_per_this_steering_movement = steeringUpdateTime // 50
                for update_no in range(no_updates_per_this_steering_movement):
                    deviation_on_this_update = lateral_velocity * 50 / 1000  # in meters
                    # We consider vehicle position as negative/positive = left/right. Therefore, in order to make
                    # the corrections properly, we need to go left if we are to the right of the lane center
                    # and vice-versa
                    # If they have the same sign, reverse the sign of the deviation in order to steer to the centre
                    if (vehicle_position > 0) == (deviation_on_this_update > 0):
                        deviation_on_this_update = -1 * deviation_on_this_update
                    vehicle_position += deviation_on_this_update
                    locDrifts.append(vehicle_position)
                    print("Update NO", update_no)
                    print("deviation_on_this_update", deviation_on_this_update)
                    print("vehicle_position", vehicle_position)
                    elapsed_time += 50
                    time_interval_ms.append(elapsed_time)
            sequence_border.append(elapsed_time)

            # Update trial time
            trialTime += time_to_type_word + nrSteeringMovementsWhenSteering * steeringUpdateTime

    print("trialTime", trialTime)
    print("elapsed_time", elapsed_time)
    # Plot stuff
    # time_interval_ms = [50 * i for i in range(len(locDrifts))]
    plt.plot(time_interval_ms, locDrifts, '-', color='blue')
    plt.xlabel("Time in ms")
    plt.ylabel("Lane position")

    # For debugging: it prints the border between drift-steer phases
    for border in sequence_border:
        plt.vlines(x=border, ymin=0.1, ymax=0.5,
                   colors='purple',
                   label='border')

    plt.text(-2.5, 0.4,
             f"Total trial time = {trialTime}; Mean position on the road = {sum(locDrifts) / len(locDrifts)}; Max position on the road (Absolute) = {max(locDrifts)}",
             bbox=dict(facecolor='red', alpha=0.5))
    plt.show()


def run_trial_sentence(nrWordsPerSentence=5, nrSentences=3, nrSteeringMovementsWhenSteering=2):
    resetParameters()
    locDrifts = []
    trialTime = 0
    time_interval_ms = []
    elapsed_time = 0
    sequence_border = []
    vehicle_position = startingPositionInLane
    wpm = random.normal(wordsPerMinuteMean, wordsPerMinuteSD)
    timePerWord = int(60000 / wpm)
    for sentence_no in range(nrSentences):
        print(f"================= Sentence {sentence_no} ==================")
        for word_no in range(nrWordsPerSentence):
            print(f"--------------- Word {word_no} ---------------")
            time_to_type_word = 0
            # Calculate how long it takes to type a word and add this to the trial time
            if word_no == 0:
                time_to_type_word += retrievalTimeSentence
            time_to_type_word += timePerWord
            print("time_to_type_word", time_to_type_word)

            print("Deviation updates:")
            # Calculate the deviation of the car in the time we are typing that word
            number_of_updates = time_to_type_word // 50
            for update_no in range(number_of_updates):
                lateral_velocity = vehicleUpdateNotSteering()  # in m/s
                deviation_on_this_update = lateral_velocity * 50 / 1000  # in meters
                # We consider vehicle position as negative/positive = left/right.
                vehicle_position += deviation_on_this_update
                print("Update NO", update_no)
                print("deviation_on_this_update", deviation_on_this_update)
                print("vehicle_position", vehicle_position)
                locDrifts.append(vehicle_position)
                elapsed_time += 50
                time_interval_ms.append(elapsed_time)
                
        sequence_border.append(elapsed_time)
        print("Correction updates:")
        # We finished typing the sentence and drifting away, now we focus on steering back
        for steering_movement_no in range(nrSteeringMovementsWhenSteering):
            print("Steering phase ", steering_movement_no)
            lateral_velocity = vehicleUpdateActiveSteering(vehicle_position)
            no_updates_per_this_steering_movement = steeringUpdateTime // 50
            for update_no in range(no_updates_per_this_steering_movement):
                deviation_on_this_update = lateral_velocity * 50 / 1000  # in meters
                # We consider vehicle position as negative/positive = left/right. Therefore, in order to make
                # the corrections properly, we need to go left if we are to the right of the lane center
                # and vice-versa
                # If they have the same sign, reverse the sign of the deviation in order to steer to the centre
                if (vehicle_position > 0) == (deviation_on_this_update > 0):
                    deviation_on_this_update = -1 * deviation_on_this_update
                vehicle_position += deviation_on_this_update
                locDrifts.append(vehicle_position)
                print("Update NO", update_no)
                print("deviation_on_this_update", deviation_on_this_update)
                print("vehicle_position", vehicle_position)
                elapsed_time += 50
                time_interval_ms.append(elapsed_time)
        sequence_border.append(elapsed_time)

        # Update trial time
        trialTime += time_to_type_word + nrSteeringMovementsWhenSteering * steeringUpdateTime


    print("trialTime", trialTime)
    print("elapsed_time", elapsed_time)
    # Plot stuff
    # time_interval_ms = [50 * i for i in range(len(locDrifts))]
    plt.plot(time_interval_ms, locDrifts, '-', color='blue')
    plt.xlabel("Time in ms")
    plt.ylabel("Lane position")

    # # For debugging: it prints the border between drift-steer phases
    # for border in sequence_border:
    #     plt.vlines(x=border, ymin=0.1, ymax=0.5,
    #                colors='purple',
    #                label='border')

    plt.text(-2.5, 0.6,
             f"Total trial time = {trialTime}; Mean position on the road = {sum(locDrifts) / len(locDrifts)}; Max position on the road (Absolute) = {max(locDrifts)}",
             bbox=dict(facecolor='red', alpha=0.5))
    plt.show()


def runTrial(nrWordsPerSentence=5, nrSentences=3, nrSteeringMovementsWhenSteering=2, interleaving="word"):
    if interleaving == "word":
        run_trial_word(nrWordsPerSentence, nrSentences, nrSteeringMovementsWhenSteering)
    elif interleaving == "sentence":
        run_trial_sentence(nrWordsPerSentence, nrSentences, nrSteeringMovementsWhenSteering)


### function to run multiple simulations. Needs to be defined by students (section 3 of assignment)
def runSimulations(nrSims=100):
    print("hello world")


if __name__ == '__main__':
    for i in range(100):
        runTrial(nrWordsPerSentence=17, nrSentences=10, nrSteeringMovementsWhenSteering=4, interleaving="word")
