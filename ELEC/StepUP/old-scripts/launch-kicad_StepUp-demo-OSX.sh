#!/bin/bash

# Absolute path to this script. /home/user/bin/foo.sh
##SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
##SCRIPTPATH=`dirname $SCRIPT`
##echo $SCRIPTPATH
##cd $SCRIPTPATH

#!/bin/bash

#realpath() {
#    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
#}

#realpath "$0"

pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

cd $SCRIPTPATH

echo  $SCRIPTPATH

# /Applications/FreeCAD.app/Contents/bin/FreeCAD  "cq_make_capacitors_export_fc.py" "1206_h078"
#/Applications/FreeCAD.app/Contents/bin/FreeCAD  /Users/mau/Downloads/kicad-3d-models-in-freecad-master/cadquery/FCAD_script_generator/cq_make_capacitors_export_fc.py 1206_h078 
/Applications/FreeCAD.app/Contents/bin/FreeCAD demo.emn ksu-config.cfg kicad_StepUp.FCMacro

# freecad demo.emn kicad_StepUp.FCMacro
## freecad <IDF file> <configuration file> kicad_StepUp.FCMacro
##freecad demo.emn ksu-config.cfg kicad_StepUp.FCMacro
