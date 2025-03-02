from pprint import pformat

from find_duplicates import get_big_size_duplicates, find_images_duplicate_md5, get_duplicates_per_catalog_depth


def main():
    # 1 Option: ONLY IMAGES:
    # find_images_duplicate_md5()

    # 2 Option: PER CATALOGS MD5!!
    # duplicates_per_dir_depth = get_duplicates_per_catalog_depth()
    # for md5sum_of_dir, paths_per_md5sum in duplicates_per_dir_depth[4].items():
    #     print(md5sum_of_dir, paths_per_md5sum)

    # 3 Option: PER BIG SIZE FILES!
    big_size_duplicates = get_big_size_duplicates()
    print(pformat(big_size_duplicates))
if __name__ == "__main__":
    main()
