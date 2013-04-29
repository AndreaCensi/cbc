from cv2 import cv  # @UnresolvedImport

import time
from procgraph_cv import cv_to_numpy


def cv_capture_stream(cam):
    print('Opening capture')
    capture = cv.CaptureFromCAM(cam)
    print('Setting properties')
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 160)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 120)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 30)
    print('Starting')
    first = True
    while True:
        t = time.time()
        img = cv.QueryFrame(capture)
        if first:
            print('arrived first')
            first = False
            
        a = cv_to_numpy(img)
        yield t, a
    
def stream_diff(stream):
    last_t, last_img = None, None
    for t, img in stream:
        if last_t is None:
            last_t, last_img = t, img
            continue
        delta = t - last_t
        fps = 1 / delta
        print('delta: %.3f = %.1f fps' % (delta, fps))
        yield t, img
        last_t, last_img = t, img
#   
def cbc_live_demo_main():    
    # cv.NamedWindow("camera", 1)
    
#     capture = cv.CaptureFromCAM(0)
    
    stream = cv_capture_stream(cam=0)
    diff = stream_diff(stream)

    for t, img in diff:
        print t, img.shape
#     cv.DestroyAllWindows()
    


