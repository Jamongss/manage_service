#!/bin/bash

docker ps --format "{{.Names}}" | tr '\n' ' ' | sed 's/ $/\n/'
