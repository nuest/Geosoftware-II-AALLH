import spatialSimilarity
##Geometry

def test_spatialdistance_Geometry():
  total =  spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
  assert total == 74.02

def test_spatialOverlap_Geometry():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
    assert total == 41.26

def test_similarArea_Geometry():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
    assert total == 58.98

## Points
def test_spatialdistance_Points():
  total =  spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
  assert total == 99.01

def test_spatialOverlap_Points():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 81.45

def test_similarArea_Points():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 100.0

##Line and Point 

def test_spatialdistance_LineAndPoint():
  total =  spatialSimilarity.spatialDistance([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
  assert total == 49.97

def test_spatialOverlap_LineAndPoint():
    total = spatialSimilarity.spatialOverlap([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 0.09

def test_similarArea_LineAndPoint():
    total = spatialSimilarity.similarArea([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 100.0
  
## Polygon and Point 

def test_spatialdistance_PolygonAndPoint():
  total =  spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
  assert total == 50.57

def test_spatialOverlap_PolygonAndPoint():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 0.0

def test_similarArea_PolygonAndPoint():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134],[13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert total == 0.0

## SameBoundingBox

def test_spatialdistance_SameBoundingBox():
  total =  spatialSimilarity.spatialDistance([0.439453,29.688053,3.911133,31.765537],[0.439453,29.688053,3.911133,31.765537])
  assert total == 100.00

def test_spatialOverlap_SameBoundingBox():
    total = spatialSimilarity.spatialOverlap([0.439453,29.688053,3.911133,31.765537],[0.439453,29.688053,3.911133,31.765537])
    assert total == 100.0

def test_similarArea_SameBoundingBox():
    total = spatialSimilarity.similarArea([0.439453,29.688053,3.911133,31.765537],[0.439453,29.688053,3.911133,31.765537])
    assert total == 100.0

## similar boundingBoxes that are close together

def test_spatialdistance_SBBTACT():
  total =  spatialSimilarity.spatialDistance([7.596703,51.950402,7.656441,51.978536],[7.588205,51.952412,7.616014,51.967644])
  assert total == 66.08

def test_spatialOverlap_SSBBTACT():
    total = spatialSimilarity.spatialOverlap([7.596703,51.950402,7.656441,51.978536],[7.588205,51.952412,7.616014,51.967644])
    assert total == 17.5

def test_similarArea_SBBTACT():
    total = spatialSimilarity.similarArea([7.596703,51.950402,7.656441,51.978536],[7.588205,51.952412,7.616014,51.967644])
    assert total == 25.2

## Far away boundingboxes 

def test_spatialdistance_fABB():
  total =  spatialSimilarity.spatialDistance([7.596703,51.950402,7.656441,51.978536],[-96.800194,32.760085,-96.796353,32.761385])
  assert total == 0

def test_spatialOverlap_fABB():
    total = spatialSimilarity.spatialOverlap([7.596703,51.950402,7.656441,51.978536],[-96.800194,32.760085,-96.796353,32.761385])
    assert total == 0.0

def test_similarArea_fABB():
    total = spatialSimilarity.similarArea([7.596703,51.950402,7.656441,51.978536],[-96.800194,32.760085,-96.796353,32.761385])
    assert total == 0.42




