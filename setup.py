#!/usr/bin/env python

import os.path
import sys
from distutils.core import setup
from distutils.command import install_scripts

from netdisk import __version__


class post_install_scripts(install_scripts.install_scripts):
    """ remove script ext """
    def run(self):
        install_scripts.install_scripts.run(self)
        if sys.platform == 'win32':
            for script in self.get_outputs():
                if script.endswith(".py"):
                    new_name = '%s_gui.py' % script[:-3]
                    if os.path.exists(new_name):
                        os.remove(new_name)
                    print('renaming %s -> %s' % (script, new_name))
                    os.rename(script, new_name)
        else:
            for script in self.get_outputs():
                if script.endswith(".py"):
                    new_name = script[:-3]
                    if os.path.exists(new_name):
                        os.remove(new_name)
                    print('renaming %s -> %s' % (script, new_name))
                    os.rename(script, new_name)
        return


with open('README.rst') as f:
    long_description = f.read()

setup(name='netdisk',
      version=__version__,
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
      scripts=['netdisk.py'],
      cmdclass={
          'install_scripts': post_install_scripts,
      },
      )
