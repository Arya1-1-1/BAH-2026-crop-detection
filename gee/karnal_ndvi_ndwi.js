// Define Karnal district, Haryana boundary
var districts = ee.FeatureCollection("FAO/GAUL/2015/level2");
var karnal = districts.filter(ee.Filter.eq('ADM2_NAME', 'Karnal'));

// Center map on Karnal and add boundary
Map.centerObject(karnal, 10);
Map.addLayer(karnal, {color: 'red'}, 'Karnal District Boundary');// Load Sentinel-2 surface reflectance data
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(karnal)
  .filterDate('2026-06-01', '2026-07-05')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20));

// Print how many images matched
print('Number of images:', s2.size());

// Create a median composite (cleaner single image from all matches)
var composite = s2.median().clip(karnal);

// Visualize as true color (natural look)
var visParams = {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000};
Map.addLayer(composite, visParams, 'Sentinel-2 True Color');// Calculate NDVI (vegetation health index)
var ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI');
var ndviVis = {min: -0.2, max: 0.8, palette: ['red', 'yellow', 'green']};
Map.addLayer(ndvi, ndviVis, 'NDVI');