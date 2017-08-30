kicadpcb2dxf python utility to export pcbnew drawing layers to dxf 
  **dxf exporter for mechanical layers of a kicad_pcb board**
  - "Dwgs", "Cmts", "Edge", "Eco1", "Eco2", "F.Fab", "B.Fab", "F.CrtYd", "B.CrtYd"
  - the dxf generated has single line draw as it should be for mechanical interchange (this option is missing in pcbnew plot)
  
  how to launch:
  
  **python kicadpcb2dxf.py -f kicad-board.kicad_pcb**