from setuptools import setup, find_packages

setup(
    name='sm-updater',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'py7zr',
        'pixeldrain',
        'requests',
        'supabase',
    ],
    entry_points={
        'console_scripts': [
            'start-sm-updater=main:main',
        ],
    },
)
