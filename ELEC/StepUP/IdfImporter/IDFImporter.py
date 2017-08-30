#***************************************************************************
#*   (c) Milos Koutny (milos.koutny@gmail.com) 2012                        *
#*   (c) Maurice (https://launchpad.net/~easyw kicad StepUp) 2015                       *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Library General Public License (LGPL)   *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Milos Koutny 2010                                                     *
#***************************************************************************/

import FreeCAD, Part, os, FreeCADGui, __builtin__
from FreeCAD import Base
from math import *
import ImportGui
if FreeCAD.GuiUp:
    from PySide import QtCore, QtGui
import time
current_milli_time = lambda: int(round(time.time() * 1000))

##########################################################
# Script base version dated 19-Jan-2012                  #
##########################################################
#Configuration parameters below - use standard slashes / #
##########################################################

## updates December 2016 Maurice:
IDF_ImporterVersion="3.9.3"
#  ignoring step search associations (too old models)
#  displaying Flat Mode models
#  checking version 3 for both Geometry and Part Number
#  supporting Z position
#  skipping PROP in emp file
#  adding color to shapes opt IDF_colorize
#  adding emp library/single model load support
#  aligning IDF shape to both Geom and PartNBR for exactly match
#  to do: .ROUTE_OUTLINE ECAD, .PLACE_OUTLINE MCAD, .ROUTE_KEPOUT ECAD, .PLACE_KEEPOUT ECAD


## path to table file (simple comma separated values)

#model_tab_filename = FreeCAD.getHomePath()+ "Mod/Idf/Idflibs/footprints_models.csv"
##model_tab_filename = FreeCAD.getHomePath()+ "Mod/Idf/lib/footprints_models.csv"  #maui

## path to directory containing step models

#step_path=FreeCAD.getHomePath()+ "Mod/Idf/Idflibs/" #maui
##step_path=FreeCAD.getHomePath()+ "Mod/Idf/lib/"

ignore_hole_size=0.0 # maui 0.5 # size in MM to prevent huge number of drilled holes
#EmpDisplayMode=2 # 0='Flat Lines', 1='Shaded', 2='Wireframe', 3='Points'; recommended 2 or 0
EmpDisplayMode=0 # 0='Flat Lines', 1='Shaded', 2='Wireframe', 3='Points'; recommended 2 or 0 #maui

IDF_sort=0 # 0-sort per refdes [1 - part number (not preffered)/refdes] 2-sort per footprint/refdes

IDF_diag=0 # 0/1=disabled/enabled output (footprint.lst/missing_models.lst) 
IDF_diag_path="/tmp" # path for output of footprint.lst and missing_models.lst

IDF_colorize=1 # 0/1 assign color to shapes
start_time=0 #var start_time

########################################################################################
#              End config section do not touch code below                              #
########################################################################################

pythonopen = __builtin__.open # to distinguish python built-in open function from the one declared here

def PLine(prm1,prm2):
    if hasattr(Part,"LineSegment"):
        return Part.LineSegment(prm1, prm2)
    else:
        return Part.Line(prm1, prm2)
        
def open(filename):
    """called when freecad opens an Emn file"""
    docname = os.path.splitext(os.path.basename(filename))[0]
    doc = FreeCAD.newDocument(docname)
    message='Started with opening of "'+filename+'" file\n'
    message=message+'IDF_ImporterVersion='+IDF_ImporterVersion+'\n'
    FreeCAD.Console.PrintMessage(message)
    if (filename.endswith('.emp')):
        FreeCAD.Console.PrintMessage('idf model file')
        IDF_Type="IDF Library"
        start_time=current_milli_time()
        process_emp_model(doc,filename)
    else:    
        IDF_Type="IDF assemblies "
        start_time=current_milli_time()
        process_emn(doc,filename)
        end_milli_time = current_milli_time()
        running_time=(end_milli_time-start_time)/1000
    msg="running time: "+str(running_time)+"sec\n"
    FreeCAD.Console.PrintMessage(msg)
    msg="""<b>IDF Importer</b> version {0}<br><br>
           <b>{1}</b> file imported:<br><i>{2}</i><br><br>
           for <b>STEP</b> version visit <a href="http://sourceforge.net/projects/kicadstepup/">kicad StepUp</a>
           """.format(IDF_ImporterVersion,IDF_Type,filename)

    #QtGui.QMessageBox.information(None,"Info ...",msg)    
    FreeCAD.Console.PrintMessage(message)
    infoDialog(msg)

