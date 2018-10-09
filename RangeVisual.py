# /*
#  * @Author: Muhaowei
#  * @Date: 2018-08-21 21:31:46
#  * @LastEditors: Muhaowei
#  * @LastEditTime: 2018-08-21 21:31:46
#  * @Description: 
#  */
from osgeo import ogr, osr
import os
import sys

def CreateGeo(MBRLine):
    # Create ring #1
    MBRArr = MBRLine.split(',')
    for i in range(0, 4):
        MBRArr[i] = float(MBRArr[i])
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(MBRArr[0], MBRArr[3])
    ring.AddPoint(MBRArr[2], MBRArr[3])
    ring.AddPoint(MBRArr[2], MBRArr[1])
    ring.AddPoint(MBRArr[0], MBRArr[1])
    ring.AddPoint(MBRArr[0], MBRArr[3])
    # Create polygon #1
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


if __name__ == '__main__':
    filename = sys.argv[-1]
    name = filename.split('.')[0]
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
    MBRLines = open(filename, 'r').readlines()
    for line in MBRLines[1:]:
        MBRLine = line.replace('\n', '')
        poly = CreateGeo(MBRLine)
        multipolygon.AddGeometry(poly)

    # create the shapefile
    driver = ogr.GetDriverByName("Esri Shapefile")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    ds = driver.CreateDataSource(name+".shp")
    out_layr = ds.CreateLayer('', srs=srs, geom_type=ogr.wkbMultiPolygon)
    print(multipolygon.GetGeometryCount())
    # create the field
    out_layr.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    # Create the feature and set values
    out_defn = out_layr.GetLayerDefn()
    out_feat = ogr.Feature(out_defn)
    value = 0
    for in_feat in multipolygon:
        geom = in_feat
        out_feat.SetGeometry(geom)
        value = value + 1
        out_feat.SetField('id', value)
        out_layr.CreateFeature(out_feat)
        # close the shapefile
    ds.Destroy()

    #  # create the shapefile
    # driver = ogr.GetDriverByName("Esri Shapefile")
    # srs = osr.SpatialReference()
    # srs.ImportFromEPSG(4326)
    # ds = driver.CreateDataSource("outputlocation1.shp")
    # out_layr = ds.CreateLayer('',srs = srs, geom_type= ogr.wkbMultiPolygon)
    # print(multipolygon.GetGeometryCount())
    # # create the field
    # out_layr.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    # # Create the feature and set values
    # out_defn = out_layr.GetLayerDefn()
    # out_feat = ogr.Feature(out_defn)
    # for in_feat in multipolygon:
    #     geom = in_feat
    #     out_feat.SetGeometry(geom)
    #     for value in range(multipolygon.GetGeometryCount()):
    #         print(value)
    #         out_feat.SetField('id', value)
    #     out_layr.CreateFeature(out_feat)
    #     # close the shapefile
    # ds.Destroy()
