

- Para crear el escenario empaquetado:

    bin/pack-scenario-with-rootfs # con rootfs

    bin/pack-scenario             # sin rootfs

A la hora de levantar el escenario se puede configar el start.sh para que haga lo que quieras, incluido el scp de la imagen para no tener que hacerlo todo manualmente ni tener que crearla con el comando. Cuando se levantan las funciones de red con osm por primera vez hay que dejarlo unos 15 o 20 min levantando aunque ponga error en osm, hasta que en OpenStack te deje acceder a las consolas de las imagenes. En ese momento tiras el servicio de red en osm y ya lo levantas otra vez. Ahí deberia tardar entre 1 y 4 min en pasar a estado de configurar y activo. Despues le das una ip flotante a las máquinas y haces la configuración inicial en cada una de ellas.
