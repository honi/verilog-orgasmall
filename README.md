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

## Módulos

- memory
- registers
- decoder
- alu
- cpu

## Testbenchs

Para testear un módulo en particular:

```sh
make test_<module>
```

Para testear todos los módulos:

```sh
make
```

Luego de correr los tests, el wavefile se genera en `src/<module>/tests/dump.vcd`.

## Notas

- Si quiero hacer un cpu single-cycle necesito si o si 2 memorias separadas (programa y datos), o una memoria dual port (2 lecturas simultáneas)?
- Mantener el clock entre distintos test cases.
- Compartir parámetros defaults como `WORD_SIZE`.
- Tipos usados para los parámetros limitan las opciones de configuración?
- Revisar config de cocotb, parece que es mucho más rápido correr directo desde python sin el makefile que te dan de ejemplo.
