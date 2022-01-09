for i in range(len(x_coords)):          # Plot the keypoints at the x and y coordinates
    cv2.circle(roi_color, (x_coords_denormalized[i], y_coords_denormalized[i]), 2, (255, 255, 0), -1)



# Particular keypoints for scaling and positioning of the filter
left_lip_coords = (int(x_coords_denormalized[11]), int(
    y_coords_denormalized[11]))
right_lip_coords = (int(x_coords_denormalized[12]), int(
    y_coords_denormalized[12]))
top_lip_coords = (int(x_coords_denormalized[13]), int(
    y_coords_denormalized[13]))
bottom_lip_coords = (
    int(x_coords_denormalized[14]), int(y_coords_denormalized[14]))
left_eye_coords = (int(x_coords_denormalized[3]), int(
    y_coords_denormalized[3]))
right_eye_coords = (
    int(x_coords_denormalized[5]), int(y_coords_denormalized[5]))
brow_coords = (int(x_coords_denormalized[6]), int(y_coords_denormalized[6]))



# Scale filter according to keypoint coordinates
beard_width = right_lip_coords[0] - left_lip_coords[0]
glasses_width = right_eye_coords[0] - left_eye_coords[0]



# Used for transparency overlay of filter using the alpha channel
img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2BGRA)



# Beard filter
santa_filter = cv2.imread('filters/santa_filter.png', -1)
santa_filter = cv2.resize(santa_filter, (beard_width*3, 150))
sw, sh, sc = santa_filter.shape



for i in range(0, sw):       # Overlay the filter based on the alpha channel
    for j in range(0, sh):
        if santa_filter[i, j][3] != 0:
            img_copy[top_lip_coords[1]+i+y-20,
                     left_lip_coords[0]+j+x-60] = santa_filter[i, j]

    # Hat filter
    hat = cv2.imread('filters/hat2.png', -1)
    hat = cv2.resize(hat, (w, w))
    hw, hh, hc = hat.shape



    for i in range(0, hw):       # Overlay the filter based on the alpha channel
        for j in range(0, hh):
            if hat[i, j][3] != 0:
                img_copy[i+y-brow_coords[1]*2, j+x -
                         left_eye_coords[0]*1 + 20] = hat[i, j]



    # Glasses filter
    glasses = cv2.imread('filters/glasses.png', -1)
    glasses = cv2.resize(glasses, (glasses_width*2, 150))
    gw, gh, gc = glasses.shape



    for i in range(0, gw):       # Overlay the filter based on the alpha channel
        for j in range(0, gh):
            if glasses[i, j][3] != 0:
                img_copy[brow_coords[1]+i+y-50,
                         left_eye_coords[0]+j+x-60] = glasses[i, j]



    # Revert back to BGR
    img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGRA2BGR)



    # Output with the filter placed on the face
    cv2.imshow('Output', img_copy)
    # Place keypoints on the webcam input
    cv2.imshow('Keypoints predicted', img_copy_1)
