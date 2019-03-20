#! /bin/bash
# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


cwd=$(pwd)

if [ $# -ne 1 ]; then
    echo "Usage: $0 <work-dir>"
fi

workdir=$1

echo "Creating work dir $workdir"
mkdir $workdir
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Copying dss-server-config.ini file"
cp $cwd/dss-server-config.ini $workdir/
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Copying plugin.ini file"
cp $cwd/plugin.ini $workdir/
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Copying plugin"
cp ../../../../plugins/dssfile.py $workdir/

echo "Updating dss-server-config.ini"
pluginfile=$workdir/dssfile.py
escapepluginfile=$(echo $pluginfile | sed 's/\//\\\//g')
sed -i "s/PLUGIN_FILE/$escapepluginfile/g" $workdir/dss-server-config.ini
if [ $? -ne 0 ]; then
    exit 1
fi

echo "Updating plugin.ini"
pluginconf=$workdir/plugin.ini
escapepluginconf=$(echo $pluginconf | sed 's/\//\\\//g')
sed -i "s/PLUGIN_CONF/$escapepluginconf/g" $workdir/dss-server-config.ini

files=$workdir/files
escapefiles=$(echo $files | sed 's/\//\\\//g')
mkdir $files
if [ $? -ne 0 ]; then
    exit 1
fi

sed -i "s/DIR/$escapefiles/g" $workdir/plugin.ini



export PYTHONPATH=$cwd/../../../

exec python $cwd/../server/dss_main.py --config $workdir/dss-server-config.ini
