# Scikit learn comes with the pre-loaded dataset, load the digits dataset from
# that collection and write a helper function to plot the image using matplotlib.
# [Hint: Explore datasets module from scikit learn]

import matplotlib.pyplot as plt
from sklearn import datasets

# Load digits dataset
digits = datasets.load_digits()

# Helper function to plot digit images
def plot_digit_image(index: int):
    """
    Plots the digit image at a given index from the digits dataset.

    Parameters:
        index (int): Index of the digit image in the dataset.
    """
    image = digits.images[index]
    label = digits.target[index]

    plt.imshow(image, cmap='gray')
    plt.title(f"Digit: {label}")
    plt.axis('off')
    plt.show()


# Example usage:
plot_digit_image(0)   # Plot the first digit image
plot_digit_image(10)  # Plot another digit image
