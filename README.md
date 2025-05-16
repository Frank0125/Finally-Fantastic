# Finally Fantastic - Python RPG

### To run this project you should do the following commands

```shell
venv\bin\activate
```
```shell
pip install -r requirements.txt
```

## This project uses the following Design Patterns:

- Creational Pattern: 
- Structural Pattern:
- Comportamiento Pattern: 
- Extra Pattern (Type): 

## UML created in mermaid:


```mermaid
classDiagram
class Casilla {
  #int numero
  #int premio_castigo
  #string tipo
  +CCasilla()
  +CCasilla(int,string)
  +int getNumeroCasilla()
  +string getTipo()
  +int getSiguienteCasilla()
  +void print()
}

class Normal {
  +CasillaNormal()
  +CasillaNormal(int)
}
Casilla <|-- Normal

class Escalera {
  +CasillaEscalera()
  +CasillaEscalera(int)
}
Casilla <|-- Escalera

class Serpiente {
  +CasillaSerpiente()
  +CasillaSerpiente(int)
}
Casilla <|-- Serpiente

class Tablero {
  -CCasilla c
  +Tablero()
  +Tablero(string)
  +void setCasilla(CCasilla,int)
  +CCasilla getCasilla(int)
  +void print()
}

class Jugador {
  #int numero
  #int casilla_actual
  +Jugador()
  +Jugador(int)
  +int getCasilla_actual()
  +void setCasilla_actual(int)
  +void print()
}

class Dado {
  -bool switchrandom
  +int cara
  +CDado()
  +CDado(bool)
  +int getValorDado()
}

class Game {
  -Tablero t
  -Jugador j
  -CDado d
  -bool swio 
  +Game()
  +Game(string,bool,bool)
  +void start()
  +void outMsg(string)
}

Game --> Tablero : tiene
Game --> Jugador : tiene 2
Game --> Dado : tiene 1
Tablero --> Casilla : tiene 30

```