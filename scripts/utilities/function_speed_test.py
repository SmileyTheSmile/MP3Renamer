from scripts.utilities.file_operations import load_supported_files

import timeit
print(timeit.timeit(stmt='load_supported_files("C:/Users/ASUS/Music/Music", [".mp3"])',
                    setup='from scripts.utilities.file_operations import load_supported_files'))