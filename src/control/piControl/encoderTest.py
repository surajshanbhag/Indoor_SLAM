import encoder

if __name__ == "__main__":
    encoder.encoderSetup()
    min = [500,500]
    max = [0,0]
    count = 0
    while True:
       R,L = encoder.readEncoder()
       if R<min[0]:
           min[0]=R
       if R>max[0]:
           max[0]=R

       if L<min[1]:
           min[1]=L
       if L>max[1]:
           max[1]=L
       count+=1
       if(count >1000):
            break
    print "min: ", min
    print "max: ", max


