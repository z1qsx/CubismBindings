# Cubism SDK Bindings

Welcome to the project for generating bindings to the Cubism SDK.

If you're interested in generating available bindings or in using this project for generating your own bindings, read on.

If you came here looking for official Live2D homepage, instead, you'll find it [here](http://www.live2d.com/products/cubism3).


## Overview

The project basically consitsts of 3 parts:
1. A representation of the Cubism SDK API in *YAML*
1. Templates the *YAML* data is run through
1. Generators that patch the *YAML* data and control what templates are to be expanded


## Prerequisites

1. [*Python*](https://www.python.org) (as that's the language the generators are written in)
1. [*PyYAML*](http://pyyaml.org/) (used for parsing the API descriptors)
1. [*Pystache*](https://github.com/defunkt/pystache) (used in the templates) 


## Available Generators

### JavaScript

This generator doesn't only provide bindings, but also allows building a fully working JavaScript Core library.
**Be aware that the [Core license](http://live2d.com/eula/live2d-proprietary-software-license-agreement_en.html) applies to the built library as well.**
The generator involves a few steps:
1. It generates *TypeScript* bindings for a *Cubism Core* to be compiled with *Emscripten*.
1. It generates a script for building the *Cubism Core* with *Emscripten* and for merging all sources into one library.


#### Prerequisites

1. [*Emscripten*](http://kripken.github.io/emscripten-site/)
1. [*TypeScript*](https://www.typescriptlang.org/)
1. [*Cubism SDK for Native*](https://live2d.github.io/#native)
1. [*UglifyJS*](https://www.npmjs.com/package/uglify-js) *

*In macOS or linux environments, it is necessary to obtain the file directly from (https://nodejs.org/en/) or install uglify-js by executing `npm install uglify-js -g`.


#### Usage

1. Run `python ./genjs.py`. By default, this will output artefacts to `./out/js`.
1. Run `python ./out/js/make.py --coredir <path-to-Cubism-SDK-Core-directory>`. This will output the final library and *TypeScript* declarations to `./out/js/out`.


### C#

### Usage

1. Run `python ./gencs.py`. By default, this will output artefacts to `./out/cs`.


## Contributing

There are many ways to contribute to the project: logging bugs, submitting pull requests on this GitHub, and reporting issues and making suggestions at Live2D Community.


## Discussion Etiquette

Please limit the discussion to English and keep it professional and things on topic.


## TODO

- Investigate framework generators.

## License

The license applying to the source code in this project allows you modify all sources without the need to submit any changes you made.
Refer to [this license](http://live2d.com/eula/live2d-open-software-license-agreement_en.html) for the gritty details.