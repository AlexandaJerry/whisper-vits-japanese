import os

# Create csv directory
def create_directories():
    slice_path = './ready_for_slice'

    if not os.path.exists(slice_path):
        try:
            os.mkdir(slice_path)
        except OSError:
            print('Creation of directory %s failed' %slice_path)

    sliced_audio = './sliced_audio'

    if not os.path.exists(sliced_audio):
        try:
            os.mkdir(sliced_audio)
        except OSError:
            print('Creation of directory %s failed' %sliced_audio)

    merged_csv_files = './merged_csv'

    if not os.path.exists(merged_csv_files):
        try:
            os.mkdir(merged_csv_files)
        except OSError:
            print('Creation of directory %s failed' %merged_csv_files)

    final_csv_files = './final_csv'

    if not os.path.exists(final_csv_files):
        try:
            os.mkdir(final_csv_files)
        except OSError:
            print('Creation of directory %s failed' %final_csv_files)
