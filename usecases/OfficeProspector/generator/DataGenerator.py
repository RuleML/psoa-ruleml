from random import *
from decimal import *
from OrderedSet import OrderedSet
import csv

dataPrefix = ''

class IRI:
    def __init__(self, name, prefix=dataPrefix):
        self.iri = ''.join([prefix, ':', name])

    def __str__(self):
        return self.iri


def psoastr(obj):
    objtype = type(obj)
    if objtype is str:
        return ''.join(['"', obj, '"'])
    else:
        return str(obj)


def randomListFromDist(dist):
    l = list()
    for d in dist:
        if random() < d[1]:
            l.append(d[0])
    return l


class PSOAAtom:
    primTypes = {IRI, str, int, float, Decimal}
    isIndependent = False
    writtenObjs = set()

    def __init__(self):
        pass

    def __str__(self):
        cls = type(self)
        segments = list()
        args = self.__dict__.copy()
        oid = args.pop('oid', None)
        if oid:
            segments += [str(oid), '#']
        segments += [str(args.pop('predicate')), '(']
        if cls.isIndependent and not cls.posArgNames.isEmpty():
            segments += ('-[')
        try:
            for name in cls.posArgNames:
                segments += [psoastr(args.pop(name)), ' ']
        except AttributeError:
            pass
        
        if cls.isIndependent and segments[-1] == ' ':
            segments[-1] = '] '
        for arg in sorted(args.items()):
            slotName = str(IRI(arg[0]))
            if type(arg[1]) is list:
                for val in arg[1]:
                    segments += [slotName, '->', psoastr(val), ' ']
            else:
                segments += [slotName, '->', psoastr(arg[1]), ' ']
        segments[-1] = ')'
        return ''.join(segments)

    def writeObj(self, arg, out, nestedArgs, nested=False):
        argType = type(arg)
        assert argType is not list
        if issubclass(argType, PSOAAtom):
            nestedArgs.add(arg)
            if nested and arg not in PSOAAtom.writtenObjs:
                arg.write(out)
            else:
                out.write(str(arg.oid))
        elif argType is str:
            print('"', arg, '"', sep='', end='', file=out)
        else:
            out.write(str(arg))

    def write(self, out, indent=0, nested=False):
        if self in PSOAAtom.writtenObjs:
            return

        PSOAAtom.writtenObjs.add(self)
        cls = type(self)
        args = self.__dict__.copy()
        oid = args.pop('oid', None)
        out.write(' '*indent)
        if oid:
            print(oid, '#', sep='', end='', file=out)
        print(args.pop('predicate'), '(', sep='', end='', file=out)
        nestedArgs = OrderedSet()
        try:
            first = True
            for name in cls.posArgNames:
                if first:
                    first = False
                    if cls.isIndependent:
                        out.write('-[')
                else:
                    out.write(' ')
                self.writeObj(args.pop(name), out, nestedArgs)
            if cls.isIndependent and not first:
                out.write(']')
            printSpace = True
        except AttributeError:
            printSpace = False

        for arg in sorted(args.items()):
            slotName = str(IRI(arg[0]))
            if type(arg[1]) is list:
                for val in arg[1]:
                    if printSpace:
                        print(' ', slotName, '->', sep='', end='', file=out)
                    else:
                        print(slotName, '->', sep='', end='', file=out)
                        printSpace = True
                    self.writeObj(val, out, nestedArgs, nested)
            else:
                if printSpace:
                    print(' ', slotName, '->', sep='', end='', file=out)
                else:
                    print(slotName, '->', sep='', end='', file=out)
                    printSpace = True
                self.writeObj(arg[1], out, nestedArgs, nested)
        out.write(')\n')
        if not nested:
            for arg in nestedArgs:
                arg.write(out, indent, False)

    @classmethod
    def genOID(cls, oidPrefix, nsPrefix=dataPrefix):
        try:
            cls.idNum += 1
        except AttributeError:
            cls.idNum = 1

        return IRI(oidPrefix + str(cls.idNum), nsPrefix)


ratings = [IRI('none', 'op-rtg'),
           IRI('basic', 'op-rtg'),
           IRI('regular', 'op-rtg'),
           IRI('advanced', 'op-rtg'),
           IRI('excellent', 'op-rtg')]


class Address:
    def __init__(self, streetNum, street, city, province, country):
        self.streetNum = streetNum
        self.street = street
        self.city = city
        self.province = province
        self.country = country


