import numpy as np
import graphlab as gl
from boto.s3.connection import S3Connection
import os
from filechunkio import FileChunkIO
import math
import shutil
import skimage.io
import fec.media.helpers.utilities as utilities
import pandas as pd


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


def _load_original_data_into_df(file_path):
    df = pd.read_csv(file_path)
    df = df.rename(columns={'Usage': 'usage', 'Emotion': 'label'})
    df['pixels'] = df['pixels'].apply(lambda x:
                                      np.fromstring(x, sep=' ', dtype=int))
    return df


# def read_data_in_and_save(file_path, raw_dir, rotate=None):
#         """Read kaggle training data text file
#
#         """
#         image_paths = []
#         targets = []
#
#         f = open(file_path)
#         f.readline()  # Ignore first
#
#         count = 0
#         if os.path.exists(raw_dir):
#             shutil.rmtree(raw_dir)
#
#         os.makedirs(raw_dir)
#
#         if rotate is not None:
#             rot_mat = [utilities.get_rotation_matrix(48, 48, r)
#                        for r in rotate]
#
#         for line in f:
#             s = line.split(',')
#             emotion = int(s[0])
#
#             suf = ''
#             if len(s) > 2:
#                 suf = str(s[2]).lower().strip()
#
#             s = s[1].replace('"', '').split()
#
#             data_ = np.array(s, dtype=int).reshape(48, 48)
#             data_ = data_.astype('uint8')
#
#             image_path = os.path.join(raw_dir,
#                                       'im_' + str(count) +
#                                       '_' + suf + '.png')
#
#             skimage.io.imsave(image_path,
#                               data_)
#             image_paths.append(image_path)
#             targets.append(emotion)
#
#             if rotate is not None:
#                 cnt = 0
#                 flip_image = utilities.flip_image(data_)
#                 for m in rot_mat:
#                     img_rot = utilities.rotate_image(data_, m)
#                     image_path = os.path.join(raw_dir,
#                                               'im_' + str(count) +
#                                               '_' + suf + '_' + str(cnt) +
#                                               '.png')
#
#                     skimage.io.imsave(image_path, img_rot)
#
#                     image_paths.append(image_path)
#                     targets.append(emotion)
#                     cnt += 1
#
#                     img_rot = utilities.rotate_image(flip_image, m)
#                     image_path = os.path.join(raw_dir, 'im_' + str(count) +
#                                               '_' + suf + '_' + str(cnt) +
#                                               '.png')
#
#                     skimage.io.imsave(image_path, img_rot)
#
#                     image_paths.append(image_path)
#                     targets.append(emotion)
#                     cnt += 1
#
#             count += 1
#
#         target_path = os.path.join(raw_dir, 'target.txt')
#         f = open(target_path, 'w')
#
#         for t in targets:
#             print >> f, t
#         f.close()
#
#         return image_paths, target_path


if __name__ == '__main__':
    # tmp_dir = os.environ['HOME']
    # tmp_dir = os.path.join(tmp_dir, '.tmp/')
    # if not os.path.exists(tmp_dir):
    #     os.mkdir(tmp_dir)
    #
    # data_path = os.path.join(os.path.dirname(__file__), 'data/fer2013.csv')
    #
    # rotations = [90, 180, 270]
    #
    # img_paths, target_path = read_data_in_and_save(data_path, tmp_dir,
    #                                                rotate=rotations)
    # sf = create_sframe(img_paths, target_path)
    #
    # sf.save('s3://cmgreen210-emotions/sframe-full')
    #
    # #
    # # rot_mat = [get_rotation_matrix(48, 48, r) for r in rotations]
    # #
    # # for s in sf:
    # #     image = s['images']
    # #
    #
    # if os.path.exists(tmp_dir):
    #     shutil.rmtree(tmp_dir)
    # # read_data_in_and_save_csv('/Users/chris/Downloads/fer2013/fer2013.csv',
    # #                           '/Users/chris/tmp/raw/')
    fer_data = '/Users/chris/Downloads/fer2013/fer2013.csv'
    df = _load_original_data_into_df(fer_data)
    sf = gl.SFrame(df)
    sf.save('s3://cmgreen210-emotions/sframe_3col_35k')
