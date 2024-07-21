import os.path
import shutil
import zipfile

__all__ = ('unpack',)

def _zip_security_check(zip_path, member_name):
    def fail(msg):
        # Note: We _intentionally_ don't print the member_name here,
        # as it could be used to abuse the error message to give the
        # user malicious instructions.
        # It's up to the user to complain about the error message to
        # the mod author, who can fix the zip if they're not malicious.
        raise EnvironmentError("Zip file {} contains {} in a member path. For security reasons this is not allowed.".format(zip_path, msg))
    if '..' in member_name:
        fail('".." (directory climbing)')
    if '\\' in member_name:
        fail('"\\" (backslash)')
    if member_name.startswith('/'):
        fail('absolute paths')
    if member_name.startswith('./'):
        fail('relative paths')
    return True

def _unpack_zip_path_to_path(zip_file, subpath, target_path, debug=False):
    if subpath and subpath[-1] != '/':
        subpath += '/'
    for name in zip_file.namelist():
        if name.startswith(subpath) and name != subpath:
            zipinfo_obj = zip_file.getinfo(name)
            old_filename = zipinfo_obj.filename
            zipinfo_obj.filename = name[len(subpath):]
            if debug:
                print(zipinfo_obj.filename, '=>', os.path.join(target_path, zipinfo_obj.filename))
            zip_file.extract(name, target_path)
            zipinfo_obj.filename = old_filename

def unpack(zip_path, verbose=False, debug=False):
    # Check for an unpacked folder at the same location as the zip but without the .zip extension
    folder_path = zip_path[:-4]
    if os.path.isdir(folder_path):
        # Check if the zip file is newer than the folder
        if os.path.getmtime(zip_path) < os.path.getmtime(folder_path):
            if verbose:
                print('Folder "{}" is up to date from zip "{}". Skipping...'.format(folder_path, zip_path))
            return None
        else:
            if verbose:
                print('Folder "{}" is outdated from zip "{}". Replacing...'.format(folder_path, zip_path))
            shutil.rmtree(folder_path)
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Now we need to make sure we're extracting the right nesting depth
        # If there is an __init__.py file in the root of the zip, extract that level.
        # Otherwise, check if there's a folder in the root of the zip and recurse to check for __init__.py
        # Repeat until we either have to choose between multiple folders or we find an __init__.py
        # Extract the complete contents of the folder with the __init__.py
        # If there is no __init__.py, raise an error
        for name in z.namelist():
            _zip_security_check(zip_path, name)
        init_files = [f for f in z.namelist() if f.endswith('__init__.py')]
        if len(init_files) == 0:
            raise EnvironmentError("Zip file {} does not appear to be a packaged mod. It is missing an __init__.py file.".format(zip_path))
        # Sort the init profiles by path depth
        init_files.sort(key=lambda x: x.count('/'))
        # Check if the first two items have the same depth, if so error out
        if len(init_files) > 1 and init_files[0].count('/') == init_files[1].count('/'):
            raise EnvironmentError("Zip file {} contains multiple __init__.py files at the shallowest depth. Cannot determine which to extract.".format(zip_path))
        # Extract the folder containing the __init__.py file
        init_path = init_files[0]
        mod_path = init_path.rsplit('/', 1)[0] if '/' in init_path else ''
        if verbose:
            print('Extracting "{}" into "{}"'.format(os.path.join(zip_path,mod_path), folder_path))
        _unpack_zip_path_to_path(z, mod_path, folder_path, debug=debug)
    return folder_path
