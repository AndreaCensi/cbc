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
        install_requires=['RepRep>=2,<3', 
                          'nose', # conf_tools
                          'PyGeometry>=1.1,<2',
                          'ConfTools>=1',
                          'compmake>=2,<3',
                          'PyContracts>=1.1,<2'],
        extras_require={},
)

