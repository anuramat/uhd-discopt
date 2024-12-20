from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import hsv_to_rgb
import numpy as np
import os
import pulp


def load_masks(dir):
    arrays = []
    for name in sorted(os.listdir(dir)):
        if name.lower().endswith(".png"):
            path = os.path.join(dir, name)
            with Image.open(path) as img:
                arrays.append(np.array(img))
    return arrays


def main(debug=False):
    path = "./segments/"
    masks = load_masks(path)

    ilp = pulp.LpProblem("segments", sense=pulp.LpMaximize)
    obj = pulp.LpAffineExpression()

    vars = []

    for i, mask in enumerate(masks):
        var = pulp.LpVariable("mask%d" % i, 0, 1, pulp.LpBinary)
        obj += var * mask.sum()
        vars.append(var)
        for j in range(i):
            if (mask * masks[j]).sum() != 0:
                ilp += var + vars[j] <= 1

    ilp.setObjective(obj)
    ilp.solve(solver=pulp.PULP_CBC_CMD(timeLimit=30) if debug else None)

    image = np.zeros_like(masks[0], dtype=np.int32)
    mask_counter = 0
    for i, var in enumerate(vars):
        if pulp.value(var) == 1:
            mask = masks[i].astype(np.int32)
            mask_counter += 1
            image += mask * mask_counter

    num_colors = mask_counter
    hues = np.linspace(0, 1, num_colors, endpoint=False)  # Equidistant hues
    hsv_colors = np.stack(
        [hues, np.ones(num_colors), np.ones(num_colors)], axis=1
    )  # Full saturation and value
    rgb_colors = hsv_to_rgb(hsv_colors)  # Convert to RGB

    # Create an RGB image based on the assigned values
    rgb_image = np.zeros((*image.shape, 3))
    for i, color in enumerate(rgb_colors, start=1):
        rgb_image[image == i] = color

    plt.imshow(rgb_image)
    plt.colorbar()
    plt.title("objective value: %d" % int(ilp.objective.value()))
    plt.show()


if __name__ == "__main__":
    main()
