# Verilog

En este repo estoy aprendiendo Verilog e intentando armar un CPU single-cycle muy básico basado en la [ISA de OrgaSmall](docs/orgaSmall_datasheet.pdf).

## Toolchain

- [Icarus Verilog](https://github.com/steveicarus/iverilog): simulador
- [cocotb](https://github.com/cocotb/cocotb): testbench en python
- [Yosys](https://github.com/YosysHQ/yosys): síntesis
- [GTKWave](https://gtkwave.sourceforge.net/): visualizador de wavefiles

## Entorno de desarrollo

- `./scripts/setup`: Buildea un container de Docker con todas las herramientas instaladas.
- `./scripts/shell`: Abre un shell adentro del container con `pwd` montado en `/workspace`.

## Estructura del proyecto

- `./src/hdl/<module>.sv`: Módulos en SystemVerilog.
- `./src/tests/test_<module>.py`: Testbench para `<module>`.
- `./src/build/<module>/`: Output de la simulación. El archivo interesante es `dump.vcd` que contiene el wavefile.

## Testbenchs

Para testear un módulo en particular:

```sh
make <module>
```

Para testear todos los módulos:

```sh
make
```

## Ejecutar programas

El testbench `programs` ensambla y ejecuta programas en el CPU simulado (`make programs`). En la carpeta `src/tests/programs` se encuentran algunos programas de ejemplo, y en `src/tests/test_programs.py` se puede ver cómo ensamblar los programas, ejecutarlos, y luego verificar el estado correcto del CPU.

Se podría extender esto para poder ejecutar programas arbitrarios "fuera" del entorno de testing. Técnicamente hablando igual se ejecuta dentro del entorno de testing, ya que usamos cocotb para orchestrar la simulación del CPU con iverilog, pero podríamos no hacer ningún assert, ocultar el output de cocotb, y al finalizar la ejecución imprimir un dump de los registros y memoria.

## Notas

- Si quiero hacer un cpu single-cycle necesito si o si 2 memorias separadas (programa y datos), o una memoria dual port (2 lecturas simultáneas)?
- Se debería cargar la sección `.text` en la memoria de instrucciones y la sección `.data` en la memoria de datos? Sino las instrucciones nunca pueden acceder a datos definidos con `DW` en el programa.
- Mantener el clock entre distintos test cases.
- Compartir configs como `WORD_SIZE` y los opcodes entre verilog y python (DRY).
- Tipos usados para los parámetros limitan las opciones de configuración?
- Mejorar el display de errores cuando se hace `make` de todos los módulos (el output es muy largo, quizás debería frenar el make si falla algún módulo).
- Para respetar la ISA de OrgaSmall el PC debería incrementar de a 2.
- El ensamblador interpreta al revés los operandos de `STR`. Funciona así: `STR RX, M` con el efecto `Mem[M] <- RX`.
- El ensamblador no interpreta los `[]` (no hay que ponerlos).
