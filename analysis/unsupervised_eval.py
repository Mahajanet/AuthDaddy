import pandas as pd
import numpy as np
from scipy.stats import chi2
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from scipy.stats import norm
from sklearn.decomposition import PCA
import simulated

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

