class person:
    def __init__(self, pid, pname, centroid, roi_time):
        self.name = pname
        self.id = pid
        self.centroids = [centroid]
        self.ROI_enter_time = roi_time
        self.has_crossed = False
    
    def update(self, centroid):
        self.centroids.append(centroid)
        
    def entered(self, cross_time):
        self.has_crossed = True
        self.cross_line_time = cross_time

    def stat(self):
        print('person name:', self.name)

