#1/usr/bin/env python

from distutils.core import setup

with open('README.rst') as f:
    long_description=f.read()

setup(name='netdisk',
        version='1.0',
        author='Yugang LIU',
        author_email='liuyug@gmail.com',
        url='https://github.com/liuyug/netdisk',
        license='GPLv3',
        description='Command Line Tool for Network Disk',
        long_description=long_description,
        platforms=['noarch'],
        packages=[
            'netdisk',
            'netdisk.dropbox',
            'netdisk.kuaipan',
            'netdisk.kuaipan.oauth',
            'netdisk.kuaipan.poster',
            ],
        package_dir={'netdisk': 'netdisk'},
        package_data={'netdisk.dropbox': ['trusted-certs.crt']},
        #data_files=[('netdisk',['README.rst')],
        scripts=['netdisk_cli'],
        )
