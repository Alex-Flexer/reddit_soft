import os


def get_file_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension


print(get_file_extension(r"D:\проекты Python new VS\subs\NFT\used\0.png"))
