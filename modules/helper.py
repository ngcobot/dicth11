import os

# Method to scan folder for files and subfolders
def scan_files(dir, ext):
    """
    Scan folder for a given file extenstion(eg .bin , .mp4)
    """
    subfolders, files = [], []

    for sub in os.scandir(dir):
        # Add found directory to list
        if sub.is_dir():
            subfolders.append(sub.path)
        if sub.is_file():
            if os.path.splitext(sub.name)[1].lower() in ext:
                files.append(sub.path)

    for dir in list(subfolders):
        sf, f = scan_files(dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return (subfolders, files)
