from ESRFMultiCollect import *

class BM14MultiCollect(ESRFMultiCollect):
    def __init__(self, name):
        ESRFMultiCollect.__init__(self, name, CcdDetector(), TunableEnergy())

    @task
    def data_collection_hook(self, data_collect_parameters):
        self.getChannelObject("parameters").setValue(data_collect_parameters)
        self.execute_command("build_collect_seq")
        self.execute_command("prepare_beamline")

    @task
    def move_detector(self, detector_distance):
        self.bl_control.resolution.newDistance(detector_distance)

    @task
    def set_resolution(self, new_resolution):
        self.bl_control.resolution.move(new_resolution)


    def get_detector_distance(self):
        return self.bl_control.resolution.res2dist(self.bl_control.resolution.getPosition())


    def get_flux(self):
        return 0 
  