class Parking(PSOAAtom):

    def __init__(self, numSpots=None):
        self.predicate = IRI('Parking')
        self.oid = Parking.genOID('pk')
        self.totalParkingSpots = numSpots if numSpots else randint(300, 600)
        self.rating = ratings[randint(0, 4)]


class HVAC(PSOAAtom):

    def __init__(self):
        self.predicate = IRI('HVAC')
        self.oid = HVAC.genOID('hv')
        self.rating = ratings[randint(0, 4)]


class FrontDesk(PSOAAtom):

    def __init__(self):
        self.predicate = IRI('FrontDesk')
        self.oid = HVAC.genOID('fd')
        if random() > 0.8:
            self.opening_hours = '{0}:00-{1}:00'.format(randint(6, 8), randint(16, 19))
        else:
            self.opening_hours = '0:00-24:00'


class Building(PSOAAtom):
    posArgNames = ['streetNum', 'street', 'city', 'province', 'country', 'yearBuilt', 'contact']

    def __init__(self, streetNum, street, city, province, country, yearBuilt=None, contact=None, suites=None):
        self.predicate = IRI('Building')
        self.oid = Building.genOID('bd')
        self.streetNum = streetNum
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.yearBuilt = yearBuilt if yearBuilt else randint(1970, 2010)
        if random() > 0.9:
            self.parking = Parking()
        self.contact = contact if contact else '416-{0:03d}-{1:03d}'.format(randint(0, 999), randint(0, 999))
        self.totalElevators = randint(0, 2)
        self.hasPart = suites if suites else [Suite() for i in range(randint(*Building.suitePerBuildingRange))]
        self.frontdesk = FrontDesk()


    # def generateSuites(self, num):
    #     suites = [None]*num
    #     for i in range(num):
    #         suites[i] = Suite()
    #     self.suites = suites


class Door(PSOAAtom):
    def __init__(self, adjSpace):
        self.predicate = IRI('Door')
        self.oid = Door.genOID('dr')
        self.plusY = adjSpace


class Measure:
    meter = IRI('m')
    sqmeter = IRI('sqm')
    measureFunc = IRI('measure')
    def __init__(self, amount, unitOfMeasure):
        self.amount = amount
        self.unitOfMeasure = unitOfMeasure

    def __str__(self):
        return '{0}({1} {2})'.format(Measure.measureFunc, self.amount, self.unitOfMeasure)