#####################################
# Function infoDialog 
#####################################
def infoDialog(msg):
    #QtGui.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
    QtGui.qApp.restoreOverrideCursor()
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,u"Info Message",msg )
    diag.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()
    QtGui.qApp.restoreOverrideCursor()
    
def insert(filename,docname):
    """called when freecad imports an Emn file"""
    FreeCAD.setActiveDocument(docname)
    doc=FreeCAD.getDocument(docname)
    FreeCAD.Console.PrintMessage('Started import of "'+filename+'" file')
    process_emn(doc,filename)
    
def process_emp_model(doc,filename):
    """process_emp(document, filename)-> adds idf/emp geometry from emp file"""
    global emn_version
    emn_version=3.0
    placement=[]
    placement=[['Ref', '"Geometry"', '"PartNbr_Library_emp"', 0.0, 0.0, 0.0, 0.0, 'TOP', 'ECAD']]
    board_thickness=1.6    
    process_emp(doc,filename,placement,board_thickness)
    FreeCAD.ActiveDocument.getObject("EMP_Models").removeObjectsFromDocument()
    FreeCAD.ActiveDocument.removeObject("EMP_Models")
    FreeCADGui.ActiveDocument.ActiveObject.BoundingBox = True
    FreeCADGui.ActiveDocument.ActiveObject.Visibility=True
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewAxometric()      
   
def process_emn(doc,filename):
   """process_emn(document, filename)-> adds emn geometry from emn file"""
   global emn_version
   emnfile=pythonopen(filename, "r")
   emn_unit=1.0 #presume milimeter like emn unit
   emn_version=2 #presume emn_version 2
   board_thickness=0 #presume 0 board height
   board_outline=[] #no outline
   drills=[] #no drills
   placement=[] #no placement
   place_item=[] #empty place item
   emnlines=emnfile.readlines()
   emnfile.close()   
   passed_sections=[]
   current_section=""
   section_counter=0
   for emnline in emnlines:
       emnrecords=split_records(emnline)
       if len( emnrecords )==0 : continue
       if len( emnrecords[0] )>4 and emnrecords[0][0:4]==".END":
          passed_sections.append(current_section)
          current_section=""
       elif emnrecords[0][0]==".":
          current_section=emnrecords[0]
          section_counter=0
       section_counter+=1
       if current_section==".HEADER"  and section_counter==2:
          emn_version=int(float(emnrecords[1]))
          FreeCAD.Console.PrintMessage("Emn version: "+emnrecords[1]+"\n")
       if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="THOU":
          emn_unit=0.0254
          FreeCAD.Console.PrintMessage("UNIT THOU\n" )
       if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="TNM":
          emn_unit=0.000010
          FreeCAD.Console.PrintMessage("TNM\n" )
       if current_section==".BOARD_OUTLINE"  and section_counter==2:
          board_thickness=emn_unit*float(emnrecords[0])
          FreeCAD.Console.PrintMessage("Found board thickness "+emnrecords[0]+"\n")
       if current_section==".BOARD_OUTLINE"  and section_counter>2:
          board_outline.append([int(emnrecords[0]),float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit,float(emnrecords[3])])
       if current_section==".DRILLED_HOLES"  and section_counter>1 and float(emnrecords[0])*emn_unit>ignore_hole_size:
          drills.append([float(emnrecords[0])*emn_unit,float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit])
       if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==0:
          place_item=[]
          place_item.append(emnrecords[2]) #Reference designator
          place_item.append(emnrecords[1]) #Component part number
          place_item.append(emnrecords[0]) #Package name
       if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==1:
          place_item.append(float(emnrecords[0])*emn_unit) #X
          place_item.append(float(emnrecords[1])*emn_unit) #Y
          if emn_version==3:
            place_item.append(float(emnrecords[2])*emn_unit) #Z  maui
            #FreeCAD.Console.PrintMessage("\nZ="+(str(float(emnrecords[2])))+"\n")   
          place_item.append(float(emnrecords[emn_version])) #Rotation
          place_item.append(emnrecords[emn_version+1]) #Side
          place_item.append(emnrecords[emn_version+2]) #Place Status
          FreeCAD.Console.PrintMessage(str(place_item)+"\n")
          placement.append(place_item)
   FreeCAD.Console.PrintMessage("\n".join(passed_sections)+"\n")
   FreeCAD.Console.PrintMessage("Proceed "+str(Process_board_outline(doc,board_outline,drills,board_thickness))+" outlines\n")
   placement.sort(key=lambda param: (param[IDF_sort],param[0]))
   process_emp(doc,filename,placement,board_thickness)
   #place_steps(doc,placement,board_thickness) maui
   FreeCADGui.SendMsgToActiveView("ViewFit")
   FreeCADGui.activeDocument().activeView().viewAxometric()
   return 1


