from setuptools import setup, find_packages


setup(name='CBC',
        author="Andrea Censi",
        author_email="andrea@cds.caltech.edu",
        version="0.1",
        package_dir={'':'src'},
        packages=['cbc'],
        entry_points={
         'console_scripts': [
           'cbc_main  = cbc.calib_main:main',
           ]
        },
        install_requires=['reprep', 'numpy', 'PyContracts', 'snp_geometry',
                          'nose'],
        extras_require={},
#    include_package_data=True,
#    package_data={
#        'be1008': ['models/*.pg', '*.pg']
#    }
)

