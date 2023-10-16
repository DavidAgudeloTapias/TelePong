# TelePong

------------

### Tabla de contenidos
  * [Introducción](#introducci-n)
  * [Desarrollo](#desarrollo)
  * [Conclusiones](#conclusiones)
  * [Referencias](#referencias)

## Introducción
El presente proyecto tiene como propósito el desarrollo de infraestructura e implementación con el clásico juego “Pong”. 
Como objetivo de la implementación, se requiere que la aplicación logre intercambiar de manera coordinada mensajes, con una eficaz comunicación entre las aplicaciones involucradas y permitir la conexión de múltiples parejas de clientes, o en otras palabras, que sea concurrente.
Para su realización, al ser muy necesario tener en cuenta el intercambio de información, se utiliza un estilo arquitectónico de tipo cliente/servidor, en donde, el cliente hará una serie de peticiones y el servidor responderá a ellas. En este caso, el socket utilizado como mecanismo de comunicación con las aplicaciones es el Datagram y este está basado en el protocolo UDP, que de igual manera, es el utilizado para el desarrollo del proyecto.
Finalmente, con la unión de todos los factores anteriormente mencionados, se logra que la aplicación y proyecto TelePong, logre las metas iniciales de crear una aplicación que se comunique por la red de manera eficiente y no se limite a una sola conexión.

## Desarrollo
Para darle inicio al desarrollo del proyecto, comenzamos creando el juego “Pong”, con la ayuda de tutoriales encontrados en internet, los cuales ayudan a esclarecer la lógica y funcionamiento correcto del juego. El juego fue desarrollado en Python debido al mejor manejo y conocimiento que se tiene del mismo, esta elección también fue influenciada por diversas librerías que lograron que el desarrollo del juego fuera más sencillo y ameno. Para darle continuidad al proyecto, tuvimos como segundo objetivo la construcción del servidor el cuál fue implementado en C, para dicha creación, se tuvo muy en cuenta una referencia dada sobre la implementación tipo cliente/servidor con TCP en el lenguaje requerido; con esta referencia se pudo avanzar ya que se tenía una comprensión más sólida y una guía de cómo proseguir. 
Como continuación del proyecto, se debía lograr que la aplicación fuera concurrente, para esto, se hizo una investigación principal para tener un entendimiento previo, para esto, debíamos inicialmente tener en cuenta siempre la comunicación entre los clientes y el servidor de manera efectiva, luego se logra la conexión de dos clientes conectarse a un mismo punto, en este caso, a un mismo hilo, el cuál llevará a cabo todos los procesos necesarios para que el juego pueda darse con una comunicación sencilla, fluida y sin interrupciones o algún tipo de interferencia generado por otra partida con clientes distintos.
Para este punto del proyecto, ya se había logrado las metas iniciales, pero en procesos de pruebas para ver el funcionamiento y en general, el desempeño de todo el proceso, se pudo evidenciar retardos en los movimientos de elementos importantes del juego, como las paletas y la pelota, esto, generando que la experiencia fuera interrumpida y poco fluida. Para atacar esta problemática encontrada, se decidió poner la lógica de las partes afectadas en el juego, en el servidor, ya que en el envió y recepción de los mensajes tardaba más cuando se encontraba en el cliente. Con esta modificación, se logra que el juego sea mucho más fluido y rápido frente a los cambios presentados.

[![Diagrama de Procesos](https://github.com/DavidAgudeloTapias/TelePong/blob/main/Diagramas/Diagrama%20de%20Procesos%20TelePong.png "Diagrama de Procesos")](https://github.com/DavidAgudeloTapias/TelePong/blob/main/Diagramas/Diagrama%20de%20Procesos%20TelePong.png "Diagrama de Procesos")

[![Diagrama de Arquitectura](https://github.com/DavidAgudeloTapias/TelePong/blob/main/Diagramas/Diagrama%20de%20Arquitectura%20TelePong.png "Diagrama de Arquitectura")](https://github.com/DavidAgudeloTapias/TelePong/blob/main/Diagramas/Diagrama%20de%20Arquitectura%20TelePong.png "Diagrama de Arquitectura")
## Conclusiones
Al momento de iniciar el proyecto, se planteó inicialmente la cuestión sobre qué tipo de protocolo y socket utilizar para que nuestra aplicación funcionara de una manera óptima, como grupo se planteó como meta tener una experiencia agradable con el juego, se optó por tener un juego con respuesta rápida, casi inmediata, por esa razón se utilizó el protocolo UDP y socket Datagram, los cuales se acomodaban mucho más a nuestra meta final, ya que son más eficientes y rápidos. Al finalizar nuestro proceso, pudimos evidenciar y concluir que la decisión tomada fue satisfactoria y acertada para alcanzar nuestro cometido, pues, se logra que el juego sea fácil y veloz; si bien, con nuestra decisión, se deja expuesto a que sea más propenso a pérdidas de información, el juego ha respondido correctamente y no se han evidenciado pérdidas significativas que logren afectar la experiencia del cliente o la fluidez del juego. 

## Referencias
- https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
- https://www.cloudflare.com/es-es/learning/network-layer/what-is-a-protocol/
- https://www.avast.com/es-es/c-tcp-vs-udp-difference#:~:text=La%20principal%20diferencia%20entre%20el,fiable%20pero%20funciona%20m%C3%A1s%20r%C3%A1pido.
- https://autmix.com/blog/que-es-protocolo-red
- https://ed.team/blog/como-funcionan-los-hilos-en-programacion
- https://www.w3schools.com/c/c_getstarted.php
- https://www.youtube.com/watch?si=lMF6fgbAsW3L_s1M&v=vVGTZlnnX3U&feature=youtu.be