def Process_board_outline(doc,board_outline,drills,board_thickness):
    """Process_board_outline(doc,board_outline,drills,board_thickness)-> number proccesed loops

        adds emn geometry from emn file"""
    vertex_index=-1; #presume no vertex
    lines=-1 #presume no lines
    out_shape=[]
    out_face=[]
    for point in board_outline:
       vertex=Base.Vector(point[1],point[2],0) 
       vertex_index+=1
       if vertex_index==0:
          lines=point[0] 
       elif lines==point[0]:
           if point[3]!=0 and point[3]!=360:
              out_shape.append(Part.Arc(prev_vertex,mid_point(prev_vertex,vertex,point[3]),vertex))
              FreeCAD.Console.PrintMessage("mid point "+str(mid_point)+"\n")
           elif point[3]==360:
              per_point=Per_point(prev_vertex,vertex)
              out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,point[3]/2),vertex))
              out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,-point[3]/2),vertex))
           else:
              out_shape.append(PLine(prev_vertex,vertex))
       else:
          out_shape=Part.Shape(out_shape)
          out_shape=Part.Wire(out_shape.Edges)
          out_face.append(Part.Face(out_shape))
          out_shape=[]
          vertex_index=0 
          lines=point[0] 
       prev_vertex=vertex
    if lines!=-1:
      out_shape=Part.Shape(out_shape)
      out_shape=Part.Wire(out_shape.Edges)
      out_face.append(Part.Face(out_shape))
      outline=out_face[0]
      FreeCAD.Console.PrintMessage("Added outline\n")
      if len(out_face)>1:
        for otl_cut in out_face[1: ]:
          outline=outline.cut(otl_cut)
          FreeCAD.Console.PrintMessage("Cutting shape inside outline\n")
      for drill in drills:
        FreeCAD.Console.PrintMessage("Cutting hole inside outline\n")
        out_shape=Part.makeCircle(drill[0]/2, Base.Vector(drill[1],drill[2],0))
        out_shape=Part.Wire(out_shape.Edges)
        outline=outline.cut(Part.Face(out_shape))
      doc_outline=doc.addObject("Part::Feature","Board_outline")
      doc_outline.Shape=outline 
      #FreeCADGui.Selection.addSelection(doc_outline)
      #FreeCADGui.runCommand("Draft_Upgrade")
      #outline=FreeCAD.ActiveDocument.getObject("Union").Shape
      #FreeCAD.ActiveDocument.removeObject("Union")
      #doc_outline=doc.addObject("Part::Feature","Board_outline")
      doc_outline.Shape=outline.extrude(Base.Vector(0,0,-board_thickness))
      grp=doc.addObject("App::DocumentObjectGroup", "Board_Geoms")
      grp.addObject(doc_outline)
      doc.Board_outline.ViewObject.ShapeColor=(0.0, 0.5, 0.0, 0.0)
    return lines+1

def mid_point(prev_vertex,vertex,angle):
    """mid_point(prev_vertex,vertex,angle)-> mid_vertex
       
       returns mid point on arc of angle between prev_vertex and vertex"""
    angle=radians(angle/2)
    basic_angle=atan2(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)-pi/2
    shift=(1-cos(angle))*hypot(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)/2/sin(angle)
    midpoint=Base.Vector((vertex.x+prev_vertex.x)/2+shift*cos(basic_angle),(vertex.y+prev_vertex.y)/2+shift*sin(basic_angle),0)
    return midpoint

