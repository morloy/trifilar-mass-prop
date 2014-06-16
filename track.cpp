#include <iostream>
#include <vector>
#include<stdio.h>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

// TrackColour.cpp : Defines the entry point for the console application.
//

IplImage* GetThresholdedImage(IplImage* img)
{
	// Convert the image into an HSV image
	IplImage* imgHSV = cvCreateImage(cvGetSize(img), 8, 3);
	cvCvtColor(img, imgHSV, CV_BGR2HSV);

	IplImage* imgThreshed = cvCreateImage(cvGetSize(img), 8, 1);

	// Values 20,100,100 to 30,255,255 working perfect for yellow at around 6pm
	cvInRangeS(imgHSV, cvScalar(150, 0, 100), cvScalar(349, 255, 255), imgThreshed);

	cvReleaseImage(&imgHSV);

	return imgThreshed;
}

int main(int argc, char* argv[])
{
    // Check the number of parameters
    if (argc < 2) {
        // Tell the user how to run the program
        std::cerr << "Usage: " << argv[0] << " NAME" << std::endl;
        /* "Usage messages" are a conventional way of telling the user
         * how to run a program if they enter the command incorrectly.
         */
        return 1;
    }
    std::string filename = argv[1];
    std::string csv_filename = filename.replace(filename.end()-3, filename.end(),"csv");
	// Initialize capturing live feed from the camera
	CvCapture* capture = 0;
	capture = cvCreateFileCapture(argv[1]);	

    FILE * csv;
    csv = fopen (csv_filename.c_str(),"w");
    fprintf(csv, "x\ty\n");

	// Couldn't get a device? Throw an error and quit
	if(!capture)
    {
        printf("Could not initialize capturing...\n");
        return -1;
    }

	// The two windows we'll be using
    // cvNamedWindow("video");
	// cvNamedWindow("thresh");

	// This image holds the "scribble" data...
	// the tracked positions of the ball
	IplImage* imgScribble = NULL;

	// An infinite loop
	while(true)
    {
		// Will hold a frame captured from the camera
		IplImage* frame = 0;
		frame = cvQueryFrame(capture);

		// If we couldn't grab a frame... quit
        if(!frame)
            break;
		
		// If this is the first frame, we need to initialize it
		if(imgScribble == NULL)
		{
			imgScribble = cvCreateImage(cvGetSize(frame), 8, 3);
		}

		// Holds the yellow thresholded image (yellow = white, rest = black)
		IplImage* imgYellowThresh = GetThresholdedImage(frame);

		// Calculate the moments to estimate the position of the ball
		CvMoments *moments = (CvMoments*)malloc(sizeof(CvMoments));
		cvMoments(imgYellowThresh, moments, 1);

		// The actual moment values
		double moment10 = cvGetSpatialMoment(moments, 1, 0);
		double moment01 = cvGetSpatialMoment(moments, 0, 1);
		double area = cvGetCentralMoment(moments, 0, 0);

		// Holding the last and current ball positions
		static double posX = 0;
		static double posY = 0;

		double lastX = posX;
		double lastY = posY;

		posX = moment10/area;
		posY = moment01/area;

		// Print it out for debugging purposes
		fprintf(csv, "%f\t%f\n", posX, posY);

		// We want to draw a line only if its a valid position
        /*
		if(lastX>0 && lastY>0 && posX>0 && posY>0)
		{
			// Draw a yellow line from the previous point to the current point
			cvLine(imgScribble, cvPoint(posX, posY), cvPoint(lastX, lastY), cvScalar(0,255,255), 5);
		}
        */

		// Add the scribbling image and the frame... and we get a combination of the two
        /*
        cvAdd(frame, imgScribble, frame);
		cvShowImage("thresh", imgYellowThresh);
		cvShowImage("video", frame);
        */

		// Wait for a keypress
        /*
		int c = cvWaitKey(10);
		if(c!=-1)
		{
			// If pressed, break out of the loop
            break;
		}
        */

		// Release the thresholded image... we need no memory leaks.. please
		cvReleaseImage(&imgYellowThresh);

		delete moments;
    }

	// We're done using the camera. Other applications can now use it
	cvReleaseCapture(&capture);
    fclose(csv);
    return 0;
}
