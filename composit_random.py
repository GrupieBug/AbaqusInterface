# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from random import randrange, uniform
import math

porosity = 1 - ((math.pi * (1.5 ** 1) * 16) / (20 * 20))
porosity = .7173
dim = 20.0
num_fibers = 16
radius = float(math.sqrt((1 - porosity) * dim * dim / (math.pi * num_fibers)))
centers = []

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=(dim * 10))
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0),
                                                        point2=(dim, dim))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Composite', type=
DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Composite'].BaseShell(sketch=
                                                   mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

for i in range(1, num_fibers + 1):
    center_x = uniform(radius, dim - radius)
    center_y = uniform(radius, dim - radius)

    if centers:
        colliding = True
        while colliding:
            for point in centers:
                if point[0] - 2 * radius <= center_x <= point[0] + 2 * radius and point[1] - 2 * radius <= center_y <= \
                        point[1] + 2 * radius:
                    center_x = uniform(radius, dim - radius)
                    center_y = uniform(radius, dim - radius)
                    colliding = True
                    break
                else:
                    colliding = False
        centers.append([center_x, center_y])
    else:
        centers.append([center_x, center_y])

    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=1.41, name='__profile__',
                                            sheetSize=56.56, transform=
                                            mdb.models['Model-1'].parts['Composite'].MakeSketchTransform(
                                                sketchPlane=mdb.models['Model-1'].parts['Composite'].faces.findAt((
                                                    0.1, 0.1, 0.0), (0.0, 0.0, 1.0)), sketchPlaneSide=SIDE1,
                                                sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
    mdb.models['Model-1'].parts['Composite'].projectReferencesOntoSketch(filter=
                                                                         COPLANAR_EDGES,
                                                                         sketch=mdb.models['Model-1'].sketches[
                                                                             '__profile__'])
    #    mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    #        gridOrigin=(-10.0, -10.0))
    mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
        center_x, center_y), point1=((center_x + radius), center_y))
    mdb.models['Model-1'].parts['Composite'].PartitionFaceBySketch(faces=
                                                                   mdb.models['Model-1'].parts[
                                                                       'Composite'].faces.findAt(((0.1, 0.1,
                                                                                                   0.0),)),
                                                                   sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].Material(name='Steel')
mdb.models['Model-1'].materials['Steel'].Elastic(table=((1.77, 0.001),))
mdb.models['Model-1'].Material(name='Polymer')
mdb.models['Model-1'].materials['Polymer'].Elastic(table=((1700.0, 0.4),))
mdb.models['Model-1'].HomogeneousSolidSection(material='Steel', name='Steel',
                                              thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='Polymer', name=
'Polymer', thickness=None)
mdb.models['Model-1'].parts['Composite'].Set(faces=
                                             mdb.models['Model-1'].parts['Composite'].faces.findAt(((9.148826, 1.121772,
                                                                                                     0.0),)),
                                             name='Set-1')
mdb.models['Model-1'].parts['Composite'].SectionAssignment(offset=0.0,
                                                           offsetField='', offsetType=MIDDLE_SURFACE, region=
                                                           mdb.models['Model-1'].parts['Composite'].sets['Set-1'],
                                                           sectionName=
                                                           'Polymer', thicknessAssignment=FROM_SECTION)

for i in range(1, num_fibers + 1):
    center_x = centers[i - 1][0]
    center_y = centers[i - 1][1]

    mdb.models['Model-1'].parts['Composite'].Set(faces=
                                                 mdb.models['Model-1'].parts['Composite'].faces.findAt(
                                                     ((center_x, center_y,
                                                       0.0),)), name='Set-%d' % (i + 1))
    mdb.models['Model-1'].parts['Composite'].SectionAssignment(offset=0.0,
                                                               offsetField='', offsetType=MIDDLE_SURFACE, region=
                                                               mdb.models['Model-1'].parts['Composite'].sets[
                                                                   'Set-%d' % (i + 1)], sectionName='Steel'
                                                               , thicknessAssignment=FROM_SECTION)

mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Composite-1',
                                            part=mdb.models['Model-1'].parts['Composite'])
mdb.models['Model-1'].StaticStep(initialInc=0.01, maxInc=0.1, maxNumInc=10000,
                                 minInc=1e-12, name='Step-1', previous='Initial')
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side1Edges=
mdb.models['Model-1'].rootAssembly.instances['Composite-1'].edges.findAt(((
                                                                              5.0, 20.0, 0.0),)))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1',
                               distributionType=UNIFORM, field='', magnitude=-10.0, name='Load-1', region=
                               mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])
mdb.models['Model-1'].rootAssembly.Surface(name='Surf-2', side1Edges=
mdb.models['Model-1'].rootAssembly.instances['Composite-1'].edges.findAt(((
                                                                              15.0, 0.0, 0.0),)))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1',
                               distributionType=UNIFORM, field='', magnitude=-10.0, name='Load-2', region=
                               mdb.models['Model-1'].rootAssembly.surfaces['Surf-2'])
mdb.models['Model-1'].rootAssembly.Set(name='Set-1', vertices=
mdb.models['Model-1'].rootAssembly.instances['Composite-1'].vertices.findAt(
    ((0.0, 0.0, 0.0),)))
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1',
                                     distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
                                     'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=0.0,
                                     u2=UNSET, ur3=UNSET)
mdb.models['Model-1'].parts['Composite'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF,
    hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
    elemCode=CPE3, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].parts['Composite'].faces.findAt(((9.148826, 1.121772,
                                                            0.0),)),))

for i in range(1, num_fibers + 1):
    center_x = centers[i - 1][0]
    center_y = centers[i - 1][1]

    mdb.models['Model-1'].parts['Composite'].setElementType(elemTypes=(ElemType(
        elemCode=CPE4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF,
        hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
        elemCode=CPE3, elemLibrary=STANDARD)), regions=(
        mdb.models['Model-1'].parts['Composite'].faces.findAt(((center_x, center_y,
                                                                0.0),)),))

mdb.models['Model-1'].parts['Composite'].seedPart(deviationFactor=0.1,
                                                  minSizeFactor=0.1, size=0.1)
mdb.models['Model-1'].parts['Composite'].generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF,
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF,
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF,
        multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE,
        numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
        ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
# Property of Not Real Engineering
# Author: Shank S. Kulkarni