def split_records(line_record):
    """split_records(line_record)-> list of strings(records)
       
       standard separator list separator is space, records containting encapsulated by " """
    split_result=[]
    quote_pos=line_record.find('"')
    while quote_pos!=-1:
       if quote_pos>0:
          split_result.extend(line_record[ :quote_pos].split())
          line_record=line_record[quote_pos: ]
          quote_pos=line_record.find('"',1)
       else: 
          quote_pos=line_record.find('"',1)
       if quote_pos!=-1:
          split_result.append(line_record[ :quote_pos+1])
          line_record=line_record[quote_pos+1: ]
       else:
          split_result.append(line_record) 
          line_record=""
       quote_pos=line_record.find('"')
    split_result.extend(line_record.split())
    return split_result
    
def process_emp(doc,filename,placement,board_thickness):
   """process_emp(doc,filename,placement,board_thickness) -> place components from emn file to board"""
   global emn_version   
   fname,file_extension = os.path.splitext(filename)
   model_file=1
   #FreeCAD.Console.PrintMessage("\nfext="+file_extension)
   if file_extension == '.emn':
    filename=filename.partition(".emn")[0]+".emp"
    model_file=0
   #FreeCAD.Console.PrintMessage("\nmodel_file="+str(model_file))
   empfile=pythonopen(filename, "r")
   emp_unit=1.0 #presume milimeter like emn unit
   emp_version=2 #presume emn_version 2
   comp_height=0 #presume 0 part height
   comp_outline=[] #no part outline
   comp_GeometryName="" # no geometry name
   comp_PartNumber="" # no Part Number
   comp_height=0 # no Comp Height
   emplines=empfile.readlines()
   empfile.close()   
   passed_sections=[]
   current_section=""
   section_counter=0
   comps=[]
   for empline in emplines:
     emprecords=split_records(empline)
     if len( emprecords )==0 : continue
     if len( emprecords[0] )>4 and emprecords[0][0:4]==".END":
        passed_sections.append(current_section)
        current_section=""
        FreeCAD.Console.PrintMessage(comp_PartNumber)
        if comp_PartNumber!="":
          if comp_height==0:
            comp_height=0.1 
          comps.append((comp_PartNumber,[Process_comp_outline(doc,comp_outline,comp_height),comp_GeometryName]))
          #comps.append((comp_GeometryName,[Process_comp_outline(doc,comp_outline,comp_height),comp_PartNumber])) #maui
          #FreeCAD.Console.PrintMessage(comps)
          comp_PartNumber=""
          comp_outline=[]
     elif emprecords[0][0]==".":
        current_section=emprecords[0]
        section_counter=0
     section_counter+=1
     if current_section==".HEADER"  and section_counter==2:
        emp_version=int(float(emprecords[1]))
        FreeCAD.Console.PrintMessage("Emp version: "+emprecords[1]+"\n")
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2 and emprecords[2]=="THOU":
        emp_unit=0.0254
        #FreeCAD.Console.PrintMessage("\nUNIT THOU" )
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2 and emprecords[2]=="MM":
        emp_unit=1
        #FreeCAD.Console.PrintMessage("\nUNIT MM" )
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter==2:
        comp_outline=[] #no part outline
        comp_GeometryName=emprecords[0] # geometry name #maui 0 1ok
        comp_PartNumber=emprecords[1] # Part Number  #maui 1 0ok
        comp_height=emp_unit*float(emprecords[3]) # Comp Height
        FreeCAD.Console.PrintMessage("\ncomp_height="+str(comp_height))
     if (current_section==".ELECTRICAL" or current_section==".MECHANICAL") and section_counter>2:
        if emprecords[0]!='PROP':
            comp_outline.append([float(emprecords[1])*emp_unit,float(emprecords[2])*emp_unit,float(emprecords[3])]) #add point of outline
            #FreeCAD.Console.PrintMessage("here\n")
            FreeCAD.Console.PrintMessage(str(float(emprecords[1])*emp_unit)+" "+str(float(emprecords[2])*emp_unit)+" "+str(float(emprecords[3]))+'\n')
   FreeCAD.Console.PrintMessage("\n".join(passed_sections)+"\n")
   #Write file with list of footprint
   if IDF_diag==1:
     empfile=pythonopen(IDF_diag_path+"/footprint.lst", "w")
     for compx in comps:
       empfile.writelines(str(compx[1][1])+"\n")
     empfile.close()
   #End section of list footprint  
   #FreeCAD.Console.PrintMessage(comps)
   comps_list=comps  #maui
   comps=dict(comps)
   #FreeCAD.Console.PrintMessage(comps_list)
   grp=doc.addObject("App::DocumentObjectGroup", "EMP Models")
   offset=0
   if emn_version==3:
    offset=1
   #adding colors
   r_col=(0.411765, 0.411765, 0.411765)  #dimgrey
   c_col=(0.823529, 0.411765, 0.117647)  #chocolate
   x_col=(0.862745, 0.862745, 0.862745) #gainsboro
   l_col=(0.333333, 0.333333, 0.333333) #sgidarkgrey
   IC_col=(0.156863, 0.156863, 0.156863)  #sgiverydarkgrey
   default_col=(0.439216, 0.501961, 0.564706)  #slategrey
   idx=0
   for item in comps_list:  #maui
    #FreeCAD.Console.PrintMessage(comps_list)
    FreeCAD.Console.PrintMessage(item[1][1] + ' comp_PartNumber\n')  #comp_PartNumber
    #FreeCAD.Console.PrintMessage(comps_list[0][1][1])  #comp_PartNumber
    #FreeCAD.Console.PrintMessage(placement)
    FreeCAD.Console.PrintMessage('\n')
    if model_file==1:
        #placement[idx][0]=item[0] #' comp_GeometryName'
        #FreeCAD.Console.PrintMessage(placement)
        placement.append(['Ref', '"Geometry"', '"PartNbr_Library_emp"', 0.0, 0.0, 0.0, 0.0, 'TOP', 'ECAD'])
        placement[idx][0]=item[0] #' comp_PartNumber' to display PartNBR
        placement[idx][1]=item[0] #' comp_PartNumber'
        placement[idx][2]=item[1][1] #' comp_GeometryName'
        #placement[idx][0]=item[1][1] #' comp_PartNumber' to display PartNBR
        #placement[idx][1]=item[1][1] #' comp_PartNumber'
        #placement[idx][2]=item[0] #' comp_GeometryName'
        #FreeCAD.Console.PrintMessage(item[1][1]+' idx='+str(idx)+'\n')
        #FreeCAD.Console.PrintMessage(placement)
        idx=idx+1
   FreeCAD.Console.PrintMessage(placement)
   #FreeCAD.Console.PrintMessage(' list\n') 
   idx=0
   for place_item in placement:
     #FreeCAD.Console.PrintMessage(place_item[1]+'pitem1'+place_item[2]+'pitem2\n')
     #FreeCAD.Console.PrintMessage(comps_list[idx][0])
     #FreeCAD.Console.PrintMessage(comps_list[idx][1])
     for item in comps_list:
        FreeCAD.Console.PrintMessage('\n'+place_item[1]+'pitem1'+place_item[2]+'pitem2\n')
        FreeCAD.Console.PrintMessage(item);FreeCAD.Console.PrintMessage('\n')
        FreeCAD.Console.PrintMessage(item[0]);FreeCAD.Console.PrintMessage('\n')
        FreeCAD.Console.PrintMessage(item[1][1]);FreeCAD.Console.PrintMessage('\n')
        #if (place_item[2] in item) and (place_item[1] in item[1][1]):
        ##if (place_item[2] in item) and (place_item[1] in item[1][1]):
        #if (place_item[1].strip('"') in item[0].strip('"')) and (place_item[2].strip('"') in item[1][1].strip('"')):
        #if (place_item[1].strip('"') in item[0].strip('"')) and (place_item[2].strip('"') in item[1][1].strip('"')):
        if (place_item[1] in item[0]) and (place_item[2] in item[1][1]):
     #if comps.has_key(place_item[2]):
     #if comps.has_key(place_item[2]) and comps.has_key(place_item[1]): #1 maui
     #if comps_list[idx][0]==(place_item[2]) and comps_list[idx][1]==(place_item[1]): #1 maui
            doc_comp=doc.addObject("Part::Feature",place_item[0])
            FreeCAD.Console.PrintMessage("Adding EMP model "+str(place_item[0])+"\n")
            ##doc_comp.Shape=comps[place_item[2]][0] #1 maui
            doc_comp.Shape=item[1][0] #1 maui
            comp_col=default_col
            if (doc_comp.Label.upper().startswith('X')):
                comp_col=x_col
            if (doc_comp.Label.upper().startswith('L')):
                comp_col=l_col
            if (doc_comp.Label.upper().startswith('R')):
                comp_col=r_col
            if (doc_comp.Label.upper().startswith('C')):
                comp_col=c_col
            if (doc_comp.Label.upper().startswith('S')|doc_comp.Label.upper().startswith('Q')|\
                doc_comp.Label.upper().startswith('D')|doc_comp.Label.upper().startswith('T')|doc_comp.Label.upper().startswith('U')):
                comp_col=IC_col
        
            if IDF_colorize==1:
                doc_comp.ViewObject.ShapeColor=comp_col  #maui
            doc_comp.ViewObject.DisplayMode=EmpDisplayMode
            z_pos=0
            rotateY=0
            if place_item[6+offset]=='BOTTOM':
                rotateY=pi
                z_pos=-board_thickness
            placmnt=Base.Placement(Base.Vector(place_item[3],place_item[4],z_pos+offset*place_item[5]),toQuaternion(rotateY,place_item[5+offset]*pi/180,0))
            doc_comp.Placement=placmnt
            doc = FreeCAD.ActiveDocument
            if model_file==0:
                grp.addObject(doc_comp)
            else:
                doc.ActiveObject.ViewObject.Visibility=False
                #doc.ActiveObject.ViewObject.BoundingBox = True
     idx=idx+1
   return 1

