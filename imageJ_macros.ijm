// This imageJ macro is adapted from https://github.com/shigekiwatanabe/SynapsEM


macro 'Freehand [f4]' {setTool(3)}
macro 'Straight Line [7]' {setTool(4)}
macro 'Freeline [8]' {setTool(6)}
macro 'Wand [f10]' {setTool(8)}

macro "Shuffle slices [s]" {
    for (i = nSlices - 1; i >= 1; i--) {
        j = round(i * random() - 0.5) + 1;
        Stack.swap(i, j);
    } 
}


macro "Add Active Zone [n9]" {
  type = selectionType();
  if (type ==7) {
    getSelectionCoordinates(xq, yq);
    List.setMeasurements;
    a = List.getValue("Length");
    roiManager("Add");
    roiManager("Select",roiManager("Count")-1);    
    roiManager("Rename","Active_zone-"+toString(xq[0])+","+toString(yq[0])+","+toString(a));
  } else {
   print("no freehand line");
   beep;
  }
}


macro "Add Endosome [n6]" {
  type = selectionType();
  if (type ==3 || type==2) {
    roiManager("Add");
    roiManager("Select",roiManager("Count")-1);
    getStatistics(area);  
    getSelectionBounds(x, y, width, height);
    roiManager("Rename","Endosome-"+toString(area)+","+toString(x+width/2)+","+toString(y+height/2));
  } else {
   print("no freehand");
   beep;
  }
}

macro "Add SV [n1]" {
  type = selectionType();
  if (type ==5) {
    getLine(x1, y1, x2, y2, lineWidth);
    xc=(x2+x1)/2;
    yc=(y2+y1)/2;
print(xc+" , "+yc);
    r=sqrt(pow((x2-x1),2)+pow((y2-y1),2))/2;
    makeOval(xc-r,yc-r,r*2,r*2);
    roiManager("Add");
    roiManager("Select",roiManager("Count")-1);    
    getSelectionBounds(x, y, width, height);
    roiManager("Rename","SV-"+toString(x+width/2)+","+toString(y+height/2));
  } else {
   print("no line");
   beep;
  }
}


macro "Add docked SV [n3]" {
  type = selectionType();
  if (type ==5) {
    getLine(x1, y1, x2, y2, lineWidth);
    xc=(x2+x1)/2;
    yc=(y2+y1)/2;
print(xc+" , "+yc);
    r=sqrt(pow((x2-x1),2)+pow((y2-y1),2))/2;
    makeOval(xc-r,yc-r,r*2,r*2);
    roiManager("Add");
    roiManager("Select",roiManager("Count")-1);    
    getSelectionBounds(x, y, width, height);
    roiManager("Rename","docked_SV-"+toString(x+width/2)+","+toString(y+height/2));
  } else {
   print("no line");
   beep;
  }
}


macro "Export ROI[p]" {
  n = roiManager("count");
  id = getInfo("slice.label");
  dir = getDirectory("");
  file = File.open(dir+id+".txt");
  for (j=0; j<n; j++) {
    roiManager("select", j);
    type = selectionType();
    fullname = call("ij.plugin.frame.RoiManager.getName", j);
    name=substring(fullname,0,indexOf(fullname,"-"));
    if (type ==2 || type==3) {
      getStatistics(area);
      getSelectionCoordinates(xl, yl);
      area=toString(area);
      xvals=toString(xl[0]);
      yvals=toString(yl[0]);
      for (i=1; i< lengthOf(xl); i++) {
        xvals=toString(xvals+","+xl[i]);
        yvals=toString(yvals+","+yl[i]);
      }  
      print(file,type+"\t"+name+"\t"+area+"\t"+xvals+"\t"+ yvals);
    }  else if (type==1) {
      getBoundingRect(x, y, w, h);
      print (file,type+"\t"+name+"\t"+x+w/2+"\t"+y+h/2+"\t"+w/2);
    }  else if (type==10) {
      getSelectionCoordinates(xm, ym);   
      print (file,type+"\t"+name+"\t"+xm[0]+"\t"+ym[0]);
    } else if (type==7) {
      getSelectionCoordinates(xn, yn);
      List.setMeasurements;
      perimeter=List.getValue("Length");
      xcords=toString(xn[0]);   
      ycords=toString(yn[0]); 
      for (k=1;k< lengthOf(xn); k++) {
        xcords=toString(xcords+","+xn[k]);
        ycords=toString(ycords+","+yn[k]);
      }
      print (file,type+"\t"+name+"\t"+perimeter+"\t"+xcords+"\t"+ycords);
    } else {
      print("unknown type"+type);
    }
  }
  if (n == 1) {
    roiManager("Delete");
  } else if (n > 1) {
    roiManager("Delete");
    roiManager("Delete");
  }
  run("Next Slice [>]");
}


macro "Import ROI[i]" {
  file=File.openAsString("");
  record=split(file,"\n")
  for (i=0; i<lengthOf(record); i++) {
    field=split(record[i],"\t");
    type=field[0];
    if (type == 1) {
      xc=field[2];
      yc=field[3];
      r=field[4];
      name=field[1]+"-"+xc+","+yc;
      makeOval(xc-r,yc-r,r*2,r*2);
      roiManager("Add");
      roiManager("Select",roiManager("Count")-1);    
      roiManager("Rename",name);
    } else if (type == 3) {
      area=field[2];
      xl=split(field[3],",");
      yl=split(field[4],",");
      makeSelection("freehand",xl,yl);
      roiManager("Add");
      roiManager("Select",roiManager("Count")-1);
      getStatistics(area); 
      getSelectionBounds(x, y, width, height);
      roiManager("Rename",toString(field[1])+"-"+toString(area)+","+toString(x+width/2)+","+toString(y+height/2)); 
    } else if (type==7) {
      xn=split(field[3],",");
      yn=split(field[4],",");
      a=field[2];
      makeSelection("freeline",xn,yn);
      roiManager("Add");
      roiManager("Select",roiManager("Count")-1);
      getSelectionCoordinates(xn, yn);
      roiManager("Rename",toString(field[1])+"-"+toString(xn[0])+","+toString(yn[0])+","+toString(a));
    } else if (type == 10) {
      xm=split(field[2],",");
      ym=split(field[3],",");
      makeSelection("point",xm,ym);
      roiManager("Add");
      roiManager("Select",roiManager("Count")-1);
      getSelectionCoordinates(xp,yp);
      roiManager("Rename",toString(field[1])+"-"+toString(xp[0])+","+toString(yp[0]));      
    }
  }
}

macro "Set scale [f2]"{
       run("Set Scale...", "distance=1 known=1 pixel=1 unit=[ ] global");
}

macro "Open image sequence[f1]"{
       run("Image Sequence...");
       run("Set Scale...", "distance=1 known=1 pixel=1 unit=[ ] global");
       run("Brightness/Contrast...");
}



