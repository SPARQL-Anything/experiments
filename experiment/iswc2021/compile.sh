#
# Copyright (c) 2022 SPARQL Anything Contributors @ http://github.com/sparql-anything
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

mvn -f ../../pom.xml clean install -DskipTests


THIS_FOLDER=$(pwd)
if [[ ! -e "bin" ]]; then
	mkdir bin
fi

cp ../../sparql.anything.cli/target/sparql-anything-$1.jar bin/


curl -OL https://github.com/spice-h2020/sparql.anything/releases/download/v$2/sparql-anything-$2.jar

mv sparql-anything-$2.jar bin/
