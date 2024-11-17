from os import system, rmdir
from os.path import join
import shutil

def obfuscate_client_app(path_to_obfuscated_file, path_to_file):
    system(f"pyarmor gen -O {path_to_obfuscated_file} -r {path_to_file}")


def zip_directory(directory: str, output_file: str):
    shutil.make_archive(output_file, 'zip', directory)


def save_requirements(path_to_requirements_file):
    venv_pip_path = f".\.venv\Scripts\pip.exe"
    system(f"{venv_pip_path} freeze > {path_to_requirements_file}")

def remove_dist_folder(path_to_dist_folder):
    shutil.rmtree(path_to_dist_folder)


def main():
    path_to_client_app = '../client_app'
    path_to_obfuscated_client_app = "./private_resources/dist"
    path_to_zipped_client_app = './private_resources/source'

    obfuscate_client_app(path_to_obfuscated_client_app, path_to_client_app)
    save_requirements(join(path_to_obfuscated_client_app, "client_app", "requirements.txt"))

    zip_directory(path_to_obfuscated_client_app, path_to_zipped_client_app)

    remove_dist_folder(path_to_obfuscated_client_app)

if __name__ == '__main__':
    path_to_obfuscated_client_app = ".\private_resources\dist"
    join(path_to_obfuscated_client_app, "client_app", "requirements.txt")
    save_requirements(".\server\private_resources\req.txt")
    main()
