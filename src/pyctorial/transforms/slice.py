def slice(img, slices=10):

    width, height = img.size
    slice_width = width // slices

    result = []

    for i in range(slices):

        left = i * slice_width
        right = left + slice_width

        crop = img.crop((left, 0, right, height))

        result.append(crop)

    return result