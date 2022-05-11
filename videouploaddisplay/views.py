from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie
import cv2
from cvzone.PoseModule import PoseDetector
import ctypes

@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            handle_uploaded_file(file)
            try:
                cap = cv2.VideoCapture(file.name) 
                detector = PoseDetector()
                posList = []
                formatedList ={}
                index = 0
                def Mbox(title, text, style):
                    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

                while True:
                    success, img = cap.read()
                    img = detector.findPose(img)
                    lmList, bboxInfo = detector.findPosition(img)                
                    if bboxInfo:
                        lmString = []
                        
                        for lm in lmList:
                            lmString.append(lm)

                                
                        posList.append(lmString)
                        
                    cv2.imshow(file.name, img)
                    key = cv2.waitKey(1)
                    count = 0
                    first23 = 0
                    first24 = 0
                    flag= False
                    flag1= False
                    with open("AnimationFile.txt", 'w') as f:
                        f.writelines(["%s\n" % item for item in posList])

                        
                        
                    if(form.data['exercises'] == '1'):
                        for _ in posList:
                            count+=1
                            xcoord_12=_[12][1]
                            xcoord_14=_[14][1]
                            xcoord_16=_[16][1]
                            ycoord_16=_[16][2]
                            ycoord_14=_[14][2]
                            per_cen_14=ycoord_14+ycoord_14*0.05
                            per_cen_12=xcoord_12*0.05
                            if(ycoord_16>per_cen_14):
                                Mbox('proper Form Detected', 'round arm action detected, can lead to injury', 0)
                                cv2.destroyAllWindows()
                                return render(request, "upload-display-video.html", {'filename': 'video1.mp4'})
                            elif(xcoord_12-xcoord_14<=per_cen_12 and xcoord_12-xcoord_16<=per_cen_12 and flag1==False):
                                flag1=True
                                Mbox('proper Form Detected', 'javelin thrown', 0)
                                cv2.destroyAllWindows()
                                return render(request, "upload-display-video.html", {'filename': 'video1.mp4'})
                            elif(xcoord_16>=xcoord_14-xcoord_14*0.030 and flag==False):
                                flag=True
                                Mbox('Improper Form Detected', 'wrist is ahead of elbow too early, please watch correct form.', 0)
                                cv2.destroyAllWindows()
                                return render(request, "upload-display-video.html", {'filename': 'video1.mp4'})

                        # elif(form.data['exercises'] == '2'):
                        #     for _ in posList:
                        #         count+=1
                        #         if(count == 1):
                        #             first23 = _[13][1]
                                    
                        #             if(first23!=0):
                        #                 per_cen= first23*0.085
                        #                 print(per_cen)                                  
                                
                        #         if((first23-_[13][1])>=per_cen and flag==False):
                        #             flag=True
                        #             Mbox('Improper Form Detected', 'Shoulders moving, please watch correct form', 0)
                        #             cv2.destroyAllWindows()
                        #             return render(request, "upload-display-video.html", {'filename': 'video2.mp4'})
            except:
                cv2.destroyAllWindows()
                Mbox('Proper form', 'Great! You are doing exercise in correct form.', 0)
            else:
                print('else')
    else:
        form = UploadFileForm()
    return render(request, 'upload-display-video.html', {'form': form})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)