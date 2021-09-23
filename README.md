# Caravan- Networking
Code for Project 2, network course from UVG

# Proyecto 2- redes

## Antecedentes 
La creación de protocolos que corran sobre TCP directamente requiere de un mejor control sobre
el tipo de comunicación y comprensión sobre la serialización de datos a un más bajo nivel. Uno de
los retos que se tienen hoy en día es poder mantener la sincronización de distintos equipos que
comparten un estado.

Los juegos tienden a ser demandantes con respecto a su planificación e implementación. Al ser
programas que ningún usuario está obligado a utilizar es un reto para los desarrolladores el hacerlo
lo más llamativo posible a manera de lograr que los jugadores se queden. Y uno de los principales
factores que hacen llamativos a un juego es la opción de multijugador.

Al mismo tiempo, los juegos de cartas tienen la flexibilidad que comparten un estado relativamente
sencillo entre los jugadores y que no requieren intercambio de información en tiempo real (al estar,
en su mayoría, basados en turnos)

## Objetivos
-Aplicar los conocimientos de TCP para mantener sincronizados los estados internos de
distintos clientes de una aplicación.
- Implementar un juego de cartas llamativo para el usuario.

## Desarrollo
El proyecto consiste en implementar un juego de cartas multijugador que utilice un protocolo
propietario (desarrollado por el equipo) para la sincronización de los distintos clientes de este. El
juego debe:

- Soportar 3+ jugadores.
- Permitir estrategia por parte de los participantes (no estar dado exclusivamente por el azar
como Guerra).
- Tener un estado público y un estado privado por jugador (no ser de información perfecta).
- Estar basado en turnos (no ser concurso de velocidad como Speed).
- Permitir chatear entre los jugadores.
- Permitir elegir un nombre al momento de unirse.
-Poder manejar varias “mesas” o “salas”. Es decir, soportar juegos concurrentes que puedan
ocurrir en el servidor.

## Instrucciones para correr el proyecto
-Descargar el .zip del github
-Desde terminal acceder a la carpeta que tenga los 3 archivos
-en terminal correr: python server.py
-en terminal acceder a: python caravan-main.py (3 terminales pues fue diseñado para ser utilizado solo en la misma red)
