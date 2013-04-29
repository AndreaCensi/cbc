from procgraph import Generator, Block

from cv2 import cv  # @UnresolvedImport
import time
import numpy as np
import warnings


class Display(Block):
    nimages = 0 
    
    Block.config('name', default=None)
    Block.config('position', default=None)
    
    Block.alias('cv_display')
    Block.input('rgb')
    
    def init(self):
        name = self.config.name
        if name is None:
            name = 'display%d' % Display.nimages
        self.name = name
            
        Display.nimages += 1
        
        cv.NamedWindow(self.name, 1)
    
        if self.config.position is not None:
            x, y = self.config.position
        else:
            cols = 4
            w, h = 320, 320
            u = Display.nimages % cols
            v = int(np.floor(Display.nimages / cols))
            x = u * w
            y = v * h
        
        cv.MoveWindow(self.name, x, y)
        
    def update(self):
        rgb = self.input.rgb
        img = numpy_to_cv(rgb)
        cv.ShowImage(self.name, img)
    
    def finish(self):    
        warnings.warn('to fix')
        cv.DestroyAllWindows()
    
        
class Capture(Generator):

    Block.alias('capture')
    Block.config('cam', default=0)
    Block.config('width', default=160)
    Block.config('height', default=120)
    Block.config('fps', default=10)
    
    Block.output('rgb')
    
    def init(self):
        cam = self.config.cam
        width = self.config.width
        height = self.config.height
        fps = self.config.fps
        
        self.info('Capturing cam=%d %dx%d @%.1f fps' % (cam, width, height, fps))
        self.capture = cv.CaptureFromCAM(cam)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FPS, fps)
    
    def update(self):
        t = time.time()
        img = cv.QueryFrame(self.capture)
        rgb = cv_to_numpy(img)
        self.set_output('rgb', value=rgb, timestamp=t)
    
    def next_data_status(self):
        return (True, None)



def numpy_to_cv(numpy_array):
    ''' Converts a HxW or HxWx3 numpy array to OpenCV 'image' '''
    
    dtype2depth = {
        'uint8': cv.IPL_DEPTH_8U,
        'int8': cv.IPL_DEPTH_8S,
        'uint16': cv.IPL_DEPTH_16U,
        'int16': cv.IPL_DEPTH_16S,
        'int32': cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }

    if len(numpy_array.shape) == 2:
        (height, width) = numpy_array.shape
        nchannels = 1
    elif len(numpy_array.shape) == 3:
        (height, width, nchannels) = numpy_array.shape
    else:
        raise ValueError('Invalid format shape %s' % str(numpy_array.shape))

    im_cv = cv.CreateImage((width, height),
                           dtype2depth[str(numpy_array.dtype)],
                           nchannels)
    cv.SetData(im_cv,
               numpy_array.tostring(),
               numpy_array.dtype.itemsize * width * nchannels)
    return im_cv


def cv_to_numpy(im):
    '''Converts opencv to numpy '''
    depth2dtype = {
        cv.IPL_DEPTH_8U: 'uint8',
        cv.IPL_DEPTH_8S: 'int8',
        cv.IPL_DEPTH_16U: 'uint16',
        cv.IPL_DEPTH_16S: 'int16',
        cv.IPL_DEPTH_32S: 'int32',
        cv.IPL_DEPTH_32F: 'float32',
        cv.IPL_DEPTH_64F: 'float64',
    }

    # arrdtype = im.depth
    a = np.fromstring(
         im.tostring(),
         dtype=depth2dtype[im.depth],
         count=im.width * im.height * im.nChannels)
    a.shape = (im.height, im.width, im.nChannels)
    return a
