#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "std_msgs/String.h"

class ObjectDetection{
    private:
        ros::Publisher msg_pub;
        ros::Subscriber image_sub_;
        image_transport::Publisher image_pub_;
        ros::NodeHandle nh_;
    public:
        ObjectDetection();
        std_msgs::String str;
        int hue_mn, hue_mx, sat_mn, sat_mx, value_mn, value_mx, bright_mn, bright_mx;

        void imageCb(const sensor_msgs::ImageConstPtr& msg); // 画像を読んだら呼ばれる関数
        void publishStr(cv::Point2f center, float radius);   // 前後左右どこに行くか返す関数
        int maxContours(std::vector<std::vector<cv::Point>> contours); // 各輪郭をcontourArea関数に渡し、最大面積を持つ輪郭を探す
        void test();
};

