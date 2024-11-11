from os import system
import shutil

def obfuscate_client_app(path_to_obfuscated_file, path_to_file):
    system(f"pyarmor gen -O {path_to_obfuscated_file} -r {path_to_file}")


def zip_directory(directory: str, output_file: str):
    shutil.make_archive(output_file, 'zip', directory)


def main():
    path_to_client_app = '../client_app'
    path_to_obfuscated_client_app = "./private_resources/dist"
    path_to_zipped_client_app = './private_resources/source'

    obfuscate_client_app(path_to_obfuscated_client_app, path_to_client_app)

    zip_directory(path_to_obfuscated_client_app, path_to_zipped_client_app)

if __name__ == '__main__':
    main()
