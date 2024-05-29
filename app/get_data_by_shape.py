import geopandas as gpd
from pandas import DataFrame
from shapely import Point


def get_data_by_shape(df: DataFrame, shape: DataFrame | gpd.GeoDataFrame, latitude_title: str,
                      longitude_title: str) -> gpd.GeoDataFrame:
    geometry = [Point(xy) for xy in zip(df[longitude_title], df[latitude_title])]
    points_geo = gpd.GeoDataFrame(df, geometry=geometry, crs=shape.crs)
    points_inside_shape = gpd.sjoin(points_geo, shape, op='within')
    return points_inside_shape
