# Maintainer: Niklas Hedlund <nojan1989@gmail.com>
pkgname=closequarters-git
pkgver=0.0
pkgrel=1
pkgdesc="2D top view zombie shooter game in cramped coridors"
url="http://github.com/nojan1/closeQuarters"
arch=('x86_64' 'i686')
license=('GPLv3')
depends=(python2 python2-pygame)
optdepends=()
makedepends=()
provides=(closequarters)
source=('git://github.com/nojan1/closeQuarters.git')
md5sums=('SKIP')

_gitname='closeQuarters'

pkgver() {
  cd $_gitname
  echo $(git rev-list --count HEAD).$(git rev-parse --short HEAD)
}

build() {
  cd "$srcdir/$_gitname"
    
  #Do some sed magic here to change paths around
  sed -i 's|./|/usr/share/closequarters/|g' config.py
}

package() {
  cd "$srcdir/$_gitname"
  
  #Copy rest of the program to site-packages
  mkdir -p $pkgdir/usr/lib/python2.7/site-packages/closequarters
  install *.py $pkgdir/usr/lib/python2.7/site-packages/closequarters/

  #Symlink main.py to /usr/bin
  mkdir -p $pkgdir/usr/bin
  ln -s main.py $pkgdir/usr/bin/closequarters

  #Copy media stuff to correct place
  mkdir -p $pkgdir/usr/share/closequarters
  cp -r {images,levels,sounds} $pkgdir/usr/share/closequarters/
}