class Suite(PSOAAtom):
    posArgNames = ['floor', 'suiteNum', 'area', 'monthlyRent']
    directions = ['plusX', 'minusY', 'minusX', 'plusY']

    def __init__(self, area=None):
        self.predicate = IRI('Suite')
        self.oid = Suite.genOID('st')
        self.floor = randint(1, 5)
        self.suiteNum = self.floor * 100 + randint(1, 20)
        self.hvac = HVAC()
        self.utility = randomListFromDist([(IRI('internet'), 0.9), (IRI('phone'), 0.8)])
        self.generateSuiteParts()

    def generateSuiteParts(self):
        suiteParts = list()
        # if random() > 0.7:
        #     suiteParts.append(SuiteSubspace(SuiteSubspace.kitchenType))
        # for i in range(randint(0, 2)):
        #     suiteParts.append(SuiteSubspace(choice(SuiteSubspace.meetingSpaceTypes)))
        #
        # suiteParts.extend(SuiteSubspace() for i in range(len(suiteParts), randint(*Suite.subspacePerSuiteRange)))
        #
        direction = 0
        sideX = randint(10, 40) / Decimal(10)
        sideY = randint(10, 40) / Decimal(10)
        points = list()
        part = SuiteSubspace(sideX, sideY, None)
        suiteParts.append(part)
        points.append((0, 0))
        deltaAngle = 0
        roomX = sideX
        roomY = 0

        while True:
            lastPart = part
            sideX = randint(10, 40) / Decimal(10)
            roomX += sideX
            part = SuiteSubspace(sideX, sideY, None)
            suiteParts.append(part)
            lastPart.plusX = part
            if random() < 0.25:
                break

        while True:
            lastPart = part
            sideY = randint(10, 40) / Decimal(10)
            roomY += sideY
            part = SuiteSubspace(sideX, sideY, None)
            suiteParts.append(part)
            part.plusY = lastPart
            if random() < 0.33:
                break

        roomY += Decimal(0.5)
        self.area = int(roomX * roomY)
        self.monthlyRent = randint(10, 50) * self.area
        print(self.monthlyRent)
        potentialReceptions = list()
        while True:
            lastPart = part
            sideX = randint(10, 20) / Decimal(10)
            roomX -= sideX
            if roomX < 0:
                break
            part = SuiteSubspace(sideX, sideY, None)
            suiteParts.append(part)
            part.plusX = lastPart
            potentialReceptions.append(part)

        while True:
            lastPart = part
            sideY = randint(10, 40) / Decimal(10)
            if roomY > sideY:
                roomY -= sideY
                part = SuiteSubspace(sideX, sideY, None)
                lastPart.plusY = part
                suiteParts.append(part)
            elif roomY < 1:
                part.sideY += roomY
                part.plusY = suiteParts[0]
                break
            else:
                sideY = roomY
                part = SuiteSubspace(sideX, sideY, None)
                lastPart.plusY = part
                part.plusY = suiteParts[0]
                suiteParts.append(part)
                break

        reception = choice(potentialReceptions)
        reception.predicate = SuiteSubspace.receptionType
        self.hasPart = suiteParts
        self.entrance = Door(reception)

        assignedParts = set()
        assignedParts.add(reception)
        if random() > 0.7:
            while True:
                kitchen = choice(suiteParts)
                if kitchen not in assignedParts:
                    assignedParts.add(kitchen)
                    kitchen.predicate = choice(SuiteSubspace.kitchenTypes)
                    break

        for i in range(randint(0, 2)):
            while True:
                room = choice(suiteParts)
                if room not in assignedParts:
                    assignedParts.add(room)
                    room.predicate = choice(SuiteSubspace.meetingSpaceTypes)
                    break

        self.totalClosedOffices = 0
        self.totalCubicles = 0
        self.totalOpenWorkSpaceArea = 0
        for space in suiteParts:
            iri = space.predicate
            if iri is SuiteSubspace.closeOfficeType:
                self.totalClosedOffices += 1
            elif iri is SuiteSubspace.cubicleType:
                self.totalCubicles += 1
            elif iri is SuiteSubspace.openOfficeType:
                self.totalOpenWorkSpaceArea += space.sideX * space.sideY
        self.totalOpenWorkSpaceArea = Measure(self.totalOpenWorkSpaceArea, Measure.meter)


class SuiteSubspace(PSOAAtom):
    isIndependent = True
    posArgNames = ['sideX', 'sideY']
    closeOfficeType = IRI('ClosedOffice')
    cubicleType = IRI('Cubicle')
    openOfficeType = IRI('OpenOffice')
    officeTypesGen = [closeOfficeType, cubicleType, openOfficeType]
    meetingSpaceTypes = [IRI('OpenMeetingSpace'), IRI('ClosedMeetingSpace')]
    receptionType = IRI('Reception')
    kitchenTypes = [IRI('OpenKitchen'), IRI('ClosedKitchen')]

    def __init__(self, sideX = None, sideY = None, spaceType = None):
        self.predicate = spaceType if spaceType else choice(SuiteSubspace.officeTypesGen)
        self.oid = SuiteSubspace.genOID('sp')
        if sideX and sideY:
            self.sideX = sideX
            self.sideY = sideY
        else:
            self.sideX = randint(10, 30) / Decimal(10)
            self.sideY = randint(10, 30) / Decimal(10)
        # self.rating = ratings[randint(0, 4)]

def run(pathOutput):
    with open(pathOutput, 'w') as fileOutput, open('addresses.csv') as addrInput:
        addrInput.readline()
        addrIter = iter(csv.reader(addrInput))
        fileOutput.write('Document(\n')
        fileOutput.write('  Prefix(: <http://psoa.ruleml.org/usecases/OfficeProspector/>)\n')
        fileOutput.write('  Prefix(op-rtg: <http://psoa.ruleml.org/usecases/OfficeProspector/rating#>)\n\n')
        fileOutput.write('  Group(\n')
        for i in range(numBuildings):
            cols = list(next(addrIter))
            Building(cols[3], cols[4], "Toronto", "ON", "CA").write(fileOutput, 4)
        fileOutput.write('  )\n')
        fileOutput.write(')\n')


numBuildings = 50
Building.suitePerBuildingRange = (1, 5)
Suite.subspacePerSuiteRange = (5, 10)
run('office.psoa')
