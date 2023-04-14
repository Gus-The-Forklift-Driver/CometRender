import logging
import yaml
import bpy
import os


def check_external_files():
    # this function check the existance of external files
    # beware that only images,cache files and libraries are checked
    # this function is scuffed as hell
    missing_files = []
    root = os.path.dirname(bpy.data.filepath)
    os.chdir(root)
    # logging.info(root)
    for img in bpy.data.images:
        if img.filepath != None and len(img.filepath) > 0:
            relative_filepath = img.filepath.replace('//', '')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            # print(f'IMAGE | {os.path.join(root,filepath)}')
            logging.info(f'IMAGE | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(relative_filepath)

    for cache in bpy.data.cache_files:
        if cache.filepath != None and len(cache.filepath) > 0:
            relative_filepath = cache.filepath.replace('//', '')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            logging.info(f'CACHE | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(relative_filepath)

    for library in bpy.data.libraries:
        if library.filepath != None and len(library.filepath) > 0:
            relative_filepath = library.filepath.replace('//', '')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            logging.info(f'library | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(relative_filepath)

    return missing_files


def locate_blend_file(blend: str, root: str = f'.{os.sep}'):
    for root, dirs, files in os.walk(root):
        for file in files:
            if file == blend + '.blend':
                return os.path.join(root, file)
    # no files matching the name were found
    return None


def load_config(file='./config.yml'):
    with open(file, 'r') as config_file:
        config = yaml.load(config_file, yaml.FullLoader)
    return config


def save_config(config, file='./config.yml'):
    with open(file, 'w') as config_file:
        yaml.dump(config, config_file, yaml.Dumper)
    return


def set_settings(settings):
    current_scene = bpy.context.scene
    current_scene.render.resolution_x = settings['output_settings']['resolutionX']


if __name__ == '__main__':
    cfg = load_config()
    save_config(cfg)
