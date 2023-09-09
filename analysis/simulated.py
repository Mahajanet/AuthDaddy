import numpy as np
import pandas as pd

def simulate_data(num_init, num_samples, num_hackers, password_length):
    mean_press_time = 150  # Mean press time in milliseconds
    std_deviation_press_time = 30  # Standard deviation of press time in milliseconds
    mean_release_time = 50  # Mean release time in milliseconds
    std_deviation_release_time = 10  # Standard deviation of release time in milliseconds

    # Define parameters for the binomial distribution for hackers
    mean_press_time_hacker = np.random.randint(120, 180, num_hackers)  # Mean press time for each hacker
    std_deviation_press_time_hacker = np.random.randint(20, 40, num_hackers)  # Std dev for press time
    mean_release_time_hacker = np.random.randint(40, 60, num_hackers)  # Mean release time for each hacker
    std_deviation_release_time_hacker = np.random.randint(8, 12, num_hackers)  # Std dev for release time

    # Simulate data for a person entering the password
    person_init = []
    for _ in range(num_init):
        entry_vector = []
        for char in range(password_length):
            press_time = int(np.random.normal(mean_press_time, std_deviation_press_time)) + char * 200
            release_time = int(np.random.normal(mean_release_time, std_deviation_release_time))
            entry_vector.extend([0, press_time, press_time + release_time])
        person_init.append(entry_vector)

    # Simulate data for a person entering the password
    person_data = []
    for _ in range(num_samples):
        entry_vector = []
        for char in range(password_length):
            press_time = int(np.random.normal(mean_press_time, std_deviation_press_time)) + char*200
            release_time = int(np.random.normal(mean_release_time, std_deviation_release_time))
            entry_vector.extend([0, press_time, press_time + release_time])
        person_data.append(entry_vector)

    # Simulate data for other people knowing the password with multimodal distribution
    hacker_data = []
    for _ in range(num_samples):
        entry_vector = []
        for char in range(password_length):
            hacker_idx = np.random.randint(0, num_hackers)
            press_time = int(
                np.random.normal(mean_press_time_hacker[hacker_idx], std_deviation_press_time_hacker[hacker_idx])) + char*200
            release_time = int(
                np.random.normal(mean_release_time_hacker[hacker_idx], std_deviation_release_time_hacker[hacker_idx]))
            entry_vector.extend([0, press_time, press_time + release_time])
        hacker_data.append(entry_vector)

    labels = []
    for i in range(password_length):
        labels.extend([f"error{i}", f"start{i}", f"end{i}"])

    init_df = pd.DataFrame(person_init, columns=labels)
    person_df = pd.DataFrame(person_data, columns=labels)
    hacker_df = pd.DataFrame(hacker_data, columns=labels)

    # Add a label column to distinguish between person and hacker data
    person_df["label"] = "Person"
    hacker_df["label"] = "Hacker"

    # Concatenate the DataFrames
    combined_df = pd.concat([person_df, hacker_df], ignore_index=True)

    # Shuffle the rows in the combined DataFrame
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)

    # Print the first few rows of the combined DataFrame
    print(combined_df.head())
    return init_df, combined_df

def evaluate_tests():
    train, test = simulate_data(10, 50, 50, 10)
    print(train)
    print(test)

if __name__ == "__main__":
    evaluate_tests()
