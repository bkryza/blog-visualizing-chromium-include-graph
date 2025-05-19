# Visualizing Chromium include graph

This repository contains supplemental material for my blog post:

* [Visualizing Chromium include graph](https://blog.bkryza.com/posts/visualizing-chromium-include-graph/)

## Docker image

The Docker image `bkryza/clang-include-graph-chromium:v1` can be used to build Chromium and generate `compile_commands.json` necessary to run `clang-include-graph`. It contains a bash script which can be used to execute the commands without attaching to the Docker container:

```bash
# First create a Docker volume to keep the generated files
$ docker volume create clang-include-graph-chromium-build

# Now show the image commands
$ docker run --rm --mount source=clang-include-graph-chromium-build,target=/build -it bkryza/clang-include-graph-chromium:v1 usage
Usage: main.sh <step>

Steps:
  fetch     Fetch Chromium sources
  build     Build Chromium
  graphml   Generate the include graph in GraphML format
  graphviz  Generate the include graph in Graphviz format
  json      Generate the include graph in JSON format
  stats     Calculate include graph statistics
  all       Run all steps in order (default)

Example:
  main.sh fetch
  main.sh build
  main.sh graphml
  main.sh graphviz
  main.sh json
  main.sh stats
  main.sh all
```


# LICENSE

```
Copyright 2025 Bartek Kryza <bkryza@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
