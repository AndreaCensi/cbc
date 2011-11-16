from setuptools import setup, find_packages


setup(name='CBC',
        author="Andrea Censi",
        author_email="andrea@cds.caltech.edu",
        version="1.0",
        package_dir={'':'src'},
        packages=['cbc'],
        entry_points={
         'console_scripts': [
           'cbc_main  = cbc.manager.calib_main:main',
           'camera_plots = cbc.demos.camera_plots:main'
           ]
        },
        install_requires=['reprep>=1.1,<2', 'numpy',
                          'nose', # conf_tools
                          'PyGeometry>=1.1,<2',
                          'conf_tools<2',
                          'compmake>=1.1,<2',
                          'PyContracts>=1.1,<2'],
        extras_require={},
)

