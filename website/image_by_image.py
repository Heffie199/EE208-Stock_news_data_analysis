from os import listdir
from typing import Dict, List
import imagehash
import numpy as np
from PIL import Image

def calculate_signature(image_file: str, hash_size: int) -> np.ndarray:
    """
    Calculate the dhash signature of a given file
    Args:
        image_file: the image (path as string) to calculate the signature for
        hash_size: hash size to use, signatures will be of length hash_size^2
    Returns:
        Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
    """
    try:
        pil_image = Image.open(image_file).convert("L").resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS)
        dhash = imagehash.dhash(pil_image, hash_size)
        signature = dhash.hash.flatten()
        pil_image.close()
        return signature
    except IOError as e:
        raise e

def get_pre_data(input_dir: str, hash_size: int, bands: int): #  -> List[Tuple[str, str, float]]
    """
    Find near-duplicate images
    Args:
        input_dir: Directory with images to check
        threshold: Images with a similarity ratio >= threshold will be considered near-duplicates
        hash_size: Hash size to use, signatures will be of length hash_size^2
        bands: The number of bands to use in the locality sensitve hashing process
    Returns:
        A list of near-duplicates found. Near duplicates are encoded as a triple: (filename_A, filename_B, similarity)
    """
    rows: int = int(hash_size ** 2 / bands)
    signatures = dict()
    hash_buckets_list: List[Dict[str, List[str]]] = [dict() for _ in range(bands)]

    # Build a list of candidate files in given input_dir
    try:
        # file_list = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
        file_list = []
        # path = 'img_article'
        # file_list.append(test_path)
        path = input_dir
        folders = listdir(path)
        for folder in folders:
            folders2 = listdir(path+'/'+folder)
            for folder2 in folders2:
                files = listdir(path+'/'+folder+'/'+folder2)
                for file in files:
                    if file.endswith('.jpg'):
                        file_list.append(path+'/'+folder+'/'+folder2+'/'+file)
        # print(file_list)
    except OSError as e:
        raise e

    # Iterate through all files in input directory
    for fh in file_list:
        try:
            # print(fh)
            signature = calculate_signature(fh, hash_size)
            # print(signature)
        except IOError:
            # Not a PIL image, skip this file
            # print('skip')
            # print(fh)
            continue

        # Keep track of each image's signature
        signatures[fh] = np.packbits(signature)
        # print(type(signatures[fh]))

        # Locality Sensitive Hashing
        for i in range(bands):
            signature_band = signature[i * rows:(i + 1) * rows]
            signature_band_bytes = signature_band.tostring()
            if signature_band_bytes not in hash_buckets_list[i]:
                hash_buckets_list[i][signature_band_bytes] = list()
            hash_buckets_list[i][signature_band_bytes].append(fh)
    return signatures,hash_buckets_list

    # Build candidate pairs based on bucket membership
def search(signatures,hash_buckets_list,hash_size,bands,threshold,test_path):
    rows: int = int(hash_size ** 2 / bands)
    candidate_pairs = set()
    signature = calculate_signature(test_path,hash_size)
    signatures[test_path] = np.packbits(signature)
    for i in range(bands):
        signature_band = signature[i * rows:(i + 1) * rows]
        signature_band_bytes = signature_band.tostring()
        if signature_band_bytes not in hash_buckets_list[i]:
            hash_buckets_list[i][signature_band_bytes] = list()
        hash_buckets_list[i][signature_band_bytes].append(test_path)

    for hash_buckets in hash_buckets_list:
        for hash_bucket in hash_buckets.values():
            if test_path in hash_bucket:
                i = 0
                # for i in range(len(hash_bucket)):
                while i < len(hash_bucket):
                    if hash_bucket[i] == test_path:
                        break
                    i += 1
                for j in range(len(hash_bucket)):
                    if j == i:
                        continue
                    candidate_pairs.add(
                        tuple([hash_bucket[i],hash_bucket[j]])
                    )

    # Check candidate pairs for similarity
    near_duplicates = list()
    for cpa, cpb in candidate_pairs:
        hd = sum(np.bitwise_xor(
            np.unpackbits(signatures[cpa]),
            np.unpackbits(signatures[cpb])
        ))
        similarity = (hash_size ** 2 - hd) / hash_size ** 2
        if similarity > threshold:
            near_duplicates.append((cpa, cpb, similarity))

    # Sort near-duplicates by descending similarity and return
    near_duplicates.sort(key=lambda x: x[2], reverse=True)
    return near_duplicates

def main(test_path):
    input_dir = 'static/img_article'
    threshold = 0.7
    hash_size = 16
    bands = 16
    # test_path = '0.jpg' # 存放查找文件路径

    signatures, hash_buckets_list = get_pre_data(input_dir, hash_size, bands)
    near_duplicates = search(signatures, hash_buckets_list, hash_size, bands, threshold, test_path)
    results_img = []
    results_url = []
    results_title = []
    if near_duplicates:
        find_img_path = ''
        for a,b,s in near_duplicates:
            find_img_path = b
            break
        sup = find_img_path[7:].index('/')
        stock_folder = find_img_path[:7+sup+8]
        folders1 = listdir(stock_folder)
        for folder in folders1:
            imgs = listdir(stock_folder+folder)
            flag = False
            for img in imgs:
                if not img.endswith('.txt'):
                    if flag:
                        continue
                    flag = True
                    results_img.append(stock_folder+folder+'/'+img)
                else:
                    with open(stock_folder+folder+'/'+img,'r', encoding='gbk') as f:
                        url = f.readline()
                        f.readline()
                        title = f.readline()
                        results_url.append(url[:-1])
                        results_title.append(title[:-1])
        # print(results_img)
        # print(results_url)
        # print(results_title)
        return results_img,results_url,results_title
    else:
        print('Not found')

if __name__ == "__main__":
    print(main('static/upload/1.jpg'))