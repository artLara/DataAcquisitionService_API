from .Visor import Visor
def run(trafficLightColor, face, verbose=True):
    visor = Visor()
    while(True):
        if visor.isFaceDetected():
            visor.start(trafficLightColor, face, verbose=verbose)
            continue

        if verbose:
            face.value = 0
            trafficLightColor.value = 2
            print('Not face in the image')