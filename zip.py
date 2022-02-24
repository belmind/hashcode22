import os
import zipfile


# Not relevant to judges
IGNORE = set([
    '.git',
    '__pycache__',
    'in',
    'out',
    '.gitignore',
    'LICENSE',
    'Makefile',
    'README.md',
    'hashcode22.zip',
    'zip_dir.py',
    'venv'
])


def zip_directory(zf):
    for root, dirs, files in os.walk('./'):
        dirs[:] = [d for d in dirs if d not in IGNORE]
        for file in files:
            if file in IGNORE:
                continue

            zf.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file),
                os.path.join('./', '..'))
            )


if __name__ == '__main__':
    zf = zipfile.ZipFile('hashcode22.zip', 'w', zipfile.ZIP_DEFLATED)
    zip_directory(zf)
    zf.close()