def Process_comp_outline(doc,comp_outline,comp_height):
    """Process_comp_outline(doc,comp_outline,comp_height)->part shape
       Create solid component shape base on its outline"""
    vertex_index=-1; #presume no vertex
    #FreeCAD.Console.PrintMessage(" Process_comp_outline\n")
    out_shape=[]
    if comp_outline==[]:  #force 0.2mm circle shape for components without place outline definition
       comp_outline.append([0.0,0.0,0.0])
       comp_outline.append([0.1,0.0,360.0])
    for point in comp_outline:
       vertex=Base.Vector(point[0],point[1],0) 
       vertex_index+=1
       if vertex_index>0:
         if point[2]!=0 and point[2]!=360:
            out_shape.append(Part.Arc(prev_vertex,mid_point(prev_vertex,vertex,point[2]),vertex))
            FreeCAD.Console.PrintMessage("mid point "+str(mid_point)+"\n")
         elif point[2]==360:
            per_point=Per_point(prev_vertex,vertex)
            out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,point[2]/2),vertex))
            out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,-point[2]/2),vertex))
         else:
            out_shape.append(PLine(prev_vertex,vertex))
       prev_vertex=vertex
    out_shape=Part.Shape(out_shape)
    out_shape=Part.Wire(out_shape.Edges)
    out_shape=Part.Face(out_shape)
    out_shape=out_shape.extrude(Base.Vector(0,0,comp_height))
    #Part.show(out_shape)
    return out_shape
    
