from setuptools import setup, find_packages


setup(name='CBC',
        author="Andrea Censi",
        author_email="andrea@cds.caltech.edu",
        version="1.0",
        package_dir={'':'src'},
        packages=['cbc'],
        entry_points={
         'console_scripts': [
           'cbc_main  = cbc.calib_main:main',
           'camera_plots = cbc.demos.camera_plots:main'
           ]
        },
        install_requires=['reprep', 'numpy', 'PyContracts', 'PyGeometry', 'nose'],
        extras_require={},
)

