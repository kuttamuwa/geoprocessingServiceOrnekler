"""
@Author: Umut Ucok

ArcGIS Server - REST üzerinde çalışacak ornek Python script.

Kullanıcının yukledigi bir dosyayi Raster Catalog'a aktaralim.
Not: Raster Catalog ArcMap'te vardır, ArcGIS Pro'da yoktur. Orada Mosaic Dataset var ama Image Server lisansı ister.

"""

import arcpy
from datetime import datetime
arcpy.g

in_raster = arcpy.GetParameterAsText(0)
# Asagidaki sabit mosaic path'i kendinizdeki mosaic dataset path'i ile degistirin.
sabit_catalog_path = r"C:\Users\LENOVO\PycharmProjects\geoprocessingServiceOrnekler\datasources\ornekFGDB.gdb\PlanCatalog"
tarihfield = "EklenmeTarihi"

# Adim 1: Add
arcpy.RasterToGeodatabase_conversion(in_raster, sabit_catalog_path)

"""
Ben updateCursor ile devam ettim, dileyen arkadaslar asagidaki kismi kullanabilir:
# Adim 2 : Tarih Sutununu guncellemek
# Model ile ayni yapalim :)
arcpy.MakeRasterCatalogLayer_management(sabit_catalog_path, "CatalogLayer")
arcpy.SelectLayerByAttribute_management("CatalogLayer", "NEW_SELECTION", "EklenmeTarihi is NULL")
arcpy.CalculateField_management('PlanCatalog_Layer', 'EklenmeTarihi', 'datetime.datetime.now( )', 'PYTHON_9.3')

"""

# Adim 2: Tarih sutununu guncellemek
# Modeldekinden farkli bi sey yapalim :)

try:
    with arcpy.da.UpdateCursor(sabit_catalog_path, [tarihfield], """EklenmeTarihi is NULL""") as ucursor:
        for row in ucursor:
            row[0] = datetime.now()

            ucursor.updateRow(row)

except Exception as err:
    arcpy.AddError("Arac calisirken bir hata alindi. \n"
                   "Hata : {0}".format(str(err)))