def toQuaternion(heading, attitude,bank): # rotation heading=arround Y, attitude =arround Z,  bank attitude =arround X
    """toQuaternion(heading, attitude,bank)->FreeCAD.Base.Rotation(Quternion)"""
    c1 = cos(heading/2)
    s1 = sin(heading/2)
    c2 = cos(attitude/2)
    s2 = sin(attitude/2)
    c3 = cos(bank/2)
    s3 = sin(bank/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w = c1c2*c3 - s1s2*s3
    x = c1c2*s3 + s1s2*c3
    y = s1*c2*c3 + c1*s2*s3
    z = c1*s2*c3 - s1*c2*s3
    return  FreeCAD.Base.Rotation(x,y,z,w)  

def Per_point(prev_vertex,vertex):
    """Per_point(center,vertex)->per point

       returns opposite perimeter point of circle"""
    #basic_angle=atan2(prev_vertex.y-vertex.y,prev_vertex.x-vertex.x)
    #shift=hypot(prev_vertex.y-vertex.y,prev_vertex.x-vertex.x)
    #perpoint=Base.Vector(prev_vertex.x+shift*cos(basic_angle),prev_vertex.y+shift*sin(basic_angle),0)
    perpoint=Base.Vector(2*prev_vertex.x-vertex.x,2*prev_vertex.y-vertex.y,0)
    return perpoint

  
