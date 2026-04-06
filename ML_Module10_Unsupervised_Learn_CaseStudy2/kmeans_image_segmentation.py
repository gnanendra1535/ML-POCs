# kmeans image segmentation
# kmeans_image_segmentation.py
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ---------- Config ----------
INPUT_IMG = '/dogs.jpeg'
K = 3
RANDOM_STATE = 42
# Optionally resize large images for speed (set None to keep original)
MAX_DIM = 600  


def load_image(path, max_dim=None):
    img = Image.open(path).convert('RGB')
    if max_dim is not None:
        # resize preserving aspect ratio if either side > max_dim
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    return img

def image_to_array(img):
    arr = np.asarray(img, dtype=np.float32)  # shape (H, W, 3)
    return arr

def array_to_image(arr):
    # clip & convert to uint8
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def kmeans_segment(img_arr, k=3, random_state=42):
    H, W, C = img_arr.shape
    assert C == 3, "Expected RGB channels"
    flat = img_arr.reshape(-1, 3)  # shape (H*W, 3)

    # Fit KMeans on pixel colors
    kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(flat)        # labels per pixel
    centers = kmeans.cluster_centers_        # shape (k, 3) float32

    # Recreate segmented image by replacing each pixel with its cluster center
    segmented_flat = centers[labels]
    segmented = segmented_flat.reshape(H, W, 3)

    # Count proportions
    unique, counts = np.unique(labels, return_counts=True)
    proportions = dict(zip(unique, counts / counts.sum()))

    return {
        "labels": labels.reshape(H, W),
        "centers": centers,
        "segmented": segmented,
        "proportions": proportions
    }

def plot_results(original_img, segmented_img_arr, centers, proportions):
    # Convert arrays/images for plotting
    original_arr = np.asarray(original_img)
    seg_img = array_to_image(segmented_img_arr)

    # Plot original and segmented side-by-side
    fig, axes = plt.subplots(1, 3, figsize=(15,5))
    axes[0].imshow(original_arr)
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    axes[1].imshow(seg_img)
    axes[1].set_title(f"Segmented (k={K})")
    axes[1].axis('off')

    # Plot dominant color palette with proportions
    # Create a horizontal palette image
    palette_h = 100
    palette = np.zeros((palette_h, 300, 3), dtype=np.uint8)
    x_start = 0
    # Sort centers by proportion descending for nicer palette ordering
    centers_int = centers.astype(int)
    # prepare ordering
    items = sorted(proportions.items(), key=lambda x: -x[1])
    for idx, prop in items:
        width = int(prop * palette.shape[1])
        color = centers_int[int(idx)]
        palette[:, x_start:x_start+width, :] = color
        x_start += width
    axes[2].imshow(palette)
    axes[2].set_title("Dominant colors (width ~ proportion)")
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

def print_dominant_colors(centers, proportions):
    # centers are in RGB float space
    centers_int = centers.astype(int)
    # Order by proportion desc
    items = sorted(proportions.items(), key=lambda x: -x[1])
    print("Dominant colors (RGB) and proportions:")
    for idx, prop in items:
        rgb = tuple(centers_int[int(idx)])
        print(f"  Cluster {idx}: RGB={rgb}, proportion={prop:.3f}")

def main():
    # Load image
    img = load_image(INPUT_IMG, max_dim=MAX_DIM)
    print("Image size (W x H):", img.size)

    # Convert to numpy array
    arr = image_to_array(img)
    H, W, C = arr.shape
    print("Array shape:", arr.shape)  # (H, W, 3)

    # Flatten -> 2D array happens inside kmeans_segment (flat = H*W x 3)

    # KMeans clustering (k=3)
    result = kmeans_segment(arr, k=K, random_state=RANDOM_STATE)

    # Predict cluster label of every pixel already done; reconstruct shown below
    segmented_arr = result['segmented']

    # Find three dominant colors (cluster centers)
    centers = result['centers']       # float RGB centers
    proportions = result['proportions']

    print_dominant_colors(centers, proportions)

    # Plot original, segmented, and palette
    plot_results(img, segmented_arr, centers, proportions)

    # Save outputs
    seg_img_pil = array_to_image(segmented_arr)
    seg_img_pil.save('/dogs_segmented.png')
    # Save palette as an image
    # create palette image again for saving (simple equal-height strip)
    palette_h = 80
    palette = np.zeros((palette_h, 300, 3), dtype=np.uint8)
    x_start = 0
    items = sorted(proportions.items(), key=lambda x: -x[1])
    centers_int = centers.astype(int)
    for idx, prop in items:
        width = int(prop * palette.shape[1])
        color = centers_int[int(idx)]
        palette[:, x_start:x_start+width, :] = color
        x_start += width
    Image.fromarray(palette).save('/dogs_palette.png')

    print("Saved segmented image to /dogs_segmented.png")
    print("Saved color palette to /dogs_palette.png")

if __name__ == "__main__":
    main()
