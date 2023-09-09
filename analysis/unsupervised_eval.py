import pandas as pd
import numpy as np
from scipy.stats import chi2
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from scipy.stats import norm
from sklearn.decomposition import PCA


class UnsupervisedML:

    def __init__(self, df):
        self.df = df

    def select_best_model(self, training_trials, training_outputs):
        SVM_entries = []
        PCA_entries = []
        maha_entries = []
        GMM = []

        for row in training_trials:
            SVM_entries.append(self.one_class_SVM(row))
            PCA_entries.append(self.PCA(row))
            maha_entries.append(self.mahalanobis_dist(row))
            GMM.append(self.GMM(row))

        SVM_m = self.confusion_matrix(SVM_entries, training_outputs)
        PCA_m = self.confusion_matrix(PCA_entries, training_outputs)
        maha_m = self.confusion_matrix(PCA_entries, training_outputs)
        GMM_m = self.confusion_matrix(GMM, training_outputs)

        print(SVM_m)
        print(PCA_m)
        print(maha_m)
        print(GMM_m)

    @staticmethod
    def confusion_matrix(result, expected):
        tp, fp, fn, tn = 0, 0, 0, 0
        for idx in range(len(result)):
            if result[idx] >= 0.5 and expected[idx] >= 1.0:
                tp += 1
            elif result[idx] < 0.5 and expected[idx] >= 1.0:
                fp += 1
            elif result[idx] >= 0.5 and expected[idx] <= 0.0:
                fn += 1
            else:
                tn += 1
        return {"true_positive": tp, "false_positive": fp, "false_negative": fn, "true_negative": tn}

    def one_class_SVM(self, vector):
        # Fit a One-Class SVM model
        svm_model = OneClassSVM(nu=0.05)  # Adjust the 'nu' hyperparameter as needed
        svm_model.fit(self.df)

        # Calculate the decision function score for the new data vector
        distance_score = svm_model.decision_function([vector])[0]

        outlier_probability = norm.cdf(distance_score)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def PCA(self, vector):
        # Fit a PCA model to your data
        n_components = 2  # Adjust the number of principal components as needed
        pca_model = PCA(n_components=n_components)
        pca_model.fit(self.df)

        # Project the new data vector onto the principal components
        new_data_projected = pca_model.transform([vector])

        # Reconstruct the data vector using the principal components
        reconstructed_data = pca_model.inverse_transform(new_data_projected)

        # Calculate the reconstruction error for the new data vector
        reconstruction_error = np.mean(np.square(vector - reconstructed_data))

        # Convert the reconstruction error to an outlier probability
        # You can adjust this conversion based on your data distribution and needs
        outlier_probability = 1.0 - np.exp(-reconstruction_error)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def mahalanobis_dist(self, vector):
        # Calculate the mean and covariance matrix of the data vectors
        mean_vector = np.mean(self.df, axis=0)
        cov_matrix = np.cov(self.df, rowvar=False)

        # Calculate the Mahalanobis distance for the new data vector
        diff_vector = vector - mean_vector
        mahalanobis_distance = np.sqrt(np.dot(np.dot(diff_vector, np.linalg.inv(cov_matrix)), diff_vector))

        # Degrees of freedom for the chi-squared distribution
        df_chi2 = len(self.df.columns)

        # Convert Mahalanobis distance to an outlier probability
        outlier_probability = 1.0 - chi2.cdf(mahalanobis_distance ** 2, df_chi2)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def GMM(self, vector):
        gmm = GaussianMixture(n_components=2)  # You can adjust the number of components
        gmm.fit(self.df)

        # Calculate the log probability density for the new data vector
        log_prob = gmm.score_samples([vector])

        # Calculate the outlier probability (normalized percentile rank)
        outlier_probability = len(log_prob[log_prob <= log_prob[0]]) / len(log_prob)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

def simulate_data(num_init, num_samples, num_hackers):
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
        for char in range(10):
            press_time = int(np.random.normal(mean_press_time, std_deviation_press_time)) + char * 200
            release_time = int(np.random.normal(mean_release_time, std_deviation_release_time))
            entry_vector.extend([char + 1, press_time, press_time + release_time])
        person_init.append(entry_vector)

    # Simulate data for a person entering the password
    person_data = []
    for _ in range(num_samples):
        entry_vector = []
        for char in range(10):
            press_time = int(np.random.normal(mean_press_time, std_deviation_press_time)) + char*200
            release_time = int(np.random.normal(mean_release_time, std_deviation_release_time))
            entry_vector.extend([char + 1, press_time, press_time + release_time])
        person_data.append(entry_vector)

    # Simulate data for other people knowing the password with multimodal distribution
    hacker_data = []
    for _ in range(num_samples):
        entry_vector = []
        for char in range(10):
            hacker_idx = np.random.randint(0, num_hackers)
            press_time = int(
                np.random.normal(mean_press_time_hacker[hacker_idx], std_deviation_press_time_hacker[hacker_idx])) + char*200
            release_time = int(
                np.random.normal(mean_release_time_hacker[hacker_idx], std_deviation_release_time_hacker[hacker_idx]))
            entry_vector.extend([char + 1, press_time, press_time + release_time])
        hacker_data.append(entry_vector)

    init_df = pd.DataFrame(person_init, columns=["Char", "Press_Time", "Release_Time"] * 10)
    person_df = pd.DataFrame(person_data, columns=["Char", "Press_Time", "Release_Time"] * 10)
    hacker_df = pd.DataFrame(hacker_data, columns=["Char", "Press_Time", "Release_Time"] * 10)

    # Add a label column to distinguish between person and hacker data
    person_df["Label"] = "Person"
    hacker_df["Label"] = "Hacker"

    # Concatenate the DataFrames
    combined_df = pd.concat([person_df, hacker_df], ignore_index=True)

    # Shuffle the rows in the combined DataFrame
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)

    # Print the first few rows of the combined DataFrame
    print(combined_df.head())
    return init_df, combined_df


def evaluate_tests():
    train, test = simulate_data(10, 50, 50)
    print(train)
    print(test)

evaluate_tests()
