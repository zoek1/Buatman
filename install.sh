#!/bin/sh

version=`python -c 'import sys; print(sys.version[:1])'`


if [ $version -lt 3 ]; then
    echo "Se requiere la version de python 3"
    exit
fi


libs="data.py red.py"

bin=/usr/bin
application=/usr/share
icon=${application}/icons
path=${application}/buapman
desktop=${application}/applications

function root {
    if [ `id -u` != 0 ]; then
	echo "Se necesitan permisos de superusuario"
	exit
    fi
}

function check {
    if [ -e $1 ]; then
	return 0
    fi

    return 1
}

function action {
	$2 $1
	echo "${3}: $1"
}

function create {
    if [ ! -e $1 ]; then
	action $1 $2 "Creando"
    fi
}

function delete {
    if [ -e $1 ]; then
	action $1 $2 "Eliminando"
    fi    
}

# create "hola.hs" touch
# delete "hola.hs" rm

function install() {
    create $path mkdir
    cat login.py | sed 's/QPixmap(/QPixmap("\/usr\/share\/buapman\/"+/'  > /tmp/login.py
    cat buapman.py | sed 's/QIcon(/QIcon("\/usr\/share\/buapman\/"+/'  > /tmp/buapman.py
    cp -v ${libs} /tmp/buapman.py /tmp/login.py ${path}
    cp -vr Img ${path}/
    cp -v Img/logo.png ${icon}/buapman.png
    chmod 755 ${path}/buapman.py
    if [[ -e ${bin}/buapman ]]; then
	rm ${bin}/buapman
    fi
    ln -sv ${path}/buapman.py ${bin}/buapman
    cp -v buapman.desktop ${desktop}
}

function noinstall() {
    if check ${path}; then 
	rm -r ${path}
	echo "Eliminando: ${path} "
    fi
    # if check ${bin}/buapman; then rm ${bin}/buapman; fi
    delete  ${bin}/buapman "rm -r"
    delete ${icon}/buapman.png rm 
    delete ${desktop}/buapman.desktop rm 
    delete ${icon}/buapman.png
}

if [[ ${#} -eq 0  || $1 == "install" ]]; then
    root
    install  
elif [ ${1} = "clean" ]; then
    root
    noinstall
fi

# echo "saliendo"
