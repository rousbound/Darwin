
# Darwin

## Seções

- [Aquecendo os tambores](#getting-started)
- [Rodando um dna previamente treinado](#running-tests)
- [Treinando sua própria espécie](#development)


## Aquecendo os tambores - Instalando os pré-requisitos

Para rodar o projeto é necessário instalar o pygame

``` bash
$ pip install pygame
```

## Rodando um dna previamente treinado

Para rodar um exemplo já treinado é necessário rodar o seguinte comando, passando um arquivo ```.npy``` como argumento:

``` bash
$ python3 runSpecimen 'BestDNA/Gen test - 2020-01-23 - 17:47:12--61-201.0.npy'
```

## Treinando sua própria espécia

A maneira canônica de usar o framework é a seguinte:

``` python
  import sys
  sys.path.append("../Nature")
  from Darwin import Evolution
  from yourGame import *
  evolve = Evolution( 

    offspring_num = 100,
    generations = 500,
    sizes=[20,21,27,4],
    num_parents = 12,
    mutation_rate = 7,
    crossing_algorithm = "uniform",
    saving_txt = True, saving_csv = True, saving_dna = True,
    saveDnaThreshold = None,
    loadDnaPath = "",
    game = yourGameClass,
    gameArgs = yourGameArgsDict) 

  evolve.main()
```

Para usar o framework é necessário importar e passar como
parâmetro para o objeto Evolution, o objeto do seu jogo.
Sua classe deve ter uma função main que retorne um score e um fitness. De
resto, os hiperparâmetros devem ser configurados a mão. Caso hajam
parâmetros para serem passados para sua gameClass, eles
devem ser passados e desempacotados em forma de dicionário. Ex: ```gameArgs = {'drawingMode': False}```
