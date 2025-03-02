from os import path as os_path
from pprint import pformat

from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy.sql.operators import like_op

from config import INIT_DIR, CLEAN_DIR, ACTION_MOVE_DIRS_IGNORED
from find_duplicates import find_images_duplicate_md5, get_duplicates_per_catalog_depth, get_big_size_duplicates, \
    md5sum_per_catalog, get_paths_directories_by_md5sum_of_directory
from fsm_connector.db.models import File
from fsm_connector.pg import PGConnector
from utils import save_pickle, load_pickle

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/big-files/")
def big_files():
    big_size_duplicates = get_big_size_duplicates()
    return render_template('big_files.html', default_path_prefix=INIT_DIR+CLEAN_DIR, data=big_size_duplicates)

@app.route("/directories/refresh")
def directories_refresh():
    md5sum_per_catalog(recursively=True)
    return "Refreshed"

@app.route("/directories/<int:depth>/")
def directories(depth):
    duplicates_per_dir_depth = get_duplicates_per_catalog_depth()
    list_of_depths = sorted(duplicates_per_dir_depth.keys())
    data = duplicates_per_dir_depth.get(depth)
    if not data:
        return f"Error, there is no depth of {depth}"
    # TODO!
    # for md5sum_of_dir, paths_per_md5sum in duplicates_per_dir_depth[depth].items():
    #     print(md5sum_of_dir, paths_per_md5sum)
    return render_template('directories.html', default_path_prefix=INIT_DIR+CLEAN_DIR, data=data, depth=depth, list_of_depths=list_of_depths)

@app.route("/image-files/")
def image_files():
    images_duplicates = find_images_duplicate_md5()
    return render_template('image_files.html', default_path_prefix=INIT_DIR+CLEAN_DIR, data=images_duplicates)

@app.route("/action-move/", methods = ['POST'])
def action_move():
    md5_sum = request.form.get('md5_sum')
    move_path = request.form.get('move_path')
    previous_url_path = request.form.get('previous_url_path')
    move_filename = request.form.get('move_filename')
    previous_url_depth = request.form.get('previous_url_depth')
    # FIXME - this should connect to database and set files of md5sum with new path to move.
    # TODO - for now making it here. Move this logic into FSM_cleanup GRPC service lateron.
    # 1. Check if new path exists
    # if not os_path.exists(move_path):
    #     return "Error, path does not exist"
    # 2. Connect to DB and set move path:
    pg_connector = PGConnector()
    session = pg_connector.get_session()
    if previous_url_path == "big_files" or previous_url_path == "image_files":
        session.query(File).filter(File.md5sum == md5_sum).update(
            {
                File.new_path_after_deleted: move_path,
                File.new_filename_after_deleted: move_filename,
                File.to_be_deleted: True,
            }, synchronize_session=False
        )
        session.commit()
        session.close()
    elif previous_url_path == "directories":
        # md5_sum in this situation is a sum of all dir file md5sums.
        try:
            all_dir_sums = load_pickle(ACTION_MOVE_DIRS_IGNORED)
        except FileNotFoundError:
            all_dir_sums = []
        list_dirs = get_paths_directories_by_md5sum_of_directory(md5_sum)
        for dir_name in list_dirs:
            for file_in_dir in session.query(File).filter(
                    File.path.like(dir_name + "%")
            ).all():
                # using md5sum of file to find any other files in other directories that may need to be moved here:
                session2 = pg_connector.get_session()
                session2.query(File).filter(File.md5sum == file_in_dir.md5sum).update(
                    {
                        File.new_path_after_deleted: move_path,
                        File.new_filename_after_deleted: move_filename,
                        File.to_be_deleted: True,
                    }, synchronize_session=False
                )
                session2.commit()
                session2.close()
        all_dir_sums.append(md5_sum)
        save_pickle(ACTION_MOVE_DIRS_IGNORED, all_dir_sums)
        session.close()
    return redirect(url_for(previous_url_path, depth=previous_url_depth))
