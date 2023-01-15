import numpy as np
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind


def plot_rdm(rdm_np):
    im = plt.imshow(rdm_np, cmap='hot', interpolation='none')
    plt.colorbar(im)
    plt.show()


def main():
    neural = pd.read_csv("files/NeuralResponses_S1.txt", sep=",")
    categories = pd.read_csv("files/CategoryVectors.txt", sep=",")
    categories.columns = ["animate", "inanim", "human", "nonhumani", "body", "face", "natObj", "artiObj", "rand24",
                          "rand48", "other48", "monkeyape"]
    neural_np = neural.to_numpy()
    sim = np.corrcoef(neural_np)
    dissim = 1 - sim
    #
    # im=plt.imshow(dissim, cmap='hot', interpolation='none')
    # plt.colorbar(im)
    # plt.show()
    animate = categories["animate"].values.tolist()

    diss_of_items_with_same_animation = []
    diss_of_items_with_different_animation = []
    for i in range(len(animate)):
        for j in range(i + 1, len(animate)):
            if animate[i] == animate[j]:
                diss_of_items_with_same_animation.append(dissim[i, j])
            else:
                diss_of_items_with_different_animation.append(dissim[i, j])

    # Perform the t-test
    t_statistic, p_value = ttest_ind(diss_of_items_with_same_animation, diss_of_items_with_different_animation)

    # Print the t-statistic and p-value
    print("t-statistic:", t_statistic)
    print("p-value:", p_value)

    avg_diss_same_anim = sum(diss_of_items_with_same_animation) / len(diss_of_items_with_same_animation)
    avg_diss_diff_anim = sum(diss_of_items_with_different_animation) / len(diss_of_items_with_different_animation)

    values = [avg_diss_same_anim, avg_diss_diff_anim]

    # Define the labels for the x-axis
    x_labels = ['same', 'different']

    # Create the bar plot
    plt.bar(x_labels, values)

    # Add a title and labels for the x-axis and y-axis
    plt.title('Bar plot')

    # Show the plot
    # plt.show()

    behaviour = pd.read_csv("files/BehaviourRDM.csv", sep=",")
    behaviour_np = behaviour.to_numpy()
    plot_rdm(behaviour_np)
    a = ''


def ex_CD():
    neural = pd.read_csv("files/NeuralResponses_S1.txt", sep=",")
    neural_np = neural.to_numpy()
    categories = pd.read_csv("files/CategoryVectors.txt", sep=",")
    categories.columns = ["animate", "inanim", "human", "nonhumani", "body", "face", "natObj", "artiObj", "rand24",
                          "rand48", "other48", "monkeyape"]
    categories = categories.drop("inanim", axis=1)
    behaviour = pd.read_csv("files/BehaviourRDM.csv", sep=",")
    behaviour_np = behaviour.to_numpy()

    sim = np.corrcoef(neural_np)
    dissim = 1 - sim

    neural_diss_of_items_with_any_category = []
    neural_diss_of_items_with_same_category = []
    neural_diss_of_items_with_different_category = []

    behaviour_diss_of_items_with_any_category = []
    behaviour_diss_of_items_with_same_category = []
    behaviour_diss_of_items_with_different_category = []
    for i in range(88):
        for j in range(88):
            neural_diss_of_items_with_any_category.append(dissim[i, j])
            behaviour_diss_of_items_with_any_category.append(behaviour_np[i, j])
            if categories.iloc[i].values.tolist() == categories.iloc[j].values.tolist():
                neural_diss_of_items_with_same_category.append(dissim[i, j])
                behaviour_diss_of_items_with_same_category.append(behaviour_np[i, j])
            else:
                neural_diss_of_items_with_different_category.append(dissim[i, j])
                behaviour_diss_of_items_with_different_category.append(behaviour_np[i, j])

    coef_any_category = np.corrcoef(
        np.asarray(neural_diss_of_items_with_any_category), np.asarray(behaviour_diss_of_items_with_any_category)
    )[0][1]
    coef_same_category = np.corrcoef(
        np.asarray(neural_diss_of_items_with_same_category), np.asarray(behaviour_diss_of_items_with_same_category)
    )[0][1]
    coef_diff_category = np.corrcoef(
        np.asarray(neural_diss_of_items_with_different_category),
        np.asarray(behaviour_diss_of_items_with_different_category)
    )[0][1]
    print("coef_any_category=", coef_any_category)
    print("coef_same_category=", coef_same_category)
    print("coef_diff_category=", coef_diff_category)


if __name__ == '__main__':
    ex_CD()
