from sqlalchemy import or_, and_

from config import EXCLUDED_PATHS, DIR_PATHS_PER_MD5SUM_PICKLE, INIT_DIR, DIRS_DUPLICATED_CATALOG_EXCLUDED, \
    MD5DIR_PATH_IGNORED, ACTION_MOVE_DIRS_IGNORED, DIRS_DUPLICATE_IGNORED_NAMES
from fsm_connector.db.models import File
from fsm_connector.pg import PGConnector
from utils import save_pickle, load_pickle
# TODO move into psycopg2 direct access instead of reusing sqlalchemy.


BIG_FILE_SIZE = 1073741824 #1GB
def find_images_duplicate_md5():
    pg_connector = PGConnector()
    session = pg_connector.get_session()
    # TODO find a better way to make those filter with OR
    all_file_paths = (session.query(File.path, File.md5sum, File.extension).filter(
        or_(
            File.extension == 'JPG',
            File.extension == 'JPEG',
            File.extension == 'PNG',
            File.extension == 'IMG',
            File.extension == 'GIF',
            File.extension == 'BMP',
            File.extension == '3GP',
        ),
    ).filter(
        and_(
            ~File.path.like(EXCLUDED_PATHS[0]),
            ~File.path.like(EXCLUDED_PATHS[1]),
            ~File.path.like(EXCLUDED_PATHS[2]),
            ~File.path.like(EXCLUDED_PATHS[3]),
            ~File.path.like(EXCLUDED_PATHS[4]),
            ~File.path.like(EXCLUDED_PATHS[5]),
            ~File.path.like(EXCLUDED_PATHS[6]),
            ~File.path.like(EXCLUDED_PATHS[7]),
            ~File.path.like(EXCLUDED_PATHS[8]),
        )
    ))
    per_md5_key = convert_to_dict_md5_sum_key_path_value(all_file_paths)
    duplicates = {}
    count = 0
    for md5sum, paths in per_md5_key.items():
        if len(paths) > 1:
            duplicates[md5sum] = paths
            count += 1
        if count == 1000:
            return duplicates
    return duplicates

def convert_to_dict_md5_sum_key_path_value(query_selection):
    data = {}
    for [path, md5sum, _] in query_selection:
        try:
            data[md5sum].append(path)
        except KeyError:
            data[md5sum] = [path]

    return data

def get_big_size_duplicates():
    pg_connector = PGConnector()
    session = pg_connector.get_session()
    all_file_paths = (session.query(File.path, File.md5sum, File.size).filter(
        and_(
            File.size >= BIG_FILE_SIZE,
            or_(
                File.to_be_deleted == False,
                File.to_be_deleted == None,
            )

        )
    ).order_by(File.size.desc()))
    per_md5_key = convert_to_dict_md5_sum_key_path_value(all_file_paths)
    duplicates = {}
    for md5sum, paths in per_md5_key.items():
        if len(paths) > 1:
            duplicates[md5sum] = paths
    return duplicates


def md5sum_per_catalog(recursively=False):
    """
    This function will return all catalogs with md5sum of all files in each catalog
    as a dict where md5sum of all files is key per directory

    This only returns md5sums of files in directory - does not do it recursively.
    This means - if key of md5sum of directory has inner directory - files in that inner directory are ignored.
    :return:
    """
    pg_connector = PGConnector()
    session = pg_connector.get_session()
    all_file_paths = (session.query(File.path, File.md5sum, File.name).filter(
        or_(
            File.to_be_deleted == False,
            File.to_be_deleted == None,
        )
    ))
    paths_unique = {}
    for [path, md5sum, name] in all_file_paths:
        path_sub_directories = path.split("/")
        last_subdirectory_counter = -1
        dir_of_file = "/".join(path_sub_directories[0:last_subdirectory_counter])
        dir_of_file_minus_one_depth = "/".join(path_sub_directories[0:last_subdirectory_counter-1])
        if recursively and paths_unique.get(dir_of_file_minus_one_depth):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!RECURSIVELY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", dir_of_file_minus_one_depth)
            paths_unique[dir_of_file_minus_one_depth] += md5sum
        try:
            paths_unique[dir_of_file] += md5sum
        except KeyError:
            paths_unique[dir_of_file] = md5sum
    save_pickle("dir_of_file_per_md5_sum.pickle", paths_unique)
    unique_md5_of_catalog = {}
    for dir_of_file, md5sum_dir in paths_unique.items():
        try:
            unique_md5_of_catalog[md5sum_dir].append(dir_of_file)
        except KeyError:
            unique_md5_of_catalog[md5sum_dir] = [dir_of_file]

    save_pickle(DIR_PATHS_PER_MD5SUM_PICKLE, unique_md5_of_catalog)

def sort_dirs_by_depth(init_dir):
    dir_of_file_per_md5sum = load_pickle("dir_of_file_per_md5_sum.pickle")
    list_of_dirs = sorted(dir_of_file_per_md5sum.keys())
    for unique_dir in list_of_dirs:
        md5sum_of_dir = dir_of_file_per_md5sum.get(unique_dir)
        if init_dir not in unique_dir:
            continue
        this_dir_paths = unique_dir.split(init_dir)[1].split("/")
        file_depth = len(this_dir_paths)
        yield (file_depth, unique_dir, md5sum_of_dir)

def get_duplicates_per_catalog_depth(refresh=False):
    if refresh:
        md5sum_per_catalog(recursively=True)
    duplicates_per_dir_depth = {}
    dir_path_per_md5sums = load_pickle(DIR_PATHS_PER_MD5SUM_PICKLE)
    all_dir_sum_ignored = load_pickle(ACTION_MOVE_DIRS_IGNORED)
    for (file_depth, unique_dir, md5sum_of_dir) in sort_dirs_by_depth(init_dir=INIT_DIR):
        if md5sum_of_dir in all_dir_sum_ignored:
            continue
        if  unique_dir in DIRS_DUPLICATE_IGNORED_NAMES:
            continue
        if md5sum_of_dir in MD5DIR_PATH_IGNORED:
            continue
        excluded = False
        for excluded_catalog_name in DIRS_DUPLICATED_CATALOG_EXCLUDED:
            if excluded_catalog_name in unique_dir:
                excluded = True
        if excluded: continue
        paths_per_md5sum = dir_path_per_md5sums.get(md5sum_of_dir)
        if len(paths_per_md5sum) > 1:
            duplicates_per_dir_depth.setdefault(file_depth, {})
            duplicates_per_dir_depth[file_depth][md5sum_of_dir] = paths_per_md5sum
    return duplicates_per_dir_depth

def get_paths_directories_by_md5sum_of_directory(md5sum_of_directory):
    dir_path_per_md5sums = load_pickle(DIR_PATHS_PER_MD5SUM_PICKLE)
    return dir_path_per_md5sums.get(md5sum_of_directory)
