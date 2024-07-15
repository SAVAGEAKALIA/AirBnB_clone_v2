##!/usr/bin/env bash
sed -i '/server_name _;/a \\t\t location \/hbnb_static {\n\t\t\talias \/data\/web_static\/current\/;\n\t\t}' test.cfg