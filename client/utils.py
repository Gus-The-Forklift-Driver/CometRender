import logging
import yaml
import bpy
import os


def check_external_files(working_dir):
    # this function check the existance of external files
    # beware that only images,cache files and libraries are checked
    # this function is scuffed as hell
    missing_files = []
    blend_root = os.path.dirname(bpy.data.filepath)
    os.chdir(working_dir)
    for img in bpy.data.images:
        if img.filepath != None and len(img.filepath) > 0:
            relative_filepath = img.filepath.replace('//', './')
            relative_filepath = relative_filepath.replace('\\', '/')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            #logging.info(f'IMAGE | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(os.path.join(os.path.relpath(blend_root, working_dir), relative_filepath))

    for cache in bpy.data.cache_files:
        if cache.filepath != None and len(cache.filepath) > 0:
            relative_filepath = cache.filepath.replace('//', './')
            relative_filepath = relative_filepath.replace('\\', '/')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            #logging.info(f'CACHE | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(os.path.join(os.path.relpath(blend_root, working_dir), relative_filepath))

    for library in bpy.data.libraries:
        if library.filepath != None and len(library.filepath) > 0:
            relative_filepath = library.filepath.replace('//', './')
            relative_filepath = relative_filepath.replace('\\', '/')
            absolute_filepath = os.path.abspath(relative_filepath)
            file_exist = os.path.isfile(absolute_filepath)
            #logging.info(f'library | {relative_filepath} | {absolute_filepath} | {file_exist}')
            if not file_exist:
                missing_files.append(os.path.join(os.path.relpath(blend_root, working_dir), relative_filepath))

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


def set_settings(settings, chunk):
    # set the scene
    # bpy.context.scene = settings['scene']
    current_scene = bpy.data.scenes[settings['scene']]
    # set the settings
    current_scene.render.resolution_x = settings['resolution_x']
    current_scene.render.resolution_y = settings['resolution_y']
    # frame range
    current_scene.frame_start = chunk[0]
    current_scene.frame_end = chunk[1]
    current_scene.frame_step = settings['frame_step']
    # engine
    current_scene.render.engine = settings['render_engine']
    # filepath
    current_scene.render.filepath = settings['output_path']


def clean_path(path):
    pass


if __name__ == '__main__':
    cfg = load_config()
    save_config(cfg)
