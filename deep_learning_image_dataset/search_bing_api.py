from requests import exceptions
import argparse
import requests
import cv2
import os
import configparser


# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")

args = vars(ap.parse_args())


# parse config for Microsoft Cognitive Service API
cp = configparser.ConfigParser()
cp.read('search.cnf')

subscription_key = cp.get('image_search_api', 'api_key')
max_results = int(cp.get('image_search_api', 'max_results'))
group_size = int(cp.get('image_search_api', 'group_size'))
search_url = cp.get('image_search_api', 'url')

EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException,
                  exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])

# store the search term
search_term = args['query']
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params = {"q": search_term, "offset": 0, "count": group_size}

print("[INFO] searching bing api for '{}'".format(search_term))
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

estimated_num_results = min(search_results['totalEstimatedMatches'], max_results)
print("[INFO] {} total results for '{}'".format(estimated_num_results, search_term))

# initialize the total number of images downloaded so far.
total = 0

# loop over the estimated number of results
for offset in range(0, estimated_num_results, group_size):
    print("[INFO] making request for group {}-{} of {}...".format(offset, offset + group_size, estimated_num_results))
    params['offset'] = offset
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + group_size, estimated_num_results))

    for v in search_results["value"]:
        try:
            # request to download the image
            print("[INFO] fetching: {}".format(v["contentUrl"]))
            r = requests.get(v["contentUrl"], timeout=30)

            # build the path to the output image
            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            p = os.path.sep.join([args["output"], "{}{}".format(str(total).zfill(8), ext)])

            # write the image to disk
            f = open(p, 'wb')
            f.write(r.content)
            f.close()
        except Exception as e:
            if type(e) in EXCEPTIONS:
                print("[INFO] skipping: {}".format(v['contentUrl']))
                continue

        # try to load the image from disk
        image = cv2.imread(p)

        # if image is None, ignore it.
        if image is None:
            print("[INFO] deleting: {}".format(p))
            os.remove(p)
            continue

        # update the counter
        total += 1
