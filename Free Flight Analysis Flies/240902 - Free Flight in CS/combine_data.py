import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def combine_data(exp_names, exp_data):

    # Combine the data from both experiments
    combined_data = np.concatenate(*exp_data)

    exp_list = []
    for name, data in zip(exp_names, exp_data):
        exp_list.append([name]*len(data))

    exp_list = [item for sublist in list_of_lists for item in sublist]

    # Convert to DataFrame for easier manipulation (optional)
    combined_df = pd.DataFrame({
        'angular_velocity': combined_data,
        'experiment': exp_list
    })

    # Calculate mean, median, standard deviation, and standard error for combined data
    mean_value = np.mean(combined_data)
    median_value = np.median(combined_data)
    std_dev = np.std(combined_data, ddof=1)  # Sample standard deviation
    std_error = std_dev / np.sqrt(len(combined_data))  # Standard error

    print(f"Mean of combined data: {mean_value:.4f}")
    print(f"Median of combined data: {median_value:.4f}")
    print(f"Standard Deviation of combined data: {std_dev:.4f}")
    print(f"Standard Error of combined data: {std_error:.4f}")

    # Plotting the data curves for visual comparison
    plt.figure(figsize=(10, 6))

    for name, data in zip(exp_names, exp_data):
        plt.plot(data, label=name, marker='o')
    plt.xlabel('Index')
    plt.ylabel('Angular Velocity')
    plt.title('Angular Velocity Comparison between Experiments')
    plt.legend()
    plt.grid(True)
    plt.savefig('angular_velocity_comparison.png')
    plt.show()

    # Function to perform normality test using Shapiro-Wilk test
    def check_normality(data):
        stat, p_value = stats.shapiro(data)
        print(f'Normality test (Shapiro-Wilk) p-value: {p_value:.4f}')
        if p_value < 0.05:
            print("Data does not follow a normal distribution (Reject H0).")
            return False
        else:
            print("Data follows a normal distribution (Fail to Reject H0).")
            return True

    # Checking normality for combined data
    print("\nNormality Check for Combined Data:")
    is_normal_combined = check_normality(combined_data)

    # Checking normality for individual experiments (optional but informative)
    print("\nNormality Check for Experiment 1:")
    is_normal_exp1 = check_normality(exp1_angular_velocity)

    print("\nNormality Check for Experiment 2:")
    is_normal_exp2 = check_normality(exp2_angular_velocity)

    # Statistical Testing
    if is_normal_combined:
        # Parametric test (e.g., Independent t-test)
        print("\nCombined data is normally distributed. Performing Independent T-test.")
        t_stat, p_value = stats.ttest_ind(exp1_angular_velocity, exp2_angular_velocity)
        print(f"T-test p-value: {p_value:.4f}")
    else:
        # Non-parametric test (e.g., Mann-Whitney U test)
        print("\nCombined data is not normally distributed. Performing Mann-Whitney U test.")
        u_stat, p_value = stats.mannwhitneyu(exp1_angular_velocity, exp2_angular_velocity)
        print(f"Mann-Whitney U test p-value: {p_value:.4f}")

    # Conclusion on Statistical Test
    if p_value < 0.05:
        print("Statistically significant difference between the experiments (Reject H0).")
    else:
        print("No statistically significant difference between the experiments (Fail to Reject H0).")
