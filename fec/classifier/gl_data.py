import numpy as np
import graphlab as gl
from boto.s3.connection import S3Connection
import os
from filechunkio import FileChunkIO
import math
import shutil
import skimage.io


_conn = None


def get_connection():
    global _conn
    if _conn is None:
        _conn = S3Connection(os.environ['AWS_ACCESS_KEY_ID'],
                             os.environ['AWS_SECRET_ACCESS_KEY'])
    return _conn


def upload_big_file(source_path, bucket):
    source_size = os.stat(source_path).st_size
    mp = bucket.initiate_multipart_upload(os.path.basename(source_path))

    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / chunk_size))
    for i in range(chunk_count + 1):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)

    mp.complete_upload()


def read_data_in_and_save(file_path, raw_dir):
        """Read kaggle training data text file

        """
        image_paths = []
        targets = []

        f = open(file_path)
        f.readline()  # Ignore first

        count = 0
        if os.path.exists(raw_dir):
            shutil.rmtree(raw_dir)

        os.makedirs(raw_dir)
        for line in f:
            s = line.split(',')
            emotion = int(s[0])

            suf = ''
            if len(s) > 2:
                suf = str(s[2]).lower().strip()

            s = s[1].replace('"', '').split()

            data_ = np.array(s, dtype=int).reshape(48, 48)
            data_ = data_.astype('uint8')

            image_path = os.path.join(raw_dir,
                                      'im_' + str(count) +
                                      '_' + suf + '.png')

            skimage.io.imsave(image_path,
                              data_)

            image_paths.append(image_path)
            targets.append(emotion)

            count += 1

        target_path = os.path.join(raw_dir, 'target.txt')
        f = open(target_path, 'w')

        for t in targets:
            print >> f, t
        f.close()

        return image_paths, target_path

if __name__ == '__main__':
    tmp_dir, _ = os.path.split(os.path.abspath(__file__))
    tmp_dir = os.path.join(tmp_dir, '.tmp/')
    if not os.path.exists(tmp_dir):
        tmp_dir = os.mkdir(os.path.join(tmp_dir, '.tmp/'))

    data_path = os.path.join(os.path.dirname(__file__), 'data/fer2013.csv')

    read_data_in_and_save(data_path, tmp_dir)
