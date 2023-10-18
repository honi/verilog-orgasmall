# Verilog

En este repo estoy aprendiendo Verilog e intentando armar un CPU muy básico.

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
- `./src/build/<module>/`: Output de la simulación. El archivo interesante es `<module>.vcd` que contiene el wavefile.

## Testbenchs

Para testear un módulo en particular:

```sh
make <module>
```

Para testear todos los módulos:

```sh
make
```

## Notas

- Si quiero hacer un cpu single-cycle necesito si o si 2 memorias separadas (programa y datos), o una memoria dual port (2 lecturas simultáneas)?
- Mantener el clock entre distintos test cases.
- Compartir configs como `WORD_SIZE` y los opcodes entre verilog y python (DRY).
- Tipos usados para los parámetros limitan las opciones de configuración?
- Mejorar el display de errores cuando se hace `make` de todos los módulos (el output es muy largo, quizás debería frenar el make si falla algún módulo).
