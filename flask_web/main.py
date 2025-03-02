from flask import Flask, render_template

from find_duplicates import find_images_duplicate_md5, get_duplicates_per_catalog_depth, get_big_size_duplicates

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/big-files/")
def big_files():
    big_size_duplicates = get_big_size_duplicates()
    return render_template('big_files.html', data=big_size_duplicates)

@app.route("/directories/{depth}")
def directories(depth):
    duplicates_per_dir_depth = get_duplicates_per_catalog_depth()
    if not duplicates_per_dir_depth.get(depth):
        return f"Error, there is no depth of {depth}"
    # TODO!
    # for md5sum_of_dir, paths_per_md5sum in duplicates_per_dir_depth[depth].items():
    #     print(md5sum_of_dir, paths_per_md5sum)
    return render_template('directories.html', size='default')

@app.route("/image-files/")
def image_files():
    images_duplicates = find_images_duplicate_md5()
    # TODO!
    return render_template('image_files.html', data=images_duplicates)

@app.route("/action-move/{md5_sum}/{path}")
def action_move(md5_sum, path):
    # FIXME - this should connect to database and set files of md5sum with new path to move.
    print(f'making action for md5sum-and-path: {md5_sum}/{path}')