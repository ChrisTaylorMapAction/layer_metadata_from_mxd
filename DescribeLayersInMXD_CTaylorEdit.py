#Import modules...
import arcpy, os, fnmatch, csv, datetime

#User input variables...

#User Input - The folder where the MXDs are stored
mxddirectory = filename = arcpy.GetParameterAsText(0)
##outputFile = "testing123.csv"
# User Input - The name of the file
filename = arcpy.GetParameterAsText(1)

# Optional variables
##dateonly = datetime.date.today()
##datestring = dateonly.strftime('%Y_%m_%d')
##foldername = os.path.basename(mxddirectory)



# outputfile uses the current date, file descriptor, and the folder name
outputFile = filename + ".csv"

#Optional variable
##outputFile = datestring + "_" + filename + "_"+ foldername + ".csv"

#outputFile = raw_input('Enter Output FileName (include extension xxx.csv):  ')
#outputcsvlocation = r"C:\Mapaction\SDG\ListLayersInMxds"
outputcsvlocation = os.path.join(mxddirectory,outputFile)

starttime = datetime.datetime.now()
print "started job at ", str(starttime)

#Create an empty list of ArcMap documents to process...
mxd_list=[]

#Walk through the input directory, adding paths for each .mxd file found to the list...

for dirpath, dirnames, filenames in os.walk(mxddirectory):
    for filename in filenames:
        print filename
        if fnmatch.fnmatch(filename, "*.mxd"):
            mxd_list.append(os.path.join(dirpath, filename))

if len(mxd_list) > 0:
    #Create the csv file...
    outputcsv = open(outputcsvlocation,"wb")
    writer = csv.writer(outputcsv, dialect = 'excel')
    writer.writerow(["Runtime","mxdPath","dataFrameName","layerName","layerLongName","layerDescription","layerSource","isVisible","isDataSourceBroken","definitionQuery","transparency","brightness","contrast","showLabels","symbologyType","isFeatureLayer","maxScale","minScale","isRaster", "IsGroupLayer"])
    #Iterate through the list of ArcMap Documents...
    for mxdpath in mxd_list:
        print mxdpath
        mxdname = os.path.split(mxdpath)[1]
        print mxdname
        try:
            mxd = arcpy.mapping.MapDocument(mxdpath)
            #Iterate through the ArcMap Document layers...
            print 'got mxd mapping'
            datafs = arcpy.mapping.ListDataFrames(mxd)
            for df in datafs: #arcpy.mapping.ListDataFrames(mxd):
                dataframeName = df.name
                print dataframeName
                for layer in arcpy.mapping.ListLayers(mxd,"",df):
                    if not layer.isGroupLayer:
                        runtime = starttime
                        print runtime

                        layerName = layer.name
                        print layerName
                        layerLongName = layer.longName
                        print layerLongName

                        if layer.supports("DESCRIPTION"):
                            desc = layer.description
                        else:
                            desc = "no desc"
                        print desc

                        if layer.supports("DATASOURCE"):
                            layerSource = layer.dataSource
                        else:
                            layerSource = "None"
                        print layerSource

                        IsVisible = layer.visible
                        print 'done visible'

                        isBroken = layer.isBroken
                        print isBroken
                        print "broken works"

                        if layer.supports("DEFINITIONQUERY"):
                            defQry = layer.definitionQuery
                        else:
                            defQry = "None"
                        print defQry

                        if layer.supports("TRANSPARENCY"):
                            transparency = layer.transparency
                        else:
                            transparency = "None"
                        print transparency

                        if layer.supports("BRIGHTNESS"):
                            brightness = layer.brightness
                        else:
                            brightness = "None"
                        print brightness
                        if layer.supports("CONTRAST"):
                            contrast = layer.contrast
                        else:
                            contrast = "None"
                        print contrast
                        if layer.supports("SHOWLABELS"):
                            showLabels = layer.showLabels
                        else:
                            showLabels = "None"
                        print showLabels

                        if layer.supports("SYMBOLOGYTYPE"):
                            symbologyType = layer.symbologyType
                        else:
                            symbologyType = "None"
                        print symbologyType

                        IsFeatureLayer = layer.isFeatureLayer
                        print 'done isFeatureLayer'

                        maxScale = layer.maxScale
                        print maxScale

                        minScale = layer.minScale
                        print minScale

                        isRaster = layer.isRasterLayer
                        print isRaster

##                        isGrouplayer = layer.isGroupLayer
##                        print isGrouplayer

                        layerattributes = [runtime, mxdpath, dataframeName, layerName, layerLongName, desc, layerSource, IsVisible, isBroken, defQry, transparency, brightness, contrast,showLabels ,symbologyType, IsFeatureLayer, maxScale, minScale, isRaster]
                        #Write the attributes to the csv file...

                        writer.writerow(layerattributes)
            del mxd
        except:
            arcpy.AddMessage("EXCEPTION: {0}".format(mxdpath))
    outputcsv.close()
#if no ArcMap documents in the specified folder notify via error message...
else:
    arcpy.AddError("No ArcMap documnents found, please check path provided.")
