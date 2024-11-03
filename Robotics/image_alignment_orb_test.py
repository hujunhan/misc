# import the necessary packages
import numpy as np
import cv2
import skimage
import imutils

image_path = "./data/forward.jpeg"
template_path = "./data/template.jpeg"


def align_images(
    image, template, maxFeatures=500, keepPercent=0.1, name="", debug=False
):
    # convert both the input image and template to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # use ORB to detect keypoints and extract (binary) local
    # invariant features
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    # match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)
    # sort the matches by their distance (the smaller the distance,
    # the "more similar" the features are)
    matches = sorted(matches, key=lambda x: x.distance)
    # keep only the top matches
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]
    # check to see if we should visualize the matched keypoints
    if debug:
        matchedVis = cv2.drawMatches(image, kpsA, template, kpsB, matches, None)
        cv2.imwrite(f"./result/compare/{name}_match.jpg", matchedVis)
        # matchedVis = imutils.resize(matchedVis, width=1000)
        # cv2.imshow("Matched Keypoints", matchedVis)
        # cv2.waitKey(0)
    # allocate memory for the keypoints (x, y)-coordinates from the
    # top matches -- we'll use these coordinates to compute our
    # homography matrix
    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")
    # loop over the top matches
    for i, m in enumerate(matches):
        # indicate that the two keypoints in the respective images
        # map to each other
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt
    # compute the homography matrix between the two sets of matched
    # points
    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
    invH = np.linalg.inv(H)
    # use the homography matrix to align the images
    (h, w) = template.shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    # return the aligned image
    return aligned


def compare_results(template, image, name):
    aligned = align_images(image, template, maxFeatures=500, debug=True, name=name)
    overlay = template.copy()
    output = aligned.copy()
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    cv2.imwrite(f"./result/compare/{name}.jpg", output)
    # show the two output image alignment visualizations
    # cv2.imshow("Image Alignment Overlay", output)
    # cv2.waitKey(0)


if __name__ == "__main__":
    template_inde = [1, 16, 31, 46, 61]
    compar_image_num = 14
    for i in template_inde:
        template = cv2.imread(f"/Users/hu/Downloads/capture_data/{i}/{i}_2d.png")
        for j in range(compar_image_num):
            image = cv2.imread(
                f"/Users/hu/Downloads/capture_data/{i+j+1}/{i+j+1}_2d.png"
            )
            compare_results(template, image, f"{i}_{i+j+1}")
            print(f"compare {i} and {i+j+1}")
