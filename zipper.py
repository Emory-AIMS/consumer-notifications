import os
import zipfile

if __name__ == "__main__":

    print("Creating package for AWS Lambda")

    zipf = zipfile.ZipFile('consumer-covapp.zip', 'w', zipfile.ZIP_DEFLATED)

    for file in os.listdir("."):
        if file.startswith('.') \
                or os.path.isdir(file) \
                or file.endswith('.pyc') \
                or (file.endswith('.ini') and str(file) != "config.ini") \
                or file.endswith('.txt') \
                or file.endswith('.md') \
                or file.endswith('-mac') \
                or file.startswith('zipper') \
                or file.startswith('test-') \
                or file.endswith('.zip'):
            continue
        print("adding", file)
        zipf.write(str(file))

    root_venv = "./venv/lib/python3.7/site-packages"
    print("adding virtualenv libraries")
    for root, dirs, files in os.walk(root_venv):
        # print root, dirs
        for file in files:
            # print "venv", os.path.join(root, file)
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path[len(root_venv):])
