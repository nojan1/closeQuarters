from distutils.core import setup

#Only usefull with the included PKGBUILD since there is no proper package

setup(name='closequarters',
      version='1.0',
      description='2D top view zombie shooter game in cramped coridors',
      author='Niklas Hedlund',
      author_email='nojan1989@gmail.com',
      url='https://github.com/nojan1/closeQuarters',
      scripts=['closeQuarters'],
      packages=["closequarters"],
      package_dir={"closequarters": "."},
)
